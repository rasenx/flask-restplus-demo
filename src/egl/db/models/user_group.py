import uuid
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from egl.db.base import Base


class UserGroup(Base):
    __tablename__ = 'user_groups'

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    id = Column(UUID, default=uuid.uuid4, primary_key=True)
    parent_id = Column(UUID, ForeignKey('user_groups.id'), nullable=True, default=None)
    name = Column(String, nullable=False)
    is_system_group = Column(Boolean, nullable=False, default=False)

    members = relationship('User', secondary='user_group_members', back_populates='groups')
    permissions = relationship('Permission', secondary='user_group_permissions', back_populates='groups')
    children = relationship('UserGroup', lazy='joined', join_depth=1)
    parent = relationship('UserGroup', back_populates='children', remote_side=[id], lazy='joined', join_depth=1)
