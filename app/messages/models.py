# -*- coding: utf-8 -*-
import sqlalchemy as sa

from ..db.base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    sender = sa.Column(sa.String, nullable=False)
    body = sa.Column(sa.String, nullable=False)
