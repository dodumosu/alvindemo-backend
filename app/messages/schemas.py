# -*- coding: utf-8 -*-
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from .models import Message


class MessageSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Message

    id = auto_field(dump_only=True)
    created = auto_field(dump_only=True)
    updated = auto_field(dump_only=True)
    sender = auto_field("sender", required=False)
