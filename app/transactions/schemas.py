# -*- coding: utf-8 -*-
from typing import Union

import marshmallow as ma
from marshmallow import validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import func

from ..categories.models import Category
from ..extensions import db
from .models import Transaction

TRANSACTION_AGGREGATE_TYPES = ["average", "total", "max", "min", "count"]


class TransactionDetailSchema(ma.Schema):
    id = ma.fields.Integer(required=True)


class TransactionSchema(SQLAlchemyAutoSchema):
    category = ma.fields.Method("get_category", deserialize="load_category")

    class Meta:
        model = Transaction
        load_instance = True
        exclude = ("user",)
        sqla_session = db.session

    created = auto_field(dump_only=True)
    updated = auto_field(dump_only=True)

    def get_category(self, obj: Transaction) -> Union[str, None]:
        return obj.category.name if obj.category else None

    def load_category(self, value: Union[str, int]) -> Union[Category, None]:
        if value and isinstance(value, str):
            if not value.isdigit():
                return Category.query.filter(
                    func.lower(Category.name) == value.lower()
                ).first()
            else:
                return Category.query.filter(Category.id == int(value)).first()

        if value and isinstance(value, int):
            return Category.query.filter(Category.id == value).first()


class TransactionRangeSchema(ma.Schema):
    start = ma.fields.Date()
    end = ma.fields.Date()


class TransactionAggregateSchema(TransactionRangeSchema):
    operation = ma.fields.String(
        required=True, validate=validate.OneOf(TRANSACTION_AGGREGATE_TYPES)
    )
    category = ma.fields.Method(deserialize="load_category")

    def load_category(self, value: Union[str, int]) -> Union[Category, None]:
        if value and isinstance(value, str):
            return Category.query.filter(
                func.lower(Category.name) == value.lower()
            ).first()

        if value and isinstance(value, int):
            return Category.query.filter(Category.id == value).first()
