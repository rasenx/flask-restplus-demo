from flask_restplus import Resource
from flask_restplus_patched import Namespace

from egl.api.v1.schemas import PagingParametersSchema, UserPageSchema
from egl.api.v1.services import UserService

ns = Namespace('Users')


@ns.route('/')
class UsersResource(Resource):

    @ns.parameters(PagingParametersSchema(), locations=['query'])
    @ns.response(UserPageSchema())
    def get(self, paging):
        service = UserService()
        return service.get_users(paging.page, paging.per_page)

    # @ns.parameters(NewUserSchema(), locations=['json'])
    # @ns.response(UserSchema(), code=201)
    # def post(self, validated):
    #     service = UserService()
    #     return service.create(validated)
