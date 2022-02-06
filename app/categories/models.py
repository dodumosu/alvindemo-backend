# -*- coding: utf-8 -*-
import sqlalchemy as sa

from ..db.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = sa.Column(sa.String, nullable=False, unique=True)
