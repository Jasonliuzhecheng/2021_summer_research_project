import pymongo

from util import get_database_config, get_common_config


def get_database(name):
	client = pymongo.MongoClient(get_database_config("common", "database_address"))
	return client[name]

# the default database
db = get_database(get_common_config("common", "database"))


def insert_data(collection, data: list):
	collection.insert_many(data)


def insert_one_data(collection, data: dict):
	collection.insert_one(data)


def query_field(collection, query = None, field = None):
	if query is None and field is None: return collection.find()
	if query is None: return collection.find({}, field)
	if field is None: return collection.find(query)
	return collection.find(query, field)


def delete_all_date(collection):
	collection.delete_many({})


def delete_all_db_data(database):
	for collection in database.list_collection_names(): delete_all_date(database[collection])


def update_data(collection, query: dict, new_value: dict):
	collection.update_many(query, new_value)
