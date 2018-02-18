from egl.db.models.user import User
from egl.db.sessions import db


class UserService:

    def get_users(self, page, per_page):
        return db.session.query(User).paginate(page, per_page, False)

    def create(self, dto):
        pass

    def update(self, dto):
        pass

    def delete(self, user_id):
        pass