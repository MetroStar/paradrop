#!/usr/bin/env python3
from flask import Response, request
from flask_restful import Resource
from flasgger import swag_from
from asyncio import run
import json
from flask_setup import logger
from api_auth import admin_api, user_api
from db.configurations import db_get_configurations, db_update_configurations


class ListConfigurations(Resource):
    @user_api
    @swag_from('endpoints_spec/list_configurations.yml')
    def get(self) -> json:
        try:
            response: dict = run(db_get_configurations())
            if response["valid"]:
                return json.dumps(response["data"]), 200
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class UpdateConfigurations(Resource):
    @admin_api
    @swag_from('endpoints_spec/update_configurations.yml')
    def post(self) -> Response:
        try:

            configs_update: dict = request.json
            if configs_update:
                current_configs: dict = run(db_get_configurations())
                if current_configs["valid"]:
                    response: dict = run(
                        db_update_configurations(
                            current_configs["data"],
                            configs_update))
                    return Response(
                        response=response["message"],
                        status=response["code"])
                else:
                    return Response(
                        response=current_configs["message"],
                        status=current_configs["code"])

            else:
                return Response(response="Required data are missing..",
                                status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)
