# -*- coding: utf-8 -*-
from http import HTTPStatus

from flask import Flask, jsonify


def _error_handler(error):
    code = getattr(error, "code", HTTPStatus.INTERNAL_SERVER_ERROR)
    response = {"status": "error"}
    match code:
        case HTTPStatus.BAD_REQUEST:
            response["message"] = HTTPStatus.BAD_REQUEST.description
        case HTTPStatus.UNAUTHORIZED:
            response[
                "message"
            ] = "You need authorization to access this resource"
        case HTTPStatus.FORBIDDEN:
            response["message"] = "You are not allowed to access this resource"
        case HTTPStatus.NOT_FOUND:
            response[
                "message"
            ] = "You requested a resource that could not be found"
        case HTTPStatus.INTERNAL_SERVER_ERROR:
            response[
                "message"
            ] = "There was a server error processing your request"

    return jsonify(response), code


def create_app(**override_settings) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(**override_settings)

    # set up error handlers
    known_error_statuses = [
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.UNAUTHORIZED,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.NOT_FOUND,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    ]
    for error_status in known_error_statuses:
        app.register_error_handler(error_status, _error_handler)

    return app
