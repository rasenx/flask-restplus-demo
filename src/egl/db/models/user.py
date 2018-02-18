import uuid

from sqlalchemy.dialects.postgresql import UUID, JSON, TEXT
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Column, DateTime, String
from sqlalchemy import func

from egl.db.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    username = Column(String, index=True, unique=False, nullable=True)
    password = Column(String, index=True, unique=False, nullable=True)
    meta = Column(JSON, default=MutableDict, nullable=True)
