from sqlalchemy import create_engine
from models.models import Base

def create_engine_db():
    engine = create_engine('sqlite:///tiktok.db', echo=False)
    Base.metadata.create_all(bind=engine)
    return engine