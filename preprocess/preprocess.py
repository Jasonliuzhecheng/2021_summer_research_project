import os
import time
import xlrd

from database import query_field, update_data, insert_one_data, delete_all_date, db
from tqdm import tqdm
from collections import defaultdict
from util import (get_preprocess_config, line_count, line_count_xls, date_to_int, timestamp_to_int, datetime_to_int,
                  Reader)

LBS_TO_KG = 0.45359237

# status field, which means the field will not save as list style because one patient can only has one status
status_field_set = {"gender", "race", "diag_age", "trouble_sleep", "StrictMealNow", "PreMealInsNow",
                    "trouble_sleep_inverse", "low_gl", "bld_pr_sys", "bld_pr_dia", "weight", "insulin_method"}

# in default style, saving field will not contain timestamps
# the field here will contain timestamps when saving to the db
timestamp_field_set = {"gl", "exercise_gl", "raw_gl", "meal", "exercise", "snack", "insulin_id", "fast_insulin",
                       "slow_insulin"}

# combine the key field value to the content field
# should be numeric
combine_field_set = {"daily_insulin_b": "daily_insulin", "daily_insulin_l": "daily_insulin",
                     "daily_insulin_d": "daily_insulin", "daily_insulin_s": "daily_insulin",
                     "daily_insulin_bs": "daily_insulin"}


def preprocess_dataset(dataset_info):
	"""
	Preprocess the file information and insert into the database.
	The file type could be csv, txt and xls.
	The file information should hardcord in the config file.
	The function allow a increnmental way adding information to the database.
	@param dataset_info: The preprocess dataset information list. Each item in the list is a dictionary which contain 
						 the dataset name and all the insert task names. The insert task name should define in the config.
	@return: None
	"""
	for info in dataset_info:
		dataset_name, insert_tasks = info["dataset"], info["insert_tasks"]
		
		# get dataset preprocess config and basic information
		config = get_preprocess_config(dataset_name, insert_tasks)
		print("dataset: ", dataset_name)
		dataset = db[dataset_name]

		# delete all the data in the current dataset, may uncomment when developing
		# delete_all_date(dataset)

		# get all the patient id in the current dataset
		all_patient_id = {patient_id["patient_id"] for patient_id in
		                  query_field(dataset, field = {"_id": 0, "patient_id": 1})}

		# get the raw data for increnmental adding
		raw_data = {result["patient_id"]: {field: result[field] for field in result if field != "patient_id"}
		            for result in query_field(dataset)}
		data = defaultdict(lambda: dict())

		# for each sub dataset task
		for insert_task in insert_tasks:
			# get sub dataset basic information
			filenames = config[insert_task]["filename"]
			fields = config[insert_task]["select_column"]
			
			# ASSUMPTION: all the insert task has field patient_id and the meaning is the same.
			#             D1NAMO break the assumption and will adhoc get the patient id from file name.
			patient_idx = sum([i for i in range(len(fields)) if fields[i] == "patient_id"])

			for filename in filenames:
				# get the file real path
				file = os.path.join(os.path.join(config["root_dir"], config["dataset"]), filename)
				print("processing file", file)

				# ASSUMPTION: all the file type in the insert task is the same.
				# get the file reader and line count
				if config[insert_task]["file_type"] == "xls":
					cnt = line_count_xls(file)
					readable = Reader(xlrd.open_workbook(file).sheets()[0], config[insert_task]["file_type"])
				# file type is txt or csv
				else:
					cnt, readable = line_count(file), Reader(open(file), config[insert_task]["file_type"])

				# use tqdm to show the process progress
				with tqdm(total = cnt) as bar:
					for line_cnt in range(cnt):
						# get file content
						line = readable.readline()

						# if the line is not the header
						if line_cnt != 0:
							# get patient_id
							if dataset_name == "D1NAMO": patient_id = int(file.split("/")[-2])
							else: patient_id = str(int(float(line[patient_idx])))
							
							# if the patient id is not in the dataset, add this patient to the database.
							if patient_id not in all_patient_id:
								insert_one_data(dataset, {"patient_id": patient_id})
								all_patient_id.add(patient_id)

							# get line timestamp. if there is no timestamp, it will be 0
							timestamp = 0
							if "datetime" in fields:
								timestamp += sum(datetime_to_int(line[i], config[insert_task]["basedate"],
								                                 config[insert_task]["pattern"])
								                 for i in range(len(fields)) if fields[i] == "datetime")
							else:
								if "date" in fields:
									timestamp += sum(date_to_int(line[i], config[insert_task]["basedate"],
									                             config[insert_task]["pattern"])
									                 for i in range(len(fields)) if fields[i] == "date")
								if "timestamp" in fields:
									timestamp += sum(timestamp_to_int(line[i], config[insert_task]["pattern"])
									                 for i in range(len(fields)) if fields[i] == "timestamp")

							row_combine_field = dict()
							for idx in range(len(line)):
								if idx >= len(line): continue
								content, field = line[idx], config[insert_task]["select_column"][idx]

								# if the field should not append or there is no content in the line, continue
								if field == '' or len(content) == 0: continue

								# if the field is patient_id or timestamp related, continue
								if field in {"patient_id", "datetime", "date", "timestamp"}: continue
								
								# if the field is a status, the field content will not store in list style.
								if field in status_field_set:
									# adhoc for field trouble_sleep_inverse
									if field == "trouble_sleep_inverse":
										data[patient_id]["trouble_sleep"] = str(5 - int(content))
									# adhoc for field low_gl
									elif field == "low_gl":
										data[patient_id]["low_gl"] = content.split(" ")[0]
									else: data[patient_id][field] = content
								# adhoc for field weight_units (weight should in data before)
								elif field == "weight_units":
									if content == "lbs":
										data[patient_id]["weight"] = str(LBS_TO_KG * float(data[patient_id]["weight"]))
								# if the field is need store with timestamp
								elif field in timestamp_field_set:
									# adhoc for field raw_gl
									if field == "raw_gl":
										content = str(float(content) * 18)
										field = "gl"

									# if field not in patient's data, initial from raw data in database
									if field not in data[patient_id]:
										data[patient_id][field] = \
											list() if patient_id not in raw_data or field not in raw_data[patient_id] \
												   else raw_data[patient_id][field]
									
									# append the content with timestamp
									data[patient_id][field].append([content, timestamp])
								# if the field needs to combine to another field
								elif field in combine_field_set:
									combine_field = combine_field_set[field]
									if combine_field not in row_combine_field: row_combine_field[combine_field] = 0
									row_combine_field[combine_field] += float(content)
								# for the common field, store in list style
								else:
									# if field not in patient's data, initial from raw data in database
									if field not in data[patient_id]:
										data[patient_id][field] = \
											list() if patient_id not in raw_data or field not in raw_data[patient_id] \
												   else raw_data[patient_id][field]
									data[patient_id][field].append(content)
							
							# ASSUMPTION: the combine field is the common field (not status or store with timestamp)
							for field in row_combine_field:
								if field not in data[patient_id]: data[patient_id][field] = list()
								data[patient_id][field].append(str(row_combine_field[field]))
						
						# update the progress bar
						bar.update()

		# insert the preprocessed data to the database
		print("start to insert data to:", dataset_name)
		start = time.clock()
		for patient_id in data:
			for field in data[patient_id]:
				# update the field in the database
				update_data(dataset, {"patient_id": patient_id}, {'$set': {field: data[patient_id][field]}})
		print("use time to insert:", time.clock() - start)
