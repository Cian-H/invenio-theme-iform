# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2025 Graz University of Technology.
#
# invenio-theme-iform is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for I-Form theme."""

import traceback
from functools import wraps
from typing import Dict

from flask import Blueprint, Flask, current_app, g, redirect, render_template, url_for
from flask_login import current_user, login_required
from invenio_rdm_records.proxies import current_rdm_records
from invenio_records_global_search.resources.serializers import (
    GlobalSearchJSONSerializer,
)
from invenio_users_resources.proxies import current_user_resources
from opensearch_dsl.utils import AttrDict

from .search import FrontpageRecordsSearch


def create_blueprint(app: Flask) -> Blueprint:
    """Create blueprint."""
    blueprint = Blueprint(
        "invenio_theme_iform",
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    routes = app.config.get("THEME_IFORM_ROUTES")

    blueprint.add_url_rule(routes["records-search"], view_func=records_search)
    blueprint.add_url_rule(routes["index"], view_func=index)
    blueprint.add_url_rule(routes["overview"], view_func=overview)

    # base case for any otherwise unhandled exception
    app.register_error_handler(Exception, default_error_handler)

    blueprint.add_app_template_filter(make_dict_like)
    blueprint.add_app_template_filter(cast_to_dict)

    return blueprint


def records_search():
    """Search page ui.

    With this route it is possible to override the default route
    "/search" to get to the rdm-records search. The default route will
    be overriden by the global search with changing the
    SEARCH_UI_SEARCH_TEMPLATE variable to the value
    "invenio_records_global_search/search/search.html" in the
    invenio.cfg file.
    """
    return render_template("invenio_app_rdm/records/search.html")


def current_identity_is_iform_authenticated() -> bool:
    """Checks whether current identity has iform-authentication.

    NOTE: Default permission-policy has no field for `iform_authenticated`.
    Should the field not exist, the service checks against admin-permissions instead.
    You probably meant to configure a custom permission-policy.
    """
    rdm_service = current_rdm_records.records_service
    return rdm_service.check_permission(g.identity, "iform_authenticated")


def require_iform_authenticated(view_func):
    """Decorator for guarding view-functions against unauthenticated users.

    Redirects un-authenticated users to their personal dashboard's overview.
    """

    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_identity_is_iform_authenticated():
            return redirect(url_for("invenio_theme_iform.overview"))
        return view_func(*args, **kwargs)

    return decorated_view


@login_required
def overview():
    """Overview."""
    url = current_user_resources.users_service.links_item_tpl.expand(g.identity, current_user)[
        "avatar"
    ]
    is_iform_authenticated = current_identity_is_iform_authenticated()
    return render_template(
        "invenio_theme_iform/overview.html",
        is_iform_authenticated=is_iform_authenticated,
        user_avatar=url,
    )


def make_dict_like(value: str, key: str) -> Dict[str, str]:
    """Convert the value to a dict like structure.

    in the form of a key -> value pair.
    """
    return {key: value}


def cast_to_dict(attr_dict):
    """Return the dict structure of AttrDict variable."""
    return AttrDict.to_dict(attr_dict)


def default_error_handler(e: Exception):
    """Called when an otherwise unhandled error occurs."""
    # TODO: use sentry here once it's configured
    # information we might want to log for debugging the error:
    #   - `flask.request`, a proxy to the current http-request in which the error occured
    #   - `flask.session`, a proxy to the current http-session
    #   - `e`, the passed-in exception
    # to get proxied-to objects: `flask.request._get_current_object()`

    msg = f"default_error_handler of invenio-theme-iform captured following error type: {
        type(e)
    } with message {e} and stack trace {traceback.format_exc()}"
    current_app.logger.error(msg)
    return render_template(current_app.config["THEME_500_TEMPLATE"]), 500


def records_serializer(records=None):
    """Serialize list of records."""
    serializer = GlobalSearchJSONSerializer()
    return [serializer.dump_obj(r.to_dict()) for r in records]


def index():
    """Frontpage."""
    records = FrontpageRecordsSearch()[:5].sort("-created").execute()

    return render_template("invenio_theme_iform/index.html", records=records_serializer(records))


def locked(e):
    """Error page for status locked."""
    return render_template("invenio_theme_iform/423.html")
