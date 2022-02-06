# -*- coding: utf-8 -*-
from datetime import timedelta
from http import HTTPStatus

from flask import abort, jsonify
from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint

from ..extensions import csrf
from ..models import User
from .schemas import UserLoginSchema

blueprint = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    description="Authentication operations",
)
csrf.exempt(blueprint)


@blueprint.route("/login", methods=["POST"])
@blueprint.arguments(UserLoginSchema)
def login(credentials):
    user = User.get_by_email(credentials.get("username"))
    if not user:
        abort(HTTPStatus.UNAUTHORIZED)

    if not user.verify_and_update_password(credentials.get("password")):
        abort(HTTPStatus.UNAUTHORIZED)

    access_token = create_access_token(
        identity=user.email, expires_delta=timedelta(hours=24)
    )
    return jsonify(access_token=access_token)
