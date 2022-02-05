# -*- coding: utf-8 -*-
import logging
from http import HTTPStatus

import sentry_sdk
import structlog
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from . import extensions, loggers, settings


def configure_logging(app: Flask, logger_name: str = "gunicorn.error") -> None:
    gunicorn_logger = logging.getLogger(logger_name)
    app.logger.handlers = gunicorn_logger.handlers[:]

    structlog.configure(
        processors=[
            loggers.add_app_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="%Y-%m-%dT%H:%M:%S.%f%z"),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def handle_error(error):
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


def configure_error_handling(app: Flask) -> None:
    known_error_statuses = [
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.UNAUTHORIZED,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.NOT_FOUND,
        HTTPStatus.INTERNAL_SERVER_ERROR,
    ]
    for error_status in known_error_statuses:
        app.register_error_handler(error_status, handle_error)


def configure_error_logging() -> None:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()],
        traces_sample_rate=1.0,
    )


def initialize_extensions(app: Flask) -> None:
    force_https = not app.config.get("DEBUG") and app.config.get("FORCE_HTTPS")

    extensions.cors.init_app(app)
    extensions.csrf.init_app(app)
    extensions.db.init_app(app)
    extensions.jwt_manager.init_app(app)
    extensions.limiter.init_app(app)
    extensions.talisman.init_app(app, force_https=force_https)


def create_app(**override_settings) -> Flask:
    configure_error_logging()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings)
    app.config.from_mapping(**override_settings)

    initialize_extensions(app)

    configure_error_handling(app)
    configure_logging(app)

    return app
