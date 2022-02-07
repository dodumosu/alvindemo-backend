# -*- coding: utf-8 -*-
from http import HTTPStatus

from flask import abort, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from sqlalchemy import func

from .. import models, utils
from ..extensions import csrf, db
from . import schemas

blueprint = Blueprint(
    "transactions",
    __name__,
    url_prefix="/transactions",
    description="Operations on transactions",
)
csrf.exempt(blueprint)


@blueprint.route("/")
class TransactionListView(MethodView):
    @blueprint.arguments(schemas.TransactionRangeSchema, location="query")
    @blueprint.response(200, schemas.TransactionSchema(many=True))
    @blueprint.doc(**utils.doc_extras)
    @blueprint.paginate(utils.CursorPage)
    @jwt_required()
    def get(self, filter_args=None):
        """Transaction list"""
        email = get_jwt_identity()
        user = models.User.get_by_email(email)
        if user is None:
            abort(HTTPStatus.UNAUTHORIZED)

        transactions = models.Transaction.query.filter(
            models.Transaction.user == user
        )
        if filter_args:
            args = []
            start_arg = filter_args.get("start")
            end_arg = filter_args.get("end")
            if start_arg:
                start = utils.convert_date(start_arg)
                args.append(models.Transaction.created >= start)
            if end_arg:
                end = utils.convert_date(end_arg, False)
                args.append(models.Transaction.created <= end)

            transactions = transactions.filter(*args)

        return transactions.order_by(models.Transaction.created)


@blueprint.route("/aggregate")
class TransactionAggregateView(MethodView):
    @blueprint.arguments(schemas.TransactionAggregateSchema, location="query")
    @blueprint.doc(**utils.doc_extras)
    @jwt_required()
    def get(self, filter_args):
        """Transaction aggregates"""
        email = get_jwt_identity()
        user = models.User.get_by_email(email)
        if user is None:
            abort(HTTPStatus.UNAUTHORIZED)

        transactions = models.Transaction.query.filter(
            models.Transaction.user == user
        )
        args = []
        start_arg = filter_args.get("start")
        end_arg = filter_args.get("end")
        if start_arg:
            start = utils.convert_date(start_arg)
            args.append(models.Transaction.created >= start)
        if end_arg:
            end = utils.convert_date(end_arg, False)
            args.append(models.Transaction.created <= end)

        transactions = transactions.filter(*args)
        category = filter_args.get("category")
        if category:
            transactions = transactions.filter(
                models.Transaction.category == category
            )

        operation = filter_args.get("operation")
        match operation.lower():
            case "average":
                function = func.avg
            case "total":
                function = func.sum
            case "min":
                function = func.min
            case "max":
                function = func.max
            case "count":
                function = func.count

        result = transactions.with_entities(
            function(models.Transaction.amount)
        ).scalar()
        return jsonify(result=result)


# @blueprint.route("/<int:id>")
# class TransactionDetailView(MethodView):
#     @blueprint.arguments(
#         schemas.TransactionDetailSchema, as_kwargs=True, location="path"
#     )
#     @blueprint.response(200, schemas.TransactionSchema)
#     @blueprint.doc(**utils.doc_extras)
#     @jwt_required()
#     def get(self, **kwargs):
#         """Transaction details"""
#         email = get_jwt_identity()
#         id = kwargs.get("id")
#         user = models.User.get_by_email(email)
#         if not user:
#             abort(HTTPStatus.UNAUTHORIZED)

#         transaction = models.Transaction.query.filter(
#             models.Transaction.user == user,
#             models.Transaction.id == id,
#         ).first()

#         if transaction is None:
#             abort(HTTPStatus.NOT_FOUND)

#         return transaction

#     @blueprint.arguments(
#         schemas.TransactionDetailSchema, as_kwargs=True, location="path"
#     )
#     @blueprint.arguments(
#         schemas.TransactionSchema(only=("category",)), as_kwargs=True
#     )
#     @blueprint.response(200, schemas.TransactionSchema)
#     @blueprint.doc(**utils.doc_extras)
#     @jwt_required()
#     def put(self, **kwargs):
#         """Transaction update"""
#         email = get_jwt_identity()
#         user = models.User.get_by_email(email)
#         if not user:
#             abort(HTTPStatus.UNAUTHORIZED)

#         transaction = models.Transaction.query.filter(
#             models.Transaction.user == user,
#             models.Transaction.id == transaction_data.id,
#         ).first()

#         if transaction is None:
#             abort(HTTPStatus.NOT_FOUND)

#         # only update the category
#         transaction.category = transaction_data.category
#         transaction.save()

#         return models.Transaction.query.filter(
#             models.Transaction.user == user
#         ).first()


@blueprint.route("/<int:id>", methods=["GET", "PUT"])
@blueprint.response(200, schemas.TransactionSchema)
@blueprint.doc(**utils.doc_extras)
@jwt_required()
def transaction_detail_or_update(id: int):
    email = get_jwt_identity()
    user = models.User.get_by_email(email)
    if user is None:
        abort(HTTPStatus.UNAUTHORIZED)

    transaction = models.Transaction.query.filter(
        models.Transaction.user == user,
        models.Transaction.id == id,
    ).first()

    if transaction is None:
        abort(HTTPStatus.NOT_FOUND)

    if request.method == "GET":
        return transaction

    if request.method == "PUT":
        request_data = request.get_json()
        s = schemas.TransactionSchema(only=("category",))
        try:
            result = s.load(request_data)
        except Exception as ex:
            print(ex)
            abort(HTTPStatus.BAD_REQUEST)

        category = result.category
        transaction.category = category

        # necessary because the result is bound to the session
        db.session.expunge(result)
        transaction.save()

        return transaction
