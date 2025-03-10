from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse
from services.sql_service import SQLService
from services.nosql_service import NoSQLService

store_router = APIRouter()
sql_service = SQLService()
nosql_service = NoSQLService()

@store_router.post("/store/financials")
async def store_financials(request:Request):
    data = request.json
    result = await sql_service.store_financials(data)
    return JSONResponse(status_code=202, content=result)

@store_router.post("/store/news")
async def store_news(request:Request):
    data = request.json
    response = await nosql_service.store_news(company="yahoo", news_data=data)
    result = {"status": response, "message": "News data stored successfully"}
    return JSONResponse(status_code=202, content=result)
