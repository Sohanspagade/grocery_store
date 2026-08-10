from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config.settings import settings
import sys

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(settings.mongodb_uri)
            # Ping to verify connection
            self.client.admin.command('ping')
            print("MongoDB Atlas connected successfully")
            self.db = self.client[settings.mongodb_database]
        except ConnectionFailure as e:
            print("Failed to connect to MongoDB Atlas.")
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print("An error occurred while connecting to MongoDB Atlas.")
            print(f"Error: {e}")
            sys.exit(1)
            
    def get_collection(self, collection_name: str):
        if self.db is None:
            self.connect()
        return self.db[collection_name]

mongodb = MongoDB()
