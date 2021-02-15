import os
import configparser


def get_common_config(section, option):
	config = configparser.ConfigParser()
	path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.join("config", "common.config"))
	config.read(path)
	if config.has_section(section) and config.has_option(section, option):
		return config.get(section, option)
	return None


def get_database_config(section, option):
	config = configparser.ConfigParser()
	path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.join("config", "database.config"))
	config.read(path)
	if config.has_section(section) and config.has_option(section, option):
		return config.get(section, option)
	return None


def get_process_config(section, option):
	config = configparser.ConfigParser()
	path = os.path.join(os.path.split(os.path.realpath(__file__))[0], os.path.join("config", "process.config"))
	config.read(path)
	if config.has_section(section) and config.has_option(section, option):
		return config.get(section, option)
	return None


def get_preprocess_config(dataset_name, sub_datasets):
	file_name = os.path.join(os.path.split(os.path.realpath(__file__))[0],
	                         os.path.join("config", dataset_name + ".config"))
	config = configparser.ConfigParser()
	config.read(file_name)

	# adhoc get preprocess config
	result = dict()
	result["root_dir"] = get_common_config("common", "root_dir")
	result["database"] = get_common_config("common", "database")
	result["dataset"] = config.get("common", "dataset")
	for sub_dataset in sub_datasets:
		result[sub_dataset] = dict()
		result[sub_dataset]["filename"] = config.get(sub_dataset, "filename").split("\n")
		result[sub_dataset]["column"] = config.get(sub_dataset, "column").split("|")
		result[sub_dataset]["select_column"] = config.get(sub_dataset, "select_column").split("|")
		if config.has_option(sub_dataset, "basedate"):
			result[sub_dataset]["basedate"] = config.get(sub_dataset, "basedate").split(".")
		else: result[sub_dataset]["basedate"] = None
		result[sub_dataset]["pattern"] = config.get(sub_dataset, "pattern")
		result[sub_dataset]["file_type"] = config.get(sub_dataset, "file_type")

	return result
