from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

URL = f'postgresql://{settings.ML_DATABASE_USERNAME}:{settings.ML_DATABASE_PASSWORD}@{settings.ML_DATABASE_HOSTNAME}:{settings.ML_DATABASE_PORT}/{settings.ML_DATABASE_NAME}'

Base = declarative_base()  # Move this here

engine = create_engine(url=URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()