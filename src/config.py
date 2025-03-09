import os

class Config:
    KAFKA_TOPIC = "data_ingestion_topic"
    POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/financials")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/news")
    MONGO_COLLECTION_NEWS = os.getenv("MONGO_COLLECTION_NEWS", "news")
    MONGO_DB_NEWS = os.getenv("MONGO_DB_NEWS", "db_news")
    KAFKA_SERVERS = os.getenv("KAFKA_SERVERS", "localhost:9092")
    