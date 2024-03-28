#!/usr/bin/env python3
from flask import session, Response
from flask_restful import Resource
import json
from asyncio import run
from db.users.read_users import db_get_user
from flask_setup import logger
from flasgger import swag_from


class AuthorizationCheck(Resource):
    @swag_from("endpoints_spec/authorization_check.yml")
    def get(self) -> json:
        try:
            session_email = session.get("email")
            if session_email is not None:
                response: dict = run(db_get_user(session_email))
                if response["valid"]:
                    return json.dumps(
                        {"user_role": response["data"]["role"]}), 200
                else:
                    return Response(
                        response=response["message"],
                        status=response["code"])
            else:
                return Response(response="Unauthorized access. Redirecting to login page..",
                                status=401)
        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)
