# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.orm import backref, relationship

from ..db.base import BaseModel


class Transaction(BaseModel):
    __tablename__ = "transactions"

    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    amount = sa.Column(sa.DECIMAL, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    category_id = sa.Column(
        sa.Integer, sa.ForeignKey("categories.id", ondelete="SET NULL")
    )

    user = relationship("User", backref=backref("transactions"))
    category = relationship("Category", backref=backref("transactions"))
