from clients import db_session
from models.financials import Financials
from schemas.financials import FinancialsRequest, FinancialsResponse


class SQLService:
    async def store_financials(self, data):
        session = db_session.SessionLocal()
        for item in data:
            financial = Financials(**item)
            session.add(financial)
        session.commit()
        session.close()
        return True

    async def query_financials(self, request: FinancialsRequest):
        session = db_session.SessionLocal()
        query_params = request.model_dump()
        query = session.query(Financials)
        if 'company' in query_params:
            query = query.filter(Financials.company == query_params['company'])
        if 'years' in query_params:
            query = query.filter(Financials.year.in_(query_params['years']))
        results  = query.all()
        data = {record.year: {field: getattr(record, field) for field in request.fields} for record in results}
        session.close()
        return FinancialsResponse(company=request.company, data=data)