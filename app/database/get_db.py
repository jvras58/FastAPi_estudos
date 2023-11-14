from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.config import get_settings

engine = create_engine(get_settings().DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
