from kafka import KafkaConsumer
from json import loads
from src.services.sql_service import SQLService
from src.services.nosql_service import NoSQLService
from src.config import Config

class KafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            Config.KAFKA_TOPIC,
            bootstrap_servers=Config.KAFKA_SERVERS,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        self.sql_service = SQLService()
        self.nosql_service = NoSQLService()

    def start_consumer(self):
        for message in self.consumer:
            data = message.value
            financial_data = data["financial_data"]
            news_data = data["news_data"]
            self.sql_service.store_financials(financial_data)
            self.nosql_service.store_news(news_data)