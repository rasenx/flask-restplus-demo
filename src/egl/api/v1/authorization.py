from flask_login import login_required, current_user
from functools import wraps
from werkzeug.exceptions import Unauthorized

from egl.api.v1.services import AuthorizationService


def authorize(permission):
    """
    Requires the current user to be logged in (authenticted), as well as have the required permission assigned (authorized).
    """
    def decorator(f):
        @wraps(f)
        @@login_required()
        def wrapped(*args, **kwargs):
            if not AuthorizationService.has_permission(current_user, permission):
                raise Unauthorized()
            r = f(*args, **kwargs)
            return r
        return wrapped
    return decorator
