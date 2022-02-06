# -*- coding: utf-8 -*-
from typing import Union

import marshmallow as ma
from marshmallow import validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import func

from ..categories.models import Category
from .models import Transaction

TRANSACTION_AGGREGATE_TYPES = ["average", "total", "max", "min", "count"]


class TransactionSchema(SQLAlchemyAutoSchema):
    category = ma.fields.Method("get_category", deserialize="load_category")

    class Meta:
        model = Transaction
        load_instance = True
        exclude = ("user",)

    id = auto_field(dump_only=True)
    created = auto_field(dump_only=True)
    updated = auto_field(dump_only=True)

    def get_category(self, obj: Transaction) -> Union[str, None]:
        return obj.category.name if obj.category else None

    def load_category(self, value: str) -> Union[Category, None]:
        if value:
            return Category.query.filter(
                func.lower(Category.name) == value.lower()
            ).first()


class TransactionRangeSchema(ma.Schema):
    start = ma.fields.Date()
    end = ma.fields.Date()


class TransactionAggregateSchema(TransactionRangeSchema):
    operation = ma.fields.String(
        required=True, validate=validate.OneOf(TRANSACTION_AGGREGATE_TYPES)
    )
    category = ma.fields.String()
