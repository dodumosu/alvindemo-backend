# -*- coding: utf-8 -*-
from http import HTTPStatus

from flask import abort
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from .. import models, utils
from ..extensions import csrf
from ..transactions.schemas import TransactionSchema
from .schemas import MessageSchema

blueprint = Blueprint(
    "messages",
    __name__,
    url_prefix="/messages",
    description="Operations on messages",
)
csrf.exempt(blueprint)


@blueprint.route("/")
class MessageView(MethodView):
    @blueprint.arguments(MessageSchema)
    @blueprint.response(201, TransactionSchema)
    @blueprint.doc(**utils.doc_extras)
    @jwt_required()
    def post(self, new_data):
        email = get_jwt_identity()
        user = models.User.get_by_email(email)
        if not user:
            abort(HTTPStatus.UNAUTHORIZED)

        data = new_data.copy()
        if not data.get("sender"):
            data.update(sender=user.phone)

        message = models.Message.create(**data)
        result = utils.parse_message(message.body)
        if result is None:
            abort(HTTPStatus.BAD_REQUEST)

        transaction = models.Transaction.create(user=user, **result)

        return transaction
