import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from zephyr.app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), index=True, default=uuid.uuid4)
    username = Column(String(16), unique=True, index=True)
    password_hash = Column(String(64))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    registered_at = Column(DateTime, default=datetime.datetime.now)
    unregistered_at = Column(DateTime, nullable=True)
