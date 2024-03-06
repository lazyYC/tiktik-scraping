from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .engine import create_engine_db

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine_db())

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()