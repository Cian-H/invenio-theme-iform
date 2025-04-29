# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 I-Form Advanced Manufacturing Research Centre.
#
# invenio-config-iform is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Run all tests for this module consecutively."""

import pytest

from . import test_docs


def main() -> None:
    """Run tests for this module."""
    test_docs.main()
    pytest.console_main()
