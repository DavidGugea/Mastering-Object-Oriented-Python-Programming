from flask import Flask, jsonify, request, url_for, Blueprint, current_app, abort, Response
from typing import Dict, Any, Tuple, List
from http import HTTPStatus
from Dice import Dice, make_dice
from dataclasses import asdict
from BadRequest import BadRequest
from AuthKeys import valid_api_key

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Blueprint.py",
        "version": "1.0",
        "description": "Rolls dice",
    },
    "paths": {
        "/rolls": {
            "post": {
                "description": "first roll",
                "responses": {201: {"description": "Created"}},
            },
            "get": {
                "description": "current state",
                "responses": {200: {"description": "Current state"}},
            },
            "patch": {
                "description": "subsequent roll",
                "responses": {200: {"description": "Updated"}},
            },
        }
    }
}
SESSIONS: Dict[str, Dice] = {}

rolls = Blueprint("rolls", __name__)


@rolls.route("/openapi.json")
def openapi() -> Response:
    return jsonify(OPENAPI_SPEC)


@rolls.route("/rolls", methods=["POST"])
def make_roll() -> tuple[Response, int, dict[str, str]]:
    body = request.get_json(force=True)
    if set(body.keys()) != {"dice"}:
        raise BadRequest()

    try:
        n_dice = int(body(["dice"]))
    except ValueError as ex:
        raise BadRequest()

    dice = make_dice(n_dice)
    SESSIONS[dice.identifier] = dice
    current_app.logger.info(f"Rolled roll={dice!r}")

    headers = {
        "Location": url_for("rolls.get_roll", identifier=dice.identifier)
    }

    return jsonify(asdict(dice)), HTTPStatus.CREATED, headers


@rolls.route("/rolls/<identifier>", methods=["GET"])
@valid_api_key
def get_roll(identifier) -> tuple[Response, int]:
    if identifier not in SESSIONS:
        abort(HTTPStatus.NOT_FOUND)

    return jsonify(asdict(SESSIONS[identifier])), HTTPStatus.OK


@rolls.route("/rolls/<identifier>", methods=["PATCH"])
def patch_roll(identifier) -> tuple[Response, int]:
    if identifier not in SESSIONS:
        abort(HTTPStatus.NOT_FOUND)

    body = request.get_json(force=True)
    if set(body.keys()) != {"keep"}:
        raise BadRequest(f"Extra fields in {body!r}")

    try:
        keep_positions = [int(d) for d in body["keep"]]
    except ValueError as ex:
        raise BadRequest(f"Bad 'keep' value in {body!r}")

    dice = SESSIONS[identifier]
    dice.reroll(keep_positions)

    return jsonify(asdict(dice)), HTTPStatus.OK
