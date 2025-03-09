# app/controllers/query_controller.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.services.sql_service import SQLService
from src.services.nosql_service import NoSQLService
from schemas.news import NewsRequest, NewsResponse
from schemas.financials import FinancialsRequest, FinancialsResponse

query_router = APIRouter()
sql_service = SQLService()
nosql_service = NoSQLService()

@query_router.post("/query/financials", response_model=FinancialsResponse)
async def query_financials(request: FinancialsRequest):
    result = await sql_service.query_financials(request)
    return JSONResponse(status_code=202, content=result)

@query_router.post("/query/news", response_model=NewsResponse)
async def query_news(request: NewsRequest):
    result = await nosql_service.query_news(request)
    return JSONResponse(status_code=202, content=result)