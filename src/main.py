from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager

from controllers import query_router, store_router
from services.kafka_consumer import KafkaConsumerService
from clients.sql_client import init_db as init_sql_db
from clients.nosql_client import init_db as init_nosql_db


consumer = KafkaConsumerService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    asyncio.create_task(consumer.start_async_consumer())
    init_sql_db()
    init_nosql_db()
    yield
    consumer.stop() 


app = FastAPI(title="Data Storage Query Service", lifespan=lifespan)
app.include_router(query_router, prefix="/query")
app.include_router(store_router, prefix="/store")


@app.get("/")
def read_root():
    return {"message": "Data Storage & Query Service"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
