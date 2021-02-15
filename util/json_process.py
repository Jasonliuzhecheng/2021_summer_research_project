import math
import json

from collections import defaultdict


def get_plot_json(result):
	json_str = {"type": "plot", "data": result}
	min_value = min([result[key] for key in result])
	json_str["min_value"] = min(math.floor(min_value / 10) * 10, 65)
	return json.dumps(obj = json_str, sort_keys = True)


def get_mult_plot_json(result):
	json_str = {"type": "mult_plot", "data": result}
	min_value = min([result[group][key] for group in result for key in result[group]])
	json_str["min_value"] = min(math.floor(min_value / 10) * 10, 65)
	return json.dumps(obj = json_str, sort_keys = True)


def get_pie_plot_json(result):
	json_str = {"type": "pie_plot", "data": result}
	return json.dumps(obj = json_str, sort_keys = True)


def combine_pie_plot_json(separate_results):
	json_str = {"type": "pie_plot", "data": defaultdict(lambda: 0)}
	for result in separate_results:
		result_str = json.loads(result)
		assert result_str["type"] == "pie_plot"
		for key in result_str["data"]:
			json_str["data"][key] += result_str["data"][key]
	return json.dumps(obj = json_str, sort_keys = True)


def get_histogram_json(result):
	json_str = {"type": "histogram", "data": result}
	min_value = min([result[key] for key in result])
	json_str["min_value"] = min(math.floor(min_value / 10) * 10, 65)
	return json.dumps(obj = json_str, sort_keys = True)
