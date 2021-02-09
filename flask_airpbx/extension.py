#
# Flask-Airpbx
#
# Copyright (C) 2021 Airpbx Ltd
# All rights reserved
#


import logging

from flask import (
    Blueprint,
    Flask,
    Response,
    current_app,
    jsonify,
    request,
    url_for,
)

from .signals import namespace


logger = logging.getLogger('Flask-Airpbx')


class Airpbx(object):
    """"""

    def __init__(self, app: Flask = None, *, url_prefix: str = None) -> None:
        if app is not None:
            self.init_app(app, url_prefix=url_prefix)

    def init_app(self, app: Flask, *, url_prefix: str = None) -> None:
        app.add_url_rule('/manifest', 'manifest', self._manifest)
        blueprint = Blueprint(__package__, __name__, url_prefix=url_prefix)
        blueprint.add_url_rule('/hooks', 'hooks', self._handle_webhook, methods=('POST',))
        app.register_blueprint(blueprint)

    def _handle_webhook(self) -> Response:
        event = request.get_json()
        namespace.signal(event['type']).send(self, event=event)
        return Response(status=201)

    @staticmethod
    def _manifest() -> Response:
        config = current_app.config
        return jsonify(
            id=config['AIRPBX_ID'],
            name=config['AIRPBX_NAME'],
            version=config['AIRPBX_VERSION'],
            services=config['AIRPBX_SERVICES'],
            logo=url_for('static', filename=config['AIRPBX_LOGO'], _external=True),
            connect_uri=url_for(config['AIRPBX_CONNECT_ENDPOINT'], _external=True),
            setup_uri=url_for(config['AIRPBX_SETUP_ENDPOINT'], _external=True),
        )


# EOF
