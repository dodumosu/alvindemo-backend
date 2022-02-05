# -*- coding: utf-8 -*-
from uuid import uuid4


def make_identifier() -> str:
    return uuid4().hex
