from egl.api.v1 import Auditable
from egl.db.models import User
from egl.db.sessions import db


class SeedDataService(Auditable):

    def seed(self):
        self.add_users();

    def add_users(self):
        # seed some junk users to demo authn
        self.add_user('a1e121cc-76d8-45a1-a476-2936c6ba3278', 'genius@evilgeniuslabs.org', 'secret')
        self.add_user('99ddc422-d2d4-46a7-a236-929abeda9af9', 'minion@evilgeniuslabs.org', 'banana')

    def add_user(self, id, email, password):
        user = db.session.query(User).get(id)
        if user is None:
            user = User(id=id)
            db.session.add(user)

        user.email = email
        user.change_password(password)

        db.session.commit()

        password_valid = user.check_password(password)
        assert password_valid
