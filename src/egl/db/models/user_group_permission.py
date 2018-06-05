from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import func

from egl.db.base import Base


class UserGroupPermission(Base):
    __tablename__ = 'user_group_permissions'

    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    user_group_id = Column(ForeignKey('user_groups.id'), primary_key=True)
    permission_id = Column(ForeignKey('permissions.id'), primary_key=True)
