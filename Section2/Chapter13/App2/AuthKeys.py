from functools import wraps
from typing import Callable, Set
from pathlib import Path

from flask import request, current_app, abort
from http import HTTPStatus

VALID_API_KEYS: Set[str] = set()


def init_app(app):
    global VALID_API_KEYS
    if app.env == "development":
        VALID_API_KEYS = {"read-only", "admin", "write"}
    else:
        app.logger.info(f"Loading from {app.config['VALID_KEYS']}")

        raw_lines = (
            Path(
                app.config['VALID_KEYS']
                    .read_text()
                    .splitlines()
            )
        )

        VALID_API_KEYS = set(filter(None, raw_lines))


def valid_api_key(view_function: Callable) -> Callable:
    @wraps(view_function)
    def confirming_view_function(*args, **kwargs):
        api_key = request.headers.get('Api-Key')
        if api_key not in VALID_API_KEYS:
            current_app.logger.error(f"Rejectin Api-Key: {api_key!r}")
            abort(HTTPStatus.UNAUTHORIZED)

        return view_function(*args, **kwargs)

    return confirming_view_function()
