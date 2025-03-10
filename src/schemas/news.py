from pydantic import BaseModel
from typing import List, Dict

class NewsRequest(BaseModel):
    company: str
    date_range: Dict[str, str]
    keywords: List[str]

class NewsItem(BaseModel):
    title: str
    date: str
    summary: str

class NewsResponse(BaseModel):
    company: str
    news: List[NewsItem]
