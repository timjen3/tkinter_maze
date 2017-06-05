import pickle
import os


def load_data():
	relative_file_path = "procedural_generator/Tools/floors.bin"
	if os.path.exists(relative_file_path):
		data = pickle.load(open(relative_file_path, "rb"))
		return data
	else:
		return []


def save_data(data):
	relative_file_path = "procedural_generator/Tools/floors.bin"
	pickle.dump(data, open(relative_file_path, "wb"))
