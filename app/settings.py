# -*- coding: utf-8 -*-
"""Application config module"""
import pathlib

from furl import furl
from prettyconf import config, loaders

project_root = pathlib.Path(__file__).parent.parent

config.loaders = [
    loaders.Environment(),
    loaders.EnvFile(filename=project_root.joinpath(".env")),
    loaders.IniFile(filename=project_root.joinpath("settings.ini")),
]

flask_env = config("FLASK_ENV", default=None)
DEBUG = flask_env == "development" or config(
    "DEBUG", cast=config.boolean, default=False
)
SECRET_KEY = config("SECRET_KEY")
TIME_ZONE = config("TIME_ZONE", default="UTC")
FORCE_HTTPS = config("FORCE_HTTPS", cast=config.boolean, default=True)

DATABASE_HOST = config("DATABASE_HOST", default="postgres")
DATABASE_PORT = config("DATABASE_PORT", cast=int, default=5432)
DATABASE_USER = config("DATABASE_USER", default="postgres")
DATABASE_PASSWORD = config("DATABASE_PASSWORD", default="postgres")
DATABASE_DB = config("DATABASE_DB", default="postgres")

db_uri = furl(
    scheme="postgresql",
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    username=DATABASE_USER,
    password=DATABASE_PASSWORD,
    path=DATABASE_DB,
)

SQLALCHEMY_DATABASE_URI = (
    config("DATABASE_URL", default=None).replace(
        "postgres://", "postgresql://"
    )
    or db_uri.url
)
SQLALCHEMY_ECHO = config("ECHO_SQL", cast=config.boolean, default=DEBUG)
SQLALCHEMY_ENGINE_OPTIONS = {
    "connect_args": {"options": "-c timezone=utc"},
    "pool_pre_ping": True,
}
SQLALCHEMY_TRACK_MODIFICATIONS = True

REDIS_HOST = config("REDIS_HOST", default="redis")
REDIS_PORT = config("REDIS_POST", cast=int, default=6379)
REDIS_USER = config("REDIS_USER", default="redis")
REDIS_PASSWORD = config("REDIS_PASSWORD", default="redis")
REDIS_DB = config("REDIS_DB", default="0")

redis_uri = furl(
    scheme="redis",
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USER,
    password=REDIS_PASSWORD,
    path=REDIS_DB,
)
REDIS_URL = config("REDIS_URL", default=None) or redis_uri.url

RATELIMIT_STORAGE_URI = REDIS_URL

SENTRY_DSN = config("SENTRY_DSN", default=None)

API_TITLE = "Transactions API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.2"
