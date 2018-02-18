import logging
import os
from datetime import datetime, date
from decimal import Decimal
from json import JSONEncoder
from uuid import UUID

from decouple import config
from flask import Blueprint, Flask, jsonify
from flask_marshmallow import Marshmallow
from requests import RequestException
from werkzeug.contrib.fixers import ProxyFix

from egl.api.v1 import api
from egl.db.sessions import db

logger = logging.getLogger(__name__)
logger.setLevel('INFO')


_encoder_default = JSONEncoder.default


def _better_encoder_default(self, o):
    if isinstance(o, Decimal) or isinstance(o, UUID):
        return str(o)

    if isinstance(o, datetime) or isinstance(o, date):
        return o.isoformat()

    return _encoder_default(self, o)


JSONEncoder.default = _better_encoder_default


def app_factory():
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if os.environ.get('PROJECT_ROOT', None) is None:
        os.environ['PROJECT_ROOT'] = project_root

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    Marshmallow(app)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.url_map.strict_slashes = False

    blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    app.register_blueprint(blueprint)

    @app.after_request
    def after_request(response):
        if 'cache-control' not in response.headers:
            response.headers['cache-control'] = 'no-cache'
        return response

    @api.errorhandler
    def default_error_handler(e):
        """
        Provide a default error handler for RestPlus to leverage.
        """
        logger.exception(e)
        debug = config.get('FLASK_DEBUG')
        if not debug:
            message = 'An unhandled exception occurred.'
            return {'message': message}, 500

    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify(error=400, text=str(e)), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error=404, text=str(e)), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error(e)
        return jsonify(error=500, text=str(e)), 500

    @app.errorhandler(RequestException)
    def request_exception(e):
        logger.error(e)
        return jsonify(error=500, text=str(e)), 500

    return app
