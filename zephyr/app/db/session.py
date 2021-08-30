from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zephyr.app.core.config import settings

SQLALCHEMY_DATABASE_URL: str = settings._database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
