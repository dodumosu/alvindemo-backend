# -*- coding: utf-8 -*-
import marshmallow as ma


class UserLoginSchema(ma.Schema):
    username = ma.fields.String(required=True)
    password = ma.fields.String(required=True)
