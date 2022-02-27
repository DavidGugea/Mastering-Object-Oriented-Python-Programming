import random

from dataclasses import dataclass, asdict, astuple
from typing import List, Dict, Any, Tuple, NamedTuple

from flask import Flask, jsonify, abort, Response
from http import HTTPStatus

from Domino import Domino
from Boneyard import Boneyard

app = Flask(__name__)

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "description": "Deals simple hands of dominoes",
        "version": "2019.02",
        "title": "Test Title"
    },
    "paths": {}
}


@app.route("/dominoes/<n>")
def dominoes(n: str) -> tuple[Response, int]:
    try:
        hand_size = int(n)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST)

    if app.env == "development":
        random.seed(2)

    b = Boneyard(limit=6)
    hand_0 = b.deal(hand_size)[0]
    app.logger.info("Send %r", hand_0)

    return jsonify(status="OK", dominoes=[astuple(d) for d in hand_0]), HTTPStatus.OK


@app.route("/hands/<int:h>/dominoes/<int:c>")
def hands(h: int, c: int) -> tuple[Response, int]:
    if h == 0 or c == 0:
        return jsonify(
            status="Bad Request",
            error=[f"hands={h!r}, dominoes={c!r} is invalid"]
        ), HTTPStatus.BAD_REQUEST

    if app.env == "development":
        random.seed(2)

    b = Boneyard(limit=6)
    try:
        hand_list = b.deal(c, h)
    except ValueError as ex:
        return jsonify(
            status="Bad Request",
            error=ex.args
        ), HTTPStatus.BAD_REQUEST

    app.logger.info("Send %r", hand_list)

    return jsonify(
        status="OK",
        dominoes=[[astuple(d) for d in hand] for hand in hand_list]
    ), HTTPStatus.OK


@app.route("/openapi.json")
def openapi() -> Response:
    """
    >>> client = app.test_client()
    >>> response = client.get("openapi.json")
    >>> response.get_json()['openapi']
    '3.0.0'
    >>> response.get_json()['info']['title']
    'Test Title'
    """

    return jsonify(OPENAPI_SPEC)