# -*- coding: utf-8 -*-
from flask import Flask

from app.factory import create_app


def test_app_factory():
    # test basic app factory
    app = create_app()
    assert isinstance(app, Flask)

    # test override settings
    app = create_app(
        SOME_SETTING=1, SOME_OTHER_SETTING="somevalue", ONE_MORE_SETTING=True
    )
    assert app.config.get("SOME_SETTING") == 1
    assert app.config.get("SOME_OTHER_SETTING") == "somevalue"
    assert app.config.get("ONE_MORE_SETTING") is True
