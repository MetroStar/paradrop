#!/usr/bin/env python3
from flask import session, request, Response
from flask_restful import Resource
from asyncio import run
from utils.csrf_protection import csrf_protection_enabled
from db.users.read_users import check_pwd
from db.users.update_users import db_update_user_attribute
from utils.timestamps import gen_timestamp
from flask_setup import logger
from flasgger import swag_from


class UserLogin(Resource):
    @csrf_protection_enabled
    @swag_from("endpoints_spec/user_login.yml")
    def post(self) -> Response:
        try:
            user_data: dict = request.json
            if user_data:
                user_email: str = user_data["email"]
                user_pwd: str = user_data["pwd"]
            else:
                return Response(response="Required data are missing..",
                                status=400)

            # Check if user's email and pwd match with the database.
            response: dict = run(check_pwd(user_email, user_pwd))

            if response["valid"]:
                # Updating user's attribute last_signin to today's date and
                # time
                run(db_update_user_attribute(
                    user_email, "last_signin", gen_timestamp()))

                # User's email is set as a session email and user can access
                # our site.
                session["email"] = user_email

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


class UserLogout(Resource):
    @swag_from("endpoints_spec/user_logout.yml")
    def get(self) -> Response:
        try:
            session["email"] = None
            return Response(
                response="User logged out successfully.",
                status=200)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)
