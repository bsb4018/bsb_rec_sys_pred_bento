import os
from exception import PredictionException
from constants import MONGO_DATABASE_NAME,MONGO_COLLECTION_NAME,MONGO_DB_URL
import sys
import pymongo

class MongoDBClient:
    client = None
    def __init__(self):
        try:
            self.database_name = MONGO_DATABASE_NAME
            self.collection_name = MONGO_COLLECTION_NAME
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGO_DB_URL)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGO_DB_URL} is not set")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            self.client = MongoDBClient.client
            self.database = self.client[self.database_name]
            self.dbcollection = self.client[self.database_name][self.collection_name]
        except Exception as e:
            raise PredictionException(e,sys)
