# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 I-Form Advanced Manufacturing Research Centre.
#
# invenio-config-iform is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""A script for testing sphinx documentation building."""

from sphinx.cmd.build import main as build_docs


def main() -> None:
    """Attempt to build documentation."""
    build_docs(["-nN", "docs", "docs/_build/html"])
    build_docs(["-nN", "-b", "doctest", "docs", "docs/_build/doctest"])
