from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import func

from egl.db.base import Base


class UserGroupMember(Base):
    __tablename__ = 'user_group_members'

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    user_group_id = Column(ForeignKey('user_groups.id'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), primary_key=True)
