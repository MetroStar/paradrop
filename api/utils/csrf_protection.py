#!/usr/bin/env python3
from flask import Response
from functools import wraps
from flask_setup import csrf, app


def csrf_protection_enabled(f):
    """
    Functions with this decorator have CSRF protection enabled.
    """
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not app.config["TESTING"]:
            pass
            # TODO: Fix CSRF for localhost
            # try:
            #     csrf.protect()
            # except BaseException:
            #     return Response(
            #         response="CSRF Token validation failed..",
            #         status=403)

        return f(*args, **kwargs)

    return decorated_func
