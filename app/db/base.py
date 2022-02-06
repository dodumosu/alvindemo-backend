# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr

from ..extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    @declared_attr
    def id(self):
        return sa.Column(
            sa.Integer, autoincrement=True, nullable=False, primary_key=True
        )

    @declared_attr
    def created(self):
        return sa.Column(
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("timezone('utc', now())"),
        )

    @declared_attr
    def updated(self):
        return sa.Column(
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("timezone('utc', now())"),
            server_onupdate=sa.text("timezone('utc', now())"),
        )

    @classmethod
    def new(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        instance = cls.new(**kwargs)

        instance.save()
        return instance

    def save(self):
        db.session.add(self)
        db.session.commit()
