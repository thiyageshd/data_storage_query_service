from pymongo import MongoClient
from typing import List, Dict
from datetime import datetime
from loguru import logger

from src.config import Config
from clients import MongoDBClient
from schemas.news import NewsRequest, NewsResponse, NewsItem


client = MongoClient(Config.MONGODB_URI)
db = client.get_database()

class NoSQLService:
    def __init__(self):
        self.client = MongoDBClient()


    async def store_news(self, company: str, news_data: List[Dict]):
        """ Stores news articles in MongoDB. """
        try:
            for article in news_data:
                article["company"] = company  # Add company field
                article["date"] = datetime.strptime(article["date"], "%Y-%m-%d")  # Convert date to DateTime

            self.client.collection.insert_many(news_data)

            return {"message": "News articles stored successfully"}
        except Exception as e:
            logger.error(f"Error storing news: {e}")
            raise e
    
    async def query_news(self, request: NewsRequest):
        """ Retrieves news articles based on company, date range, and keywords. """
        try:
            start_date = datetime.strptime(request.date_range["from"], "%Y-%m-%d")
            end_date = datetime.strptime(request.date_range["to"], "%Y-%m-%d")

            # Build MongoDB Query
            query = {
                "company": request.company,
                "date": {"$gte": start_date, "$lte": end_date},
                "summary": {"$regex": "|".join(request.keywords), "$options": "i"}  # Case-insensitive keyword match
            }

            news_articles = list(self.client.collection.find(query, {"_id": 0}))

            return NewsResponse(company=request.company, news=[NewsItem(**item) for item in news_articles])
        except Exception as e:
            logger.exception(f"Exception in querying news for request: {request}: {e}")
            raise e
    