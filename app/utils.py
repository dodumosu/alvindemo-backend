# -*- coding: utf-8 -*-
import decimal
import re
from datetime import date, datetime, time
from typing import Union
from uuid import uuid4

from dateutil.tz import gettz
from flask_smorest.pagination import Page

from .settings import CURRENCY, TIME_ZONE

default_flags = re.I | re.MULTILINE
amount_regex = re.compile(
    rf"Amount:\s+{CURRENCY}\s+(?P<amount>\d*[.,]?\d*).*", flags=default_flags
)
description_regex = re.compile(r"Description:\s+", flags=default_flags)


def make_identifier() -> str:
    return uuid4().hex


doc_extras = {
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    "security": [{"bearerAuth": []}],
}


def convert_date(dt: date, use_lower=True) -> datetime:
    app_tzinfo = gettz(TIME_ZONE)
    tm = time.min if use_lower else time.max

    return datetime.combine(dt, tm, app_tzinfo)


class CursorPage(Page):
    @property
    def item_count(self):
        return self.collection.count()


def parse_message(body: str) -> Union[dict, None]:
    """
    Parses a message body for transaction details

    A sample message body is below:
    Amount: NGN 10.00
    Description: Bank charges
    """
    # process amount
    amount_match = re.search(amount_regex, body)
    amount = (
        decimal.Decimal(amount_match.group("amount")) if amount_match else None
    )

    # process description
    description_match = re.search(description_regex, body)
    if description_match:
        description = (
            body[description_match.span()[1]:].strip().split("\n")[0]
        )
    else:
        description = None

    if amount is not None and description is not None:
        return {"amount": amount, "description": description}
