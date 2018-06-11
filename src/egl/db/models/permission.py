import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from egl.db.base import Base


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String, nullable=False)

    # groups = relationship('UserGroup', secondary='user_group_permissions', back_populates='permissions')
