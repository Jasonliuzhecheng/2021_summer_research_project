import os
import numpy as np

# root data dir
data_file_path = os.path.split(os.path.realpath(__file__))[0] + "/data"


def initial():
	if not os.path.exists(data_file_path): os.mkdir(data_file_path)


def get_file_path(file_name):
	return data_file_path + "/" + file_name + ".npy"


def store(file_name, data):
	np.save(get_file_path(file_name), data)


def load(file_name):
	return np.load(get_file_path(file_name), allow_pickle = True)


def load_dict(file_name):
	return np.load(get_file_path(file_name), allow_pickle = True).item()


def exist(file_name):
	return os.path.exists(get_file_path(file_name))


def clear():
	for file in os.listdir(data_file_path):
		os.remove(os.path.join(data_file_path, file))
