#!/usr/bin/env python3
from flask import Response
from flask_restful import Resource
from flask_setup import logger
from flasgger import swag_from


class HealthCheck(Resource):
    @swag_from("endpoints_spec/health_check.yml")
    def get(self) -> Response:
        try:
            return Response(response="OK..",
                            status=200)
        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)
