import math
import store

from database import query_field, db
from collections import defaultdict
from util import (get_plot_json, int_to_timestamp, get_process_config, get_mult_plot_json,
                  get_pie_plot_json, get_histogram_json)


def get_group(divides: list or tuple, value: str or int or float):
	"""
	Get the value's group by the divides.
	If the divides is empty, this means the value don't need to group.
	@param divides: the divides for the group.
					ex: divides [10, 20] -> the value will group [<11, 11-20, >20]
	@param value: the value need to group. the value should be numeric.
	@return: the value's group name
	"""
	# if the divides is empty, return the value.
	if len(divides) == 0: return value

	digit = int(math.log(divides[-1], 10)) + 1

	# get the divide_idx.
	# ensure divides[divide_idx] >= value or the divide_idx reach the end of divides
	divide_idx = 0
	while divide_idx < len(divides) and float(value) > divides[divide_idx]: divide_idx += 1

	# ASSUMPTION: the digit will not bigger than 3
	if digit == 1:
		# if value <= divides[0]
		if divide_idx == 0: return "{:0>1d}-{:0>1d}".format(0, int(divides[0]))
		# if value > divides[-1]
		elif divide_idx >= len(divides): return ">{:0>1d}".format(int(divides[-1]))
		# if value between two divides
		else: return "{:0>1d}-{:0>1d}".format(int(divides[divide_idx - 1]) + 1, int(divides[divide_idx]))
	elif digit == 2:
		# if value <= divides[0]
		if divide_idx == 0: return "{:0>2d}-{:0>2d}".format(0, int(divides[0]))
		# if value > divides[-1]
		elif divide_idx >= len(divides): return ">{:0>2d}".format(int(divides[-1]))
		# if value between two divides
		else: return "{:0>2d}-{:0>2d}".format(int(divides[divide_idx - 1]) + 1, int(divides[divide_idx]))
	elif digit == 3:
		# if value <= divides[0]
		if divide_idx == 0: return "{:0>3d}-{:0>3d}".format(0, int(divides[0]))
		# if value > divides[-1]
		elif divide_idx >= len(divides): return ">{:0>3d}".format(int(divides[-1]))
		# if value between two divides
		else: return "{:0>3d}-{:0>3d}".format(int(divides[divide_idx - 1]) + 1, int(divides[divide_idx]))


def get_functiona_all_dataset(function_name: str):
	"""
	@param function_name: the name of the function, should exist in the process config
	@return: a list of all valid dataset name for the function
	"""
	return get_process_config(function_name, "all_dataset").split("\n")


def get_time_from_str(time: str):
	"""
	Transform the time (string format) to int (unit second).
	If the unit cannot recognize, it will return 0
	@param time: the format should be value + unit. ex: "1s", "25m", "3w".
				 the value should be int, the unit should be one of "s", "m", "h", "d", "w"
	@return: the int value of time, unit second.
	"""
	digit, level = int(time[:-1]), time[-1]
	if level == "s": return digit
	if level == "m": return digit * 60
	if level == "h": return digit * 3600
	if level == "d": return digit * 86400
	if level == "w": return digit * 604800
	return 0

time_hour = get_time_from_str("1h")


def assert_dataset(function_name, dataset_name):
	"""
	Assert the dataset name is valid for the function.
	If the dataset name is all, the function will return all the valid dataset name.
	@param function_name: the function name.
	@param dataset_name: the name of the dataset name. It could be string of list of string
	@return: return the processed dataset name, the return type is list.
	"""
	all_dataset_name = get_functiona_all_dataset(function_name)
	all_dataset_name.sort()

	# return all the valid dataset name if the dataset_name is "all"
	if dataset_name == "all": return all_dataset_name
	else:
		if isinstance(dataset_name, str):
			assert dataset_name in all_dataset_name
			# return the list of dataset name
			return [dataset_name]
		if isinstance(dataset_name, list):
			for name in dataset_name: assert name in all_dataset_name
			dataset_name.sort()
			return dataset_name


def process_main(help_function, function_name: str, dataset_name, *args):
	"""
	The main function for the process. The function can work by only using this function.
	@param help_function: the help function, complish main process logic
	@param function_name: the name of the function
	@param dataset_name: the dataset need to process
	@param args: the remain parameters, for help function
	@return: the json result of the query
	"""
	# assert the dataset name is valid
	dataset_name = assert_dataset(function_name, dataset_name)

	# get the json file name
	json_file = function_name + "_" + str(dataset_name) + "_" + "_".join([str(i) for i in args])

	# if the query result exist in store directory, get result from store directory
	if store.exist(json_file): return store.load(json_file)

	# if the query result doesn't exist in store directory, get result from the help function
	json_result = help_function(dataset_name, args)
	
	# store the json result
	store.store(json_file, json_result)
	return json_result


def get_status_statistic(dataset_name: list, args: tuple):
	"""
	Statistic the proportion of different status
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the statistic field status and the group information
	@return: the json result of the query
	"""
	status, group = args
	statistic_result = dict()
	for name in dataset_name:
		for query_result in query_field(db[name], field = {"_id": 0, status: 1}):
			if status in query_result:
				# get the query value's group result
				key = get_group(group, query_result[status])
				if key not in statistic_result: statistic_result[key] = 0
				statistic_result[key] += 1

	# return the pie plot result
	return get_pie_plot_json({key: statistic_result[key] for key in statistic_result})


def get_mult_field_status_statistic(dataset_name, args):
	"""
	Statistic the proportion of different status
	This function will get the sum of differnt field in a period of time, group the sum.
	Adhoc for get_daily_insulin_time_vs_gl.
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the statistic fields status and the group information
	@return: the json result of the query
	"""
	fields, group, period = args

	# get the time period and query field
	time_period = get_time_from_str(period)
	statistic_result, field = defaultdict(lambda: 0), {f: 1 for f in fields}
	field["patient_id"] = 1

	for name in dataset_name:
		# statistic based on the patient id. For get the patient mean status
		result = defaultdict(lambda: defaultdict(lambda: 0))
		for query_result in query_field(db[name], field = field):
			if "patient_id" not in query_result: continue
			patient_id = query_result["patient_id"]
			for f in fields:
				if f not in query_result: continue
				for r, datetime in query_result[f]: result[patient_id][datetime // time_period] += float(r)

		# get the statistic result based on the patient mean status
		for patient_id in result:
			mean_status = sum(result[patient_id][t] for t in result[patient_id]) / len(result[patient_id])
			key = get_group(group, mean_status)
			statistic_result[key] += 1

	# return the pie plot result
	return get_pie_plot_json({key: statistic_result[key] for key in statistic_result})


def get_list_status_statistic(dataset_name, args):
	"""
	Statistic the proportion of different status.
	The status is store in list style.
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the statistic field status and the group information
	@return: the json result of the query
	"""
	status, group = args
	statistic_result = dict()
	for name in dataset_name:
		dataset = db[name]
		for query_result in query_field(dataset, field = {"_id": 0, status: 1}):
			# make sure the query result has field status
			if status not in query_result: continue
			for result in query_result[status]:
				# if the result contains timestamp, we don't need timestamp here and just get the content
				if isinstance(result, list): result = result[0]

				# get the query value's group result
				key = get_group(group, result)
				if key not in statistic_result: statistic_result[key] = 0
				statistic_result[key] += 1

	# return the pie plot result
	return get_pie_plot_json({key: statistic_result[key] for key in statistic_result})


def get_status1_vs_status2_statistic(dataset_name, args):
	"""
	Get status2 statistic group by the status1 group.
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the statistic field status1 and status2 and the group information
	@return: the json result of the query
	"""
	status1, status2, group = args
	statistic_result = dict()
	for name in dataset_name:
		dataset = db[name]
		for query_result in query_field(dataset, field = {"_id": 0, status1: 1, status2: 1}):
			# make sure the query result has field status1 and status2
			if status1 not in query_result or status2 not in query_result: continue

			# get the query value's group result
			key = get_group(group, query_result[status1])
			if key not in statistic_result: statistic_result[key] = [0, 0]

			# append the status2 query result into status1 group result
			for status in query_result[status2]:
				statistic_result[key][0] += float(status)
				statistic_result[key][1] += 1

	# return the histogram result
	return get_histogram_json({key: statistic_result[key][0] / statistic_result[key][1] for key in statistic_result})


def get_status_vs_gl(dataset_name, args):
	"""
	Get mean glucose value based on the status group result.
	The glucose value will statistic every time interval and cycle every time cycle.
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the statistic field status, time interval, time cycle and the group information
	@return: the json result of the query
	"""
	status, group, interval, cycle = args

	# get time interval and time cycle value
	time_interval, time_cycle = get_time_from_str(interval), get_time_from_str(cycle)

	# get hour digit for consistent format
	hour_digit = int(math.log(time_cycle / time_hour, 10)) + 1
	
	# prepare the processed timestamp based on the time interval and time cycle
	timestamp_trans_list = [int_to_timestamp(i // time_interval * time_interval, hour_digit = hour_digit)
	                        for i in range(time_cycle)]

	statistic_result = dict()
	for name in dataset_name:
		# for every dataset
		for query_result in query_field(db[name], field = {"_id": 0, status: 1, "gl": 1}):
			if status in query_result and "gl" in query_result:
				# get the query value's group result
				key = get_group(group, query_result[status])
				if key not in statistic_result: statistic_result[key] = defaultdict(lambda: [0, 0])

				# append query glucose value into status group result
				for gl, datetime in query_result["gl"]:
					datetime_trans = timestamp_trans_list[datetime % time_cycle]
					statistic_result[key][datetime_trans][0] += float(gl)
					statistic_result[key][datetime_trans][1] += 1

	# get the query result from statistic result
	result = {status: {timestamp: statistic_result[status][timestamp][0] / statistic_result[status][timestamp][1]
	                   for timestamp in statistic_result[status]} for status in statistic_result}
	
	# return the mult plot result
	return get_mult_plot_json(result)


def get_time_diff_list_status_vs_gl(dataset_name, args):
	"""
	Get mean glucose value based on the status result. The status should also store with timestamp.
	The function will statistic the glucose value when a status comes and before the next status comes.
	The glucose value will statistic every time interval and statistic at most time max duration
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the statistic field status, time interval and time max duration.
	             Currently does not has group information.
	@return: the json result of the query
	"""
	status, interval, max_duration = args
	
	# get time interval and time cycle value
	time_interval, time_max_duration = get_time_from_str(interval), get_time_from_str(max_duration)

	# get hour digit for consistent format
	hour_digit = int(math.log(time_max_duration / time_hour, 10)) + 1
	
	# prepare the processed timestamp based on the time interval and time cycle
	timestamp_trans_list = [int_to_timestamp(i // time_interval * time_interval, hour_digit = hour_digit)
	                        for i in range(time_max_duration)]

	# statistic the query result
	gl_dict, status_dict = dict(), dict()
	for name in dataset_name:
		for query_result in query_field(db[name], field = {"_id": 0, "patient_id": 1, status: 1, "gl": 1}):
			if "patient_id" in query_result and "gl" in query_result and status in query_result:
				patient_id = query_result["patient_id"]
				
				# add patient id to status_dict and gl_dict
				if patient_id not in status_dict: status_dict[patient_id] = list()
				if patient_id not in gl_dict: gl_dict[patient_id] = list()
				
				# append query glucose value and datetime into status_dict and gl_dict
				for status_result, datetime in query_result[status]:
					status_dict[patient_id].append(int(datetime))
				for gl_result, datetime in query_result["gl"]:
					gl_dict[patient_id].append((int(datetime), float(gl_result)))

	# for each patient sort the result for faster time matching
	for patient_id in status_dict: status_dict[patient_id].sort()
	for patient_id in gl_dict: gl_dict[patient_id].sort(key = lambda x: x[0])

	# matching result
	statistic_result = dict()
	for patient_id in status_dict:
		# patient should also has glucose record
		if patient_id not in gl_dict: continue

		# get the patient's status and glucose data
		status_list, gl_list = status_dict[patient_id], gl_dict[patient_id]
		
		status_idx, gl_idx = 0, 0
		while status_idx < len(status_list):
			# set a sliding window to find match datetime, the valid glucose datetime should in the sliding window.
			left = status_list[status_idx]
			right = min(status_list[status_idx] + time_max_duration,
						float("inf") if status_idx >= len(status_list) - 1 else status_list[status_idx + 1])

			# ensure the glucose datetime bigger than the window's left side
			while gl_idx < len(gl_list) and left > gl_list[gl_idx][0]: gl_idx += 1
			
			while gl_idx < len(gl_list):
				# if the glucose datetime smaller than the windows's right side
				if right > gl_list[gl_idx][0]:
					# get the datetime diff
					diff = timestamp_trans_list[gl_list[gl_idx][0] - left]
					if diff not in statistic_result: statistic_result[diff] = [0, 0]
					
					# append the glucose result into the datetime diff
					statistic_result[diff][0] += float(gl_list[gl_idx][1])
					statistic_result[diff][1] += 1

					# check for next glucose result
					gl_idx += 1
				# if the glucose datetime bigger than the windows's right side, we need to update the window
				else: break

			# get next status	
			status_idx += 1

	# get the query result from statistic result		
	result = {timestamp: statistic_result[timestamp][0] / statistic_result[timestamp][1] for timestamp in statistic_result}

	# return the plot result
	return get_plot_json(result)


def get_gl_plot(dataset_name, args):
	"""
	Get mean glucose value. The glucose value will statistic every time interval and cycle every time cycle.
	This function also can be used for numeric list style field with timestamp with simple modify.
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the time interval and time cycle
	@return: the json result of the query
	"""
	interval, cycle = args

	# get time interval and time cycle value
	time_interval, time_cycle = get_time_from_str(interval), get_time_from_str(cycle)

	# get hour digit for consistent format
	hour_digit = int(math.log(time_cycle / time_hour, 10)) + 1
	
	# prepare the processed timestamp based on the time interval and time cycle
	timestamp_trans_list = [int_to_timestamp(i // time_interval * time_interval, hour_digit = hour_digit)
	                        for i in range(time_cycle)]

	statistic_result = defaultdict(lambda: [0, 0])
	for name in dataset_name:
		for query_result in query_field(db[name], field = {"_id": 0, "gl": 1}):
			if "gl" not in query_result: continue
			for gl, datetime in query_result["gl"]:
				datetime_trans = timestamp_trans_list[datetime % time_cycle]
				statistic_result[datetime_trans][0] += float(gl)
				statistic_result[datetime_trans][1] += 1

	# get the query result from statistic result
	result = {timestamp: statistic_result[timestamp][0] / statistic_result[timestamp][1]
	          for timestamp in statistic_result}

	# return the plot result
	return get_plot_json(result)


def get_exercise_gl_plot(dataset_name, args):
	"""
	Get mean exercise_gl value. The exercise_gl value will statistic every time interval and cycle every time cycle.
	@param dataset_name: the list of dataset name for statistic
	@param args: contain the certain exercise status, time interval and time cycle
	@return: the json result of the query
	"""
	exercise_status, interval, cycle = args

	# get time interval and time cycle value
	time_interval, time_cycle = get_time_from_str(interval), get_time_from_str(cycle)

	# get hour digit for consistent format
	hour_digit = int(math.log(time_cycle / time_hour, 10)) + 1
	
	# prepare the processed timestamp based on the time interval and time cycle
	timestamp_trans_list = [int_to_timestamp(i // time_interval * time_interval, hour_digit = hour_digit)
	                        for i in range(time_cycle)]

	statistic_result = defaultdict(lambda: [0, 0])
	for name in dataset_name:
		for query_result in query_field(db[name], field = {"_id": 0, "exercise_gl": 1, "exercise_status": 1}):
			if "exercise_gl" not in query_result or "exercise_status" not in query_result: continue
			
			# ASSUMPTION: the exercise glucose and exerices status is one-one related.
			for idx, (exercise_gl, datetime) in enumerate(query_result["exercise_gl"]):
				if query_result["exercise_status"][idx] != exercise_status: continue
				datetime_trans = timestamp_trans_list[datetime % time_cycle]
				statistic_result[datetime_trans][0] += float(exercise_gl)
				statistic_result[datetime_trans][1] += 1

	# get the query result from statistic result
	result = {timestamp: statistic_result[timestamp][0] / statistic_result[timestamp][1]
	          for timestamp in statistic_result}

	# return the plot result
	return get_plot_json(result)



