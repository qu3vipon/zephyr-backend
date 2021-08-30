from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zephyr.app.core.config import settings

SQLALCHEMY_DATABASE_URL: str = settings.DB_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
