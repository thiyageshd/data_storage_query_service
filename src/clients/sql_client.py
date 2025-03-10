from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker

from config import Config

Base = declarative_base()
engine = create_engine(Config.POSTGRES_URL)

class Financials(Base):
    __tablename__ = "financials"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    year = Column(Integer, index=True)
    revenue = Column(Float)
    profit = Column(Float)


def init_db():
    Base.metadata.create_all(engine)

class DatabaseSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
            cls._instance.engine = create_engine(Config.POSTGRES_URL, pool_size=20, max_overflow=0)
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
        return cls._instance

# Singleton Instance
db_session = DatabaseSession()

def get_db():
    """Provides a database session for FastAPI requests."""
    db = db_session.SessionLocal()
    try:
        yield db
    finally:
        db.close()
