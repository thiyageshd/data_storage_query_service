from sqlalchemy import Column, Integer, String, Float

class Financials(Base):
    __tablename__ = "financials"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    year = Column(Integer, index=True)
    revenue = Column(Float)
    profit = Column(Float)
