from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import config


engine = create_engine(config.DB_DEFAULT)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
