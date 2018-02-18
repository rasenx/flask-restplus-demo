import uuid

from flask_restplus_patched import Parameters, ModelSchema
from marshmallow import fields, post_load

from egl.db.models import User


###############################################################################
# Pagination
###############################################################################


class Page:
    def __init__(self, **kwargs):
        self.page = kwargs.get('page', 1)
        self.per_page = kwargs.get('per_page', 25)
        self.total = kwargs.get('total', 0)


class PageItems(Page):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = kwargs.get('items', {})


class PageSchema(Parameters):
    page = fields.Int(required=False, default=1, missing=1, example=1)
    per_page = fields.Int(required=False, default=25, missing=25, example=25)
    total = fields.Int(required=False, default=0, missing=0, example=0)

    @post_load
    def deserialize(self, data):
        return Page(**data)


class PagingParameters:
    def __init__(self, page=1, per_page=25):
        self.page = page
        self.per_page = per_page


class PagingParametersSchema(Parameters):
    page = fields.Int(required=False, default=1, missing=1, example=1)
    per_page = fields.Int(required=False, default=25, missing=25, example=25)

    @post_load
    def deserialize(self, data):
        return PagingParameters(**data)

###############################################################################
# Users
###############################################################################


class UserSchema(ModelSchema):
    class Meta:
        model = User
        strict = True


class UserPageSchema(PageSchema):
    items = fields.Nested(UserSchema, many=True)

    @post_load
    def deserialize(self, data):
        return PageItems(**data)