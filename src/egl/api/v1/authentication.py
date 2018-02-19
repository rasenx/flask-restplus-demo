from flask import jsonify
from flask_login import login_required, current_user, logout_user, login_user
from flask_restplus import Resource
from flask_restplus_patched import Namespace
from werkzeug.exceptions import Unauthorized

from egl.api.v1.schemas import LoginSchema, UserSchema
from egl.db.models import User
from egl.db.sessions import db

ns = Namespace('Authentication')


@ns.route('/current')
class HomeResource(Resource):

    @login_required
    def get(self):
        return jsonify(current_user)


@ns.route('/login')
class UsersResource(Resource):

    @ns.parameters(LoginSchema(), locations=['json'])
    @ns.response(UserSchema())
    def post(self, login):
        user = db.session.query(User).filter(User.email == login.email).one_or_none()
        if user is None:
            raise Unauthorized()

        if user.check_password(login.password):
            login_user(user)
            return user

        return None


@ns.route('/logout')
class UsersResource(Resource):

    @login_required
    def post(self, paging):
        logout_user()
        return '', 204