from process.process_help import *
from util import combine_pie_plot_json


def get_time_vs_gl(dataset = "all", interval = "1h", cycle = "1d"):
	"""
	statistic the glucose value changes based on time
	@:param dataset: the list of query dataset name
	@:param interval: statistic minimum interval.
	@:param cycle: statistic cycle.
	@:return: the json result of the query
	"""
	return process_main(get_gl_plot, "get_time_vs_gl", dataset, interval, cycle)


def get_time_vs_exercise_gl(dataset = "all", exercise_status = "Exercise", interval = "1h", cycle = "1d"):
	"""
	statistic the glucose value changes based on time and exercise status
	@:param dataset: the list of query dataset name
	@:param exercise_status: the exercise_status value, either Exercise or Sedentary
	@:param interval: statistic minimum interval.
	@:param cycle: statistic cycle.
	@:return: the json result of the query
	"""
	return process_main(get_exercise_gl_plot, "get_time_vs_exercise_gl", dataset, exercise_status, interval, cycle)


def get_insulin_time_vs_gl(dataset = "all", interval = "1d", max_duration = "7d"):
	"""
	statistic the glucose value changes based on time after inject insulin
	@:param dataset: the list of query dataset name
	@:param interval: statistic minimum interval.
	@:param max_duration: statistic max_duration.
	@:return: the json result of the query
	"""
	return process_main(get_time_diff_list_status_vs_gl, "get_insulin_time_vs_gl",
	                    dataset, "insulin_id", interval, max_duration)


def get_meal_vs_gl(dataset = "all", interval = "1h", max_duration = "1d"):
	"""
	statistic the glucose value changes based on time after have meal
	@:param dataset: the list of query dataset name
	@:param interval: statistic minimum interval.
	@:param max_duration: statistic max_duration.
	@:return: the json result of the query
	"""
	return process_main(get_time_diff_list_status_vs_gl, "get_meal_vs_gl", dataset, "meal", interval, max_duration)


def get_snack_vs_gl(dataset = "all", interval = "1h", max_duration = "1d"):
	"""
	statistic the glucose value changes based on time after have snack
	@:param dataset: the list of query dataset name
	@:param interval: statistic minimum interval.
	@:param max_duration: statistic max_duration.
	@:return: the json result of the query
	"""
	return process_main(get_time_diff_list_status_vs_gl, "get_snack_vs_gl", dataset, "snack", interval, max_duration)


def get_exercise_vs_gl(dataset = "all", interval = "1h", max_duration = "1d"):
	"""
	statistic the glucose value changes based on time after have exercise
	@:param dataset: the list of query dataset name
	@:param interval: statistic minimum interval.
	@:param max_duration: statistic max_duration.
	@:return: the json result of the query
	"""
	return process_main(get_time_diff_list_status_vs_gl, "get_exercise_vs_gl",
	                    dataset, "exercise", interval, max_duration)


def get_fast_insulin_time_vs_gl(dataset = "all", interval = "1h", max_duration = "1d"):
	"""
	statistic the glucose value changes based on time after have fast insulin
	@:param dataset: the list of query dataset name
	@:param interval: statistic minimum interval.
	@:param max_duration: statistic max_duration.
	@:return: the json result of the query
	"""
	return process_main(get_time_diff_list_status_vs_gl, "get_fast_insulin_time_vs_gl",
	                    dataset, "fast_insulin", interval, max_duration)


def get_strict_meal_vs_gl(dataset = "all", group = list(), interval = "1h", cycle = "1d"):
	"""
	statistic the glucose value changes based on time and have strict meal level
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:param interval: statistic minimum interval.
	@:param cycle: statistic cycle.
	@:return: the json result of the query
	"""
	return process_main(get_status_vs_gl, "get_strict_meal_vs_gl",
	                    dataset, "StrictMealNow", group, interval, cycle)


def get_pre_meal_vs_gl(dataset = "all", group = list(), interval = "1h", cycle = "1d"):
	"""
	statistic the glucose value changes based on time and have pre meal level
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:param interval: statistic minimum interval.
	@:param cycle: statistic cycle.
	@:return: the json result of the query
	"""
	return process_main(get_status_vs_gl, "get_pre_meal_vs_gl", dataset, "PreMealInsNow", group, interval, cycle)


def get_trouble_sleep_vs_gl(dataset = "all", group = list(), interval = "1h", cycle = "1d"):
	"""
	statistic the glucose value changes based on time and have troble sleep level
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:param interval: statistic minimum interval.
	@:param cycle: statistic cycle.
	@:return: the json result of the query
	"""
	return process_main(get_status_vs_gl, "get_trouble_sleep_vs_gl",
	                    dataset, "trouble_sleep", group, interval, cycle)


def get_weight_vs_gl(dataset = "all", group = (30, 60, 90), interval = "1h", cycle = "1d"):
	"""
	statistic the glucose value changes based on time and weight
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:param interval: statistic minimum interval.
	@:param cycle: statistic cycle.
	@:return: the json result of the query
	"""
	return process_main(get_status_vs_gl, "get_weight_vs_gl", dataset, "weight", group, interval, cycle)


def get_insulin_method_vs_gl(dataset = "all", interval = "1h", cycle = "1d"):
	"""
	statistic the glucose value changes based on time and insulin method
	@:param dataset: the list of query dataset name
	@:param interval: statistic minimum interval.
	@:param cycle: statistic cycle.
	@:return: the json result of the query
	"""
	return process_main(get_status_vs_gl, "get_insulin_method_vs_gl",
	                    dataset, "insulin_method", list(), interval, cycle)


def get_gender(dataset = "all"):
	"""
	statistic the gender distribution
	@:param dataset: the list of query dataset name
	@:return: the json result of the query
	"""
	return process_main(get_status_statistic, "get_gender", dataset, "gender", list())


def get_race(dataset = "all"):
	"""
	statistic the race distribution
	@:param dataset: the list of query dataset name
	@:return: the json result of the query
	"""
	return process_main(get_status_statistic, "get_race", dataset, "race", list())


def get_diag_age(dataset = "all", group = (20, 40, 60)):
	"""
	statistic the diagnostic age distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_status_statistic, "get_diag_age", dataset, "diag_age", group)


def get_low_gl(dataset = "all"):
	"""
	statistic the diagnostic age distribution
	@:param dataset: the list of query dataset name
	@:return: the json result of the query
	"""
	return process_main(get_status_statistic, "get_low_gl", dataset, "low_gl", list())


def get_bld_pr_sys(dataset = "all", group = (100, 110, 120, 130, 140)):
	"""
	statistic the systolic blood pressure distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_status_statistic, "get_bld_pr_sys", dataset, "bld_pr_sys", group)


def get_bld_pr_dia(dataset = "all", group = (50, 60, 70, 80, 90)):
	"""
	statistic the diastolic blood pressure distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_status_statistic, "get_bld_pr_dia", dataset, "bld_pr_dia", group)


def get_weight(dataset = "all", group = (30, 60, 90)):
	"""
	statistic the weight distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_status_statistic, "get_weight", dataset, "weight", group)


def get_breakfast_ratio(dataset = "all", group = (10, 15)):
	"""
	statistic the breakfast ratio distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_list_status_statistic, "get_breakfast_ratio", dataset, "breakfast_ratio", group)


def get_lunch_ratio(dataset = "all", group = (10, 15)):
	"""
	statistic the lunch ratio distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_list_status_statistic, "get_lunch_ratio", dataset, "lunch_ratio", group)


def get_dinner_ratio(dataset = "all", group = (10, 15)):
	"""
	statistic the dinner ratio distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_list_status_statistic, "get_dinner_ratio", dataset, "dinner_ratio", group)


def get_daily_insulin(dataset = "all", group = (20, 30, 40, 50)):
	"""
	statistic the daily insulin distribution
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	result_1 = process_main(get_mult_field_status_statistic, "get_daily_insulin",
	                        dataset, ["fast_insulin", "slow_insulin"], group, "1d")
	result_2 = process_main(get_list_status_statistic, "get_daily_insulin", dataset, "daily_insulin", group)
	return combine_pie_plot_json([result_1, result_2])


def get_weight_vs_daily_insulin(dataset = "all", group = (30, 60, 90)):
	"""
	statistic the daily insulin based on weight
	@:param dataset: the list of query dataset name
	@:param group: the divider of the group, ex: divider [10, 20] -> the value will group [<11, 11-20, >20]
	@:return: the json result of the query
	"""
	return process_main(get_status1_vs_status2_statistic, "get_weight_vs_daily_insulin",
	                    dataset, "weight", "daily_insulin", group)
