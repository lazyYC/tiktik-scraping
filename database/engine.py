from sqlalchemy import create_engine
from models.models import Base

def create_engine_db():
    engine = create_engine('postgresql://postgres:admin@localhost:5432/tiktok-scraper', echo=False)
    # engine = create_engine('sqlite:///tiktok.db', echo=False)
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine