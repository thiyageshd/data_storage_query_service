from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

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
