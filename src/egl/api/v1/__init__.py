import logging

# NOTE: If you import Resource from flask_restplus_patched, you will get a default OPTIONS method for every GET method you implement.
# The swagger UI it exposes adds no value, so rather than monkey patching, just be careful what you import.
# Original Commit: https://github.com/frol/flask-restplus-server-example/commit/e17bde52a287afa984d6d7eab3f1a63e5c377efe
# --mark
from flask_restplus import Resource
from flask_restplus_patched import Api, reqparse


logger = logging.getLogger(__name__)
logger.setLevel('INFO')

api = Api(version='1',
          title='Flask Restplus Demo',
          description='REST APIs demonstrated by Evil Genius Labs.',
          )

paging_parameters = reqparse.RequestParser()
paging_parameters.add_argument('page', default=1, type=int, help='Current page')
paging_parameters.add_argument('per_page', default=25, type=int, help='Number of items per page')


class PagedResult:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
