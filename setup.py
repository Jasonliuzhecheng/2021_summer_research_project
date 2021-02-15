import time
import store

from database import delete_all_db_data, db
from frontier.web_main import app
from preprocess import preprocess_dataset
from process import *


def init_preprocess_dataset():
	# remove all the data in the database
	delete_all_db_data(db)

	# you need to init the mongoDB first
	dataset_info = [
		{"dataset": "Aleppo2017", "insert_tasks": ["sleep_query", "screening", "gl"]},
		{"dataset": "Anderson2016", "insert_tasks": ["insulin", "enrollment", "clarke", "gl"]},
		{"dataset": "Buckingham2007", "insert_tasks": ["patient_info", "enrollment", "gl"]},
		{"dataset": "Chase2005", "insert_tasks": ["enrollment", "insulin_log", "gl"]},
		{"dataset": "D1NAMO", "insert_tasks": ["insulin", "gl"]},
		{"dataset": "Tamborlane2008", "insert_tasks": ["sleep_query", "summary", "blood_pressure", "gl"]},
		{"dataset": "Tsalikian2005", "insert_tasks": ["enrollment", "ultra_exercise", "freestyle_exercise", "gl"]},
		{"dataset": "Weinstock2016", "insert_tasks": ["enrollment", "unware", "med_chart", "gl"]},
	]
	preprocess_dataset(dataset_info)


def setup_query():
	# run the common query for fast query on the same query
	print(get_insulin_method_vs_gl(dataset = "all"))
	print(get_insulin_method_vs_gl(dataset = "Weinstock2016"))

	print(get_weight_vs_daily_insulin(dataset = "all", group = (30, 60, 90)))
	print(get_weight_vs_daily_insulin(dataset = "Anderson2016", group = (30, 60, 90)))
	print(get_weight_vs_daily_insulin(dataset = "Buckingham2007", group = (30, 60, 90)))
	print(get_weight_vs_daily_insulin(dataset = "Chase2005", group = (30, 60, 90)))
	print(get_weight_vs_daily_insulin(dataset = "Tsalikian2005", group = (30, 60, 90)))
	print(get_weight_vs_daily_insulin(dataset = "Weinstock2016", group = (30, 60, 90)))

	print(get_weight_vs_gl(dataset = "all", group = (30, 60, 90)))
	print(get_weight_vs_gl(dataset = "Anderson2016", group = (30, 60, 90)))
	print(get_weight_vs_gl(dataset = "Buckingham2007", group = (30, 60, 90)))
	print(get_weight_vs_gl(dataset = "Chase2005", group = (30, 60, 90)))
	print(get_weight_vs_gl(dataset = "Tsalikian2005", group = (30, 60, 90)))
	print(get_weight_vs_gl(dataset = "Weinstock2016", group = (30, 60, 90)))

	print(get_daily_insulin(dataset = "all", group = (20, 30, 40, 50)))
	print(get_daily_insulin(dataset = "Anderson2016", group = (20, 30, 40, 50)))
	print(get_daily_insulin(dataset = "Buckingham2007", group = (20, 30, 40, 50)))
	print(get_daily_insulin(dataset = "Chase2005", group = (20, 30, 40, 50)))
	print(get_daily_insulin(dataset = "D1NAMO", group = (20, 30, 40, 50)))
	print(get_daily_insulin(dataset = "Tsalikian2005", group = (20, 30, 40, 50)))
	print(get_daily_insulin(dataset = "Weinstock2016", group = (20, 30, 40, 50)))

	print(get_weight(dataset = "all", group = (30, 60, 90)))
	print(get_weight(dataset = "Anderson2016", group = (30, 60, 90)))
	print(get_weight(dataset = "Buckingham2007", group = (30, 60, 90)))
	print(get_weight(dataset = "Chase2005", group = (30, 60, 90)))
	print(get_weight(dataset = "Tsalikian2005", group = (30, 60, 90)))
	print(get_weight(dataset = "Weinstock2016", group = (30, 60, 90)))

	print(get_fast_insulin_time_vs_gl(dataset = "all"))
	print(get_fast_insulin_time_vs_gl(dataset = "D1NAMO"))

	print(get_bld_pr_dia(dataset = "all", group = (50, 60, 70, 80, 90)))
	print(get_bld_pr_dia(dataset = "Tamborlane2008", group = (50, 60, 70, 80, 90)))

	print(get_bld_pr_sys(dataset = "all", group = (100, 110, 120, 130, 140)))
	print(get_bld_pr_sys(dataset = "Tamborlane2008", group = (100, 110, 120, 130, 140)))

	print(get_low_gl(dataset = "all"))
	print(get_low_gl(dataset = "Anderson2016"))
	print(get_low_gl(dataset = "Weinstock2016"))

	print(get_breakfast_ratio(dataset = "all", group = (10, 15)))
	print(get_breakfast_ratio(dataset = "Buckingham2007", group = (10, 15)))
	print(get_breakfast_ratio(dataset = "Chase2005", group = (10, 15)))

	print(get_lunch_ratio(dataset = "all", group = (10, 15)))
	print(get_lunch_ratio(dataset = "Buckingham2007", group = (10, 15)))
	print(get_lunch_ratio(dataset = "Chase2005", group = (10, 15)))

	print(get_dinner_ratio(dataset = "all", group = (10, 15)))
	print(get_dinner_ratio(dataset = "Buckingham2007", group = (10, 15)))
	print(get_dinner_ratio(dataset = "Chase2005", group = (10, 15)))

	print(get_race(dataset = "all"))
	print(get_race(dataset = "Aleppo2017"))
	print(get_race(dataset = "Anderson2016"))
	print(get_race(dataset = "Buckingham2007"))
	print(get_race(dataset = "Chase2005"))
	print(get_race(dataset = "Tamborlane2008"))
	print(get_race(dataset = "Tsalikian2005"))
	print(get_race(dataset = "Weinstock2016"))

	print(get_gender(dataset = "all"))
	print(get_gender(dataset = "Aleppo2017"))
	print(get_gender(dataset = "Anderson2016"))
	print(get_gender(dataset = "Buckingham2007"))
	print(get_gender(dataset = "Chase2005"))
	print(get_gender(dataset = "Tamborlane2008"))
	print(get_gender(dataset = "Tsalikian2005"))
	print(get_gender(dataset = "Weinstock2016"))

	print(get_diag_age(dataset = "all", group = (20, 40, 60)))
	print(get_diag_age(dataset = "Aleppo2017", group = (20, 40, 60)))
	print(get_diag_age(dataset = "Anderson2016", group = (20, 40, 60)))

	print(get_trouble_sleep_vs_gl(dataset = "all"))
	print(get_trouble_sleep_vs_gl(dataset = "Aleppo2017"))
	print(get_trouble_sleep_vs_gl(dataset = "Tamborlane2008"))

	print(get_pre_meal_vs_gl(dataset = "all"))
	print(get_pre_meal_vs_gl(dataset = "Aleppo2017"))

	print(get_strict_meal_vs_gl(dataset = "all"))
	print(get_strict_meal_vs_gl(dataset = "Aleppo2017"))

	print(get_meal_vs_gl(dataset = "all"))
	print(get_meal_vs_gl(dataset = "Buckingham2007"))

	print(get_snack_vs_gl(dataset = "all"))
	print(get_snack_vs_gl(dataset = "Buckingham2007"))

	print(get_exercise_vs_gl(dataset = "all"))
	print(get_exercise_vs_gl(dataset = "Buckingham2007"))

	print(get_insulin_time_vs_gl(dataset = "all"))
	print(get_insulin_time_vs_gl(dataset = "Anderson2016"))

	print(get_time_vs_exercise_gl(dataset = "all", exercise_status = "Exercise"))
	print(get_time_vs_exercise_gl(dataset = "all", exercise_status = "Sedentary"))
	print(get_time_vs_exercise_gl(dataset = "Tsalikian2005", exercise_status = "Exercise"))
	print(get_time_vs_exercise_gl(dataset = "Tsalikian2005", exercise_status = "Sedentary"))

	print(get_time_vs_gl(dataset = "all"))
	print(get_time_vs_gl(dataset = "Aleppo2017"))
	print(get_time_vs_gl(dataset = "Anderson2016"))
	print(get_time_vs_gl(dataset = "Buckingham2007"))
	print(get_time_vs_gl(dataset = "Chase2005"))
	print(get_time_vs_gl(dataset = "Tamborlane2008"))
	print(get_time_vs_gl(dataset = "Tsalikian2005"))
	print(get_time_vs_gl(dataset = "Weinstock2016"))


if __name__ == '__main__':
	start = time.clock()

	# initial the store directory and clear the previous query result
	store.initial()

	# initial the mongo database
	init_preprocess_dataset()

	# initial the common query
	store.clear()
	setup_query()

	print("setup time usage:", time.clock() - start)

	# start the server
	app.run()
