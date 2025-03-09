from fastapi import FastAPI
from src.controllers import query_router, store_router
from src.services.kafka_consumer import KafkaConsumerService
import threading
from contextlib import asynccontextmanager

app = FastAPI(title="Data Storage Query Service")
app.include_router(query_router, prefix="/query")
app.include_router(store_router, prefix="/store")

def start_kafka_consumer():
    consumer = KafkaConsumerService()
    consumer.start_consumer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting...")
    threading.Thread(target=start_kafka_consumer).start()
    yield


@app.get("/")
def read_root():
    return {"message": "Data Storage & Query Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)