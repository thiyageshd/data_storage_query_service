from pydantic import BaseModel
from typing import List

class FinancialsRequest(BaseModel):
    company: str
    fields: List[str]
    years: List[int]

class FinancialsResponse(BaseModel):
    company: str
    data: dict
