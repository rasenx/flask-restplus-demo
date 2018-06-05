import logging

from egl.api.v1 import Auditable
from egl.api.v1.defaults import Users, UserGroups, Permissions
from egl.db.models import User, UserGroup, Permission
from egl.db.sessions import db


class SeedDataService(Auditable):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def seed(self):
        self.seed_user(Users.root)
        self.seed_user(Users.admin)
        self.seed_user(Users.minion)

        self.seed_group(UserGroups.superusers)
        self.seed_group(UserGroups.admins)

        self.seed_permission(Permissions.view_users)
        self.seed_permission(Permissions.view_user_groups)

        self.seed_permission(Permissions.modify_users)
        self.seed_permission(Permissions.modify_user_groups)
        self.seed_permission(Permissions.modify_permissions)

        db.session.commit()

    def seed_user(self, user: User) -> User:
        existing = db.session.query(User).get(user.id).first()
        if not existing:
            existing = db.session.query(User).filter(User.email == user.email).first()
            if not existing:
                existing = user
                db.session.add(existing)
                self.logger.info('Adding user: {}'.format(existing))

        existing.email = user.email
        existing.password = user.password
        existing.meta = user.meta
        existing.active = user.active
        return existing

    def seed_group(self, group: UserGroup) -> UserGroup:
        existing = db.session.query(UserGroup).get(group.id).first()
        if not existing:
            existing = group
            db.session.add(existing)
            self.logger.info('Adding group: {}'.format(existing))

        existing.name = group.name
        existing.is_system_group = group.is_system_group
        existing.parent_id = group.parent_id
        return existing

    def seed_permission(self, permission: Permission) -> Permission:
        existing = db.session.query(Permission).get(permission.id).first()
        if not existing:
            existing = permission
            db.session.add(existing)
            self.logger.info('Adding permission: {}'.format(existing))

        existing.name = permission.name
        return existing

    def seed_group_permission(self, group: UserGroup, permission: Permission):
        if permission not in group.permissions:
            group.permissions.append(permission)
            self.logger.info('Adding permission: {} to group: {}'.format(permission, group))

    def seed_group_member(self, group: UserGroup, user: User):
        if user not in group.members:
            group.members.append(user)
            self.logger.info('Adding user: {} to group: {}'.format(user, group))
