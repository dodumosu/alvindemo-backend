# -*- coding: utf-8 -*-
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from .models import Category


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

    id = auto_field(dump_only=True)
    created = auto_field(dump_only=True)
    updated = auto_field(dump_only=True)
