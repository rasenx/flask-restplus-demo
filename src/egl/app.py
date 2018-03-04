# #!/usr/bin/env python
import logging

from decouple import config
from egl.app_factory import app_factory

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

app = app_factory()


def main():
    host = config('FLASK_HOST', '0.0.0.0')
    port = config('FLASK_PORT', 5000, cast=int)
    debug = config('FLASK_DEBUG', True, cast=bool)
    use_reloader = config('FLASK_USE_RELOADER', True, cast=bool)
    app.run(host=host, port=port, debug=debug, use_debugger=debug, use_reloader=use_reloader)


if __name__ == '__main__':
    main()
