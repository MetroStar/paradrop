#!/usr/bin/env python3
from flask import session, request, Response
from functools import wraps
from asyncio import run
from db.users.read_users import db_get_user, db_get_user_token


def user_api(f):
    """
    Functions with this decorator can be used only by
    users with read-only and admin rights.
    """
    @wraps(f)
    def decorated_func(*args, **kwargs):

        # USER TOKEN AUTH
        # Check if auth_token and auth_email attributes are present in the
        # header
        auth_token = request.headers.get("X-Paradrop-Token")
        auth_email = request.headers.get("X-Paradrop-Email")
        if auth_token and auth_email:

            # If they are, compare token binded to the email and token from
            # header
            response: dict = run(db_get_user_token(auth_email))
            if response["valid"]:
                if response["data"]["token"] == auth_token:
                    return f(*args, **kwargs)
                else:
                    return Response(
                        response="Specified user token is invalid.",
                        status=400)
            else:
                return Response(
                    response="There is no user token binded to specified email.",
                    status=400)

        # SESSION COOKIES AUTH
        if session.get("email") is not None:
            return f(*args, **kwargs)
        else:
            return Response(
                response="You have to login to access this endpoint..",
                status=401)

    return decorated_func


def admin_api(f):
    """
    Functions with this decorator can be used only by
    users with admin rights.
    """
    @wraps(f)
    def decorated_func(*args, **kwargs):

        # USER TOKEN AUTH
        # Check if auth_token and auth_email attributes are present in the
        # header
        auth_token = request.headers.get("X-Paradrop-Token")
        auth_email = request.headers.get("X-Paradrop-Email")
        if auth_token and auth_email:
            # If they are, compare token binded to the email and token from
            # header
            response: dict = run(db_get_user_token(auth_email))
            if response["valid"]:
                if response["data"]["token"] == auth_token:
                    # Check the role of the user
                    if response["data"]["role"] == "admin":
                        return f(*args, **kwargs)
                    else:
                        return Response(
                            response="You have to have admin rights to access this endpoint..",
                            status=403)
                else:
                    return Response(
                        response="Specified user token is invalid.",
                        status=400)
            else:
                return Response(
                    response="There is no user token binded to specified email.",
                    status=400)

        # SESSION COOKIES AUTH
        session_email = session.get("email")
        if session_email is not None:
            response: dict = run(db_get_user(session_email))
            if response["valid"]:
                user_role = response["data"]["role"]
                if user_role == "admin":
                    return f(*args, **kwargs)
                else:
                    return Response(
                        response="You have to have admin rights to access this endpoint..",
                        status=403)
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        else:
            return Response(
                response="You have to login to access this endpoint..",
                status=401)

    return decorated_func
