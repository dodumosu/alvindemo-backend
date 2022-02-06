# -*- coding: utf-8 -*-
import decimal

from app.settings import CURRENCY
from app.utils import parse_message


def test_message_parsing():
    sample_text1 = f'''amount: {CURRENCY} 5 description: stash'''
    result = parse_message(sample_text1)

    assert result is not None
    assert result.get('amount') == decimal.Decimal(5)
    assert result.get('description') == 'stash'

    sample_text2 = f'''
    description: rounding error
    amount: {CURRENCY} .5


    '''
    result = parse_message(sample_text2)
    assert result is not None
    assert result.get('amount') == decimal.Decimal(0.5)
    assert result.get('description') == 'rounding error'
