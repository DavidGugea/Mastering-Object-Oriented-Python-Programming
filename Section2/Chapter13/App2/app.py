from flask import Flask, jsonify, request, url_for, Blueprint, current_app, abort, Response
from typing import Dict, Any, Tuple, List
from http import HTTPStatus
from BadRequest import BadRequest
from Blueprint import rolls


def make_app() -> Flask:
    app = Flask(__name__)

    @app.errorhandler(BadRequest)
    def error_message(ex) -> tuple[Response, int]:
        current_app.logger.info(f"{ex.args}")
        return jsonify(status="Bad Request", message=ex.args), HTTPStatus.BAD_REQUEST

    app.register_blueprint(rolls)

    return app
