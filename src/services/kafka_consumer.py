import json
import asyncio
from confluent_kafka import Consumer
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from services import SQLService, NoSQLService
from config import Config

class KafkaConsumerService:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': Config.KAFKA_SERVERS,
            'group.id': Config.KAFKA_FINANCIAL_GROUP,
            'auto.offset.reset': 'earliest'  # Start consuming from the beginning if no offset exists
        })
        self.topic = Config.KAFKA_TOPIC
        self.consumer.subscribe([self.topic])
        self.sql_service = SQLService()
        self.nosql_service = NoSQLService()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.running = True

    async def consume_messages(self):
        """Consume messages from Kafka topic"""
        try:
            while self.running:
                msg = await asyncio.to_thread(self.consumer.poll, 1.0)
                # msg = self.consumer.poll(timeout=1.0)  # Wait for messages

                if msg is None:
                    continue
                if msg.error():
                    logger.error(f"Kafka error: {msg.error()}")
                    break
                
                try:
                    # Deserialize and process the message
                    data = json.loads(msg.value().decode('utf-8'))
                    financial_data = data.get("financial_data")
                    news_data = data.get("news_data")

                    await self.sql_service.store_financials([financial_data])
                    await self.nosql_service.store_news(company="yahoo", news_data=news_data)
                    logger.info(f"Processed message: {data}")
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            self.consumer.close()

    async def process_message(self, data):
        """Processes Kafka messages asynchronously."""
        try:
            financial_data = data["financial_data"]
            news_data = data["news_data"]
            await self.sql_service.store_financials(financial_data)
            await self.nosql_service.store_news(company="yahoo", news_data=news_data)
        except Exception as e:
            logger.error(f"Failed to process message: {e}")

    async def start_async_consumer(self):
        """Start Kafka consumer in an async background task."""
        await self.consume_messages()

    def stop(self):
        """Gracefully stop the Kafka consumer"""
        self.running = False
        self.consumer.close()
        logger.info("Kafka consumer stopped.")

# if __name__ == "__main__":
#     consumer = KafkaConsumerService()
#     consumer.consume_messages()
