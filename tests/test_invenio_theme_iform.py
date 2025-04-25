# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Graz University of Technology.
#
# invenio-theme-iform is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask

from invenio_theme_iform import InvenioThemeIform


def test_version():
    """Test version import."""
    from invenio_theme_iform import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioThemeIform(app)
    assert "invenio-theme-iform" in app.extensions

    app = Flask("testapp")
    ext = InvenioThemeIform()
    assert "invenio-theme-iform" not in app.extensions
    ext.init_app(app)
    assert "invenio-theme-iform" in app.extensions


def test_app(app):
    """Test extension initialization."""
    _ = InvenioThemeIform(app)
