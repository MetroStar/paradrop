#!/usr/bin/env python3
from flask import session, Response, request
from flask_restful import Resource
from asyncio import run
# from flask_wtf.csrf import generate_csrf
import uuid
import json
from flask_setup import logger
from flasgger import swag_from
from api_auth import admin_api, user_api
from db.users.read_users import db_get_user
from db.agent_token import db_get_agent_token, db_update_agent_token
from db.user_tokens import db_add_user_token, db_get_user_token, db_update_user_token


def is_valid_uuid(token):
    """
    Function to check if token is a valid UUID.
    """
    try:
        uuid.UUID(str(token))
        return True
    except ValueError:
        return False


class AddUserToken(Resource):
    @admin_api
    @swag_from("endpoints_spec/add_user_token.yml")
    def post(self) -> json:
        try:
            request_body: dict = request.json
            if "email" in request_body:
                user_data: dict = run(db_get_user(request_body["email"]))
                if user_data["valid"]:
                    user_token: str = ""

                    # If there is a custom token in the request body,
                    # check if token is a valid UUID token.
                    if "token" in request_body:
                        if request_body["token"]:
                            if is_valid_uuid(request_body["token"]):
                                user_token = request_body["token"]
                            else:
                                return Response(response="Token specified in request body is not valid UUID..",
                                                status=400)

                    response: dict = run(
                        db_add_user_token(
                            user_data["data"]["email"],
                            user_data["data"]["role"],
                            user_token))
                    return Response(
                        response=response["message"],
                        status=response["code"])
                else:
                    return Response(
                        response=user_data["message"],
                        status=user_data["code"])
            else:
                return Response(response="Required data are missing..",
                                status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=500)


class GetUserToken(Resource):
    @user_api
    @swag_from("endpoints_spec/get_user_token.yml")
    def get(self) -> json:
        try:
            session_email: str = session.get("email")
            response: dict = run(db_get_user_token(session_email))
            if response["valid"]:
                return json.dumps({"user_auth_token": response["data"]}), 200
            else:
                return json.dumps({"user_auth_token": ""}), 404

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=500)


class UpdateUserToken(Resource):
    @user_api
    @swag_from("endpoints_spec/update_user_token.yml")
    def post(self) -> json:
        try:
            session_email: str = session.get("email")
            user_data: dict = run(db_get_user(session_email))
            if user_data["valid"]:
                response: dict = run(
                    db_update_user_token(
                        session_email,
                        user_data["data"]["role"]))
                return Response(
                    response=response["message"],
                    status=response["code"])
            else:
                return Response(
                    response=user_data["message"],
                    status=user_data["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=500)


class GetAgentToken(Resource):
    @admin_api
    @swag_from("endpoints_spec/get_agent_token.yml")
    def get(self) -> json:
        try:
            response: dict = run(db_get_agent_token())
            if response["valid"]:
                return json.dumps({"agent_auth_token": response["data"]}), 200
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=500)


class UpdateAgentToken(Resource):
    @admin_api
    @swag_from("endpoints_spec/update_agent_token.yml")
    def post(self) -> json:
        try:
            user_defined_token: str = ""
            request_body: dict = request.json
            if "custom_agent_token" in request_body:
                if request_body["custom_agent_token"]:
                    if is_valid_uuid(request_body["custom_agent_token"]):
                        user_defined_token: str = request_body["custom_agent_token"]
                    else:
                        return Response(response="Token specified in request body is not valid UUID..",
                                        status=400)

            response: dict = run(db_update_agent_token(user_defined_token))
            return Response(
                response=response["message"],
                status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=500)


class GetCsrfToken(Resource):
    @swag_from("endpoints_spec/get_csrf_token.yml")
    def get(self) -> json:
        try:
            # token: str = generate_csrf()
            return json.dumps({"csrf_token": "token"}), 200

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=500)
