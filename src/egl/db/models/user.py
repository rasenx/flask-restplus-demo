import bcrypt
import uuid

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID, JSON, TEXT
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy import func

from egl.db.base import Base


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, index=True, unique=False, nullable=True)
    meta = Column(JSON, default=MutableDict, nullable=True)
    active = Column(Boolean, default=True, nullable=False, index=True)

    def change_password(self, password):
        password = password or ''

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def check_password(self, password):
        password = password or ''
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf-8'))
