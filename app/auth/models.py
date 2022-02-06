# -*- coding: utf-8 -*-
import sqlalchemy as sa
from flask_security import RoleMixin, UserMixin
from flask_security.utils import hash_password

from ..db.base import BaseModel
from ..extensions import db
from ..utils import make_identifier

roles_users = db.Table(
    "roles_users",
    sa.Column(
        "role_id",
        sa.Integer,
        sa.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "user_id",
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Role(BaseModel, RoleMixin):
    __tablename__ = "roles"

    name = sa.Column(sa.String, nullable=False, unique=True)
    description = sa.Column(sa.String)


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    email = sa.Column(sa.String, nullable=False, unique=True)
    username = sa.Column(sa.String, nullable=True, unique=True)
    password = sa.Column(sa.String, nullable=False)
    last_login_at = sa.Column(sa.DateTime)
    current_login_at = sa.Column(sa.DateTime)
    last_login_ip = sa.Column(sa.String)
    current_login_ip = sa.Column(sa.String)
    login_count = sa.Column(sa.Integer)
    active = sa.Column(sa.Boolean, default=True)
    confirmed_at = sa.Column(sa.DateTime)
    fs_uniquifier = sa.Column(
        sa.String, default=make_identifier, nullable=False, unique=True
    )
    phone = sa.Column(sa.String, nullable=False, unique=True)

    roles = sa.orm.relationship(
        "Role",
        secondary="roles_users",
        backref=sa.orm.backref("users", lazy="dynamic"),
    )

    @classmethod
    def get_by_phone(cls, phone: str):
        return cls.query.filter(cls.phone == phone).first()

    @classmethod
    def get_by_email(cls, email: str):
        return cls.query.filter(cls.email == email).first()

    def set_password(self, plaintext_password: str) -> None:
        self.password = hash_password(plaintext_password)
