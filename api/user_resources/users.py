#!/usr/bin/env python3
from flask import session, Response, request
from flask_restful import Resource
from typing import List
import json
import re
from asyncio import run
from db.users.create_users import db_create_user
from db.users.read_users import db_get_user, db_get_all_users, validate_email, check_pwd
from db.users.update_users import db_allow_pwd_reset, db_pwd_reset, db_update_user
from db.users.delete_users import db_delete_user
from db.user_tokens import db_delete_user_token
from api_auth import user_api, admin_api
from flask_setup import logger
from flasgger import swag_from


async def validate_password(password):
    """
    Function to validate if password meets our requirements.
    """
    if len(password) >= 12:
        if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
            if re.search(r"\W", password) and re.search(r"\d", password):
                return {
                    "valid": True,
                    "code": 200,
                    "message": "Password is valid.."}
            else:
                return {
                    "valid": False,
                    "code": 400,
                    "message": "Password must have atleast one digit and special character.."}
        else:
            return {
                "valid": False,
                "code": 400,
                "message": "Password must have atleast one uppercase and lowercase letter.."}
    else:
        return {
            "valid": False,
            "code": 400,
            "message": "Password must be atleast 12 characters long.."}


class ListUsers(Resource):
    @user_api
    @swag_from("endpoints_spec/list_users.yml")
    def get(self, query: str, data_part: str, sort: str) -> json:
        try:
            # If sorting specifications are specificed,
            # convert it to correct format
            if sort.split("-")[0] == "none":
                sort = {}
            else:
                if sort.split("-")[1] == "true":
                    sort = {sort.split("-")[0]: "asc"}
                else:
                    sort = {sort.split("-")[0]: "desc"}

            search_query: dict = {
                "from": data_part.split("-")[0],
                "size": data_part.split("-")[1],
                "sort": [sort],
                "query": {
                    "query_string": {
                        "query": f"*{query}*",
                        "fields": ["email", "name", "role",
                                   "last_signin", "created_at", "expire_at"]
                    }
                }
            }
            response: dict = run(db_get_all_users(query=search_query))
            if response["valid"]:
                user_data: List[dict] = []

                for data in response["data"]:
                    filtered_data: dict = {}
                    session_email = session.get("email")
                    if session_email is not None and session_email == data["email"]:
                        filtered_data["current_user"] = True
                    else:
                        filtered_data["current_user"] = False
                    filtered_data["email"] = data["email"]
                    filtered_data["name"] = data["name"]
                    filtered_data["role"] = data["role"]
                    filtered_data["last_signin"] = data["last_signin"]
                    filtered_data["created_at"] = data["created_at"]
                    filtered_data["expire_at"] = data["expire_at"]
                    filtered_data["reset_password"] = data["reset_password"]
                    user_data.append(filtered_data)

                response_data: dict = {}
                response_data["user_data"] = user_data
                response_data["number_of_results"] = response["number_of_results"]

                # Add role of the current user to the response data
                if session_email:
                    current_user_role: dict = run(db_get_user(session_email))
                    response_data["current_user_role"] = current_user_role["data"]["role"]
                else:
                    response_data["current_user_role"] = ""

                return json.dumps(response_data), 200
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class CreateAccount(Resource):
    @admin_api
    @swag_from("endpoints_spec/create_account.yml")
    def post(self) -> Response:
        try:
            user_data: dict = request.json
            if user_data:
                user_name: str = user_data["name"]
                user_email: str = user_data["email"]
                user_pwd1: str = user_data["pwd1"]
                user_pwd2: str = user_data["pwd2"]
                user_role: str = user_data["role"]
            else:
                return Response(response="Required data are missing..",
                                status=400)

            # Check if user provided data are valid.
            if user_email and user_name and user_pwd1 and user_pwd2 and user_role:
                if user_pwd1 == user_pwd2:
                    password_validation: dict = run(
                        validate_password(user_pwd1))
                    if password_validation["valid"]:
                        email_valid: bool = run(validate_email(user_email))
                        if email_valid:
                            response: dict = run(db_create_user(
                                user_email, user_name, user_pwd1, user_role))
                        else:
                            return Response(
                                response="Email is in a wrong format..",
                                status=400)
                    else:
                        return Response(
                            response=password_validation["message"],
                            status=password_validation["code"])
                else:
                    return Response(response="Passwords doesn't match..",
                                    status=400)

                if response["valid"]:
                    return Response(
                        response=response["message"],
                        status=response["code"])
                else:
                    return Response(
                        response=response["message"],
                        status=response["code"])
            else:
                return Response(
                    response="Data from user are incomplete..",
                    status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class AllowPasswordReset(Resource):
    @admin_api
    @swag_from("endpoints_spec/allow_password_reset.yml")
    def put(self) -> Response:
        try:
            user_data: dict = request.json
            if user_data:
                user_email: str = request.json["email"]
            else:
                return Response(response="Required data are missing..",
                                status=400)

            response: dict = run(db_allow_pwd_reset(user_email))
            if response["valid"]:
                return Response(
                    response=response["message"],
                    status=response["code"])
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class ResetPassword(Resource):
    @swag_from("endpoints_spec/reset_password.yml")
    def put(self) -> Response:
        try:
            user_data: dict = request.json
            if user_data:
                user_email: str = user_data["email"]
                user_pwd1: str = user_data["pwd1"]
                user_pwd2: str = user_data["pwd2"]
            else:
                return Response(response="Required data are missing..",
                                status=400)

            # Check if user provided data are valid.
            if user_pwd1 and user_pwd2:
                if user_pwd1 == user_pwd2:
                    password_validation: dict = run(
                        validate_password(user_pwd1))
                    if password_validation["valid"]:
                        email_valid: bool = run(validate_email(user_email))
                        if email_valid:
                            response: dict = run(
                                db_pwd_reset(user_email, user_pwd1))
                            if response["valid"]:
                                return Response(
                                    response=response["message"],
                                    status=response["code"])
                            else:
                                return Response(
                                    response=response["message"],
                                    status=response["code"])
                        else:
                            return Response(
                                response="Email is in a wrong format..",
                                status=400)
                    else:
                        return Response(
                            response=password_validation["message"],
                            status=password_validation["code"])
                else:
                    return Response(response="Passwords doesn't match..",
                                    status=400)
            else:
                return Response(
                    response="Data from user are incomplete..",
                    status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class UpdateUser(Resource):
    @user_api
    @swag_from("endpoints_spec/update_user.yml")
    def put(self) -> Response:
        try:
            user_data: dict = request.json
            if user_data:
                user_email: str = user_data["email"]
                user_pwd1: str = user_data["pwd1"]
                user_pwd2: str = user_data["pwd2"]
            else:
                return Response(response="Required data are missing..",
                                status=400)

            if user_pwd1 != user_pwd2:
                return Response(response="Passwords do not match..",
                                status=400)

            email_found: dict = run(db_get_user(user_email))
            if email_found["valid"]:
                return Response(response="Email is already in use..",
                                status=400)

            session_email = session.get("email")
            if session_email is not None:
                password_match: dict = run(check_pwd(session_email, user_pwd2))
                if password_match["valid"]:
                    update_user: dict = run(db_update_user(
                        email=session_email,
                        new_email=user_email)
                    )
                    if update_user["valid"]:
                        session["email"] = user_email
                        return Response(
                            response=update_user["message"],
                            status=update_user["code"])
                    else:
                        return Response(
                            response=update_user["message"],
                            status=update_user["code"])
                else:
                    return Response(
                        response=password_match["message"],
                        status=password_match["code"])
            else:
                return Response(response="You must login as a user to be able to use this endpoint..",
                                status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class DeleteUser(Resource):
    @admin_api
    @swag_from("endpoints_spec/delete_user.yml")
    def delete(self) -> Response:
        try:
            user_data: dict = request.json
            if user_data:
                user_email: str = user_data["email"]
            else:
                return Response(response="Required data are missing..",
                                status=400)

            response: dict = run(db_delete_user(user_email))
            if response["valid"]:
                # Deleting user token of deleted user
                run(db_delete_user_token(user_email))
                return Response(
                    response=response["message"],
                    status=response["code"])
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)
