from pymongo import MongoClient, ASCENDING
from config import Config

client = MongoClient(Config.MONGODB_URI)
db = client.get_database()

def init_db():
    # Create indexes if needed
    db.news.create_index([("company", 1), ("date", 1)])
    
class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = MongoClient(Config.MONGODB_URI)
            cls._instance.db = cls._instance.client[Config.MONGO_DB_NEWS]

            # Create index for fast querying (if not exists)
            cls._instance.db[Config.MONGO_COLLECTION_NEWS].create_index([("company", ASCENDING), ("date", ASCENDING)])
        
        return cls._instance

    @property
    def collection(self):
        return self.db[Config.MONGO_COLLECTION_NEWS]
    