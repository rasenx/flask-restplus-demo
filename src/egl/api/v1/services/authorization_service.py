import logging
from typing import Optional

from flask_login import current_user
from egl.db.models import UserGroup, UserGroupMember, UserGroupPermission, Permission, User
from egl.db.sessions import db
from egl.api.v1.defaults import Users, UserGroups

logger = logging.getLogger(__name__)


class AuthorizationService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def is_superuser(user: User=current_user) -> bool:
        return AuthorizationService.is_in_group(UserGroups.superusers, user=user)

    @staticmethod
    def is_in_group_or_ancestor(group: UserGroup, user: User=current_user) -> bool:
        target_group = group

        while not (target_group is None):
            if AuthorizationService.is_in_group(target_group, user):
                return True

            target_group = target_group.parent

        return False

    @staticmethod
    def is_in_group(group: UserGroup, user: User=current_user) -> bool:
        if not user or group:
            return False

        # if the user has no groups assigned, bail
        if user.groups is None:
            return False

        for g in user.groups:
            if str(g.id) == str(UserGroups.superusers.id):
                return True

            if str(g.id) == str(group.id):
                return True

        return False

    @staticmethod
    def has_permission(user: User, *permissions) -> bool:
        if user is None:
            return False

        if user.groups is None:
            return False

        for group in user.groups:
            if group.permissions is None:
                continue

            if str(group.id) == str(Groups.superusers.id):
                return True

            for group_permission in group.permissions:
                for permission in permissions:
                    if str(group_permission.id) == str(permission.id):
                        return True

        return False

    @staticmethod
    def get_effective_permissions(user: User=current_user) -> list:
        if user is None:
            return []

        if user.groups is None:
            return []

        permissions = []

        for group in user.groups:
            if group.permissions is None:
                continue

            if str(group.id) == str(Groups.superusers.id):
                return db.session.query(Permission).all()

            for permission in group.permissions:
                if permission not in permissions:
                    permissions.append(permission)

        return permissions
