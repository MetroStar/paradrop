#!/usr/bin/env python3
from flask import Response, request
from flask_restful import Resource
import json
from asyncio import run
from flask_setup import logger
from flasgger import swag_from
from db.event_triggers import db_get_events_triggers, db_add_event_trigger, db_update_event_trigger, db_delete_event_trigger
from api_auth import user_api, admin_api


class ListEventTriggers(Resource):
    @user_api
    @swag_from("endpoints_spec/list_event_triggers.yml")
    def get(self, query: str, data_part: str, sort: str) -> json:
        try:
            # If sorting specifications are specificed,
            # convert it to correct format
            if sort.split("-")[0] == "none":
                sort = {}
            elif sort.split("-")[0] == "event_trigger":
                if sort.split("-")[1] == "true":
                    sort = {sort.split("-")[0] + ".field": "asc"}
                else:
                    sort = {sort.split("-")[0] + ".field": "desc"}
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
                        "fields": [
                            "event_name", "event_impact",
                            "event_enable", "send_alert",
                            "event_trigger.field", "event_trigger.operator",
                            "event_trigger.expected_value"
                        ]
                    }
                }
            }

            response: dict = run(db_get_events_triggers(search_query))
            if response["valid"]:
                response_data: dict = {}
                response_data["data"] = response["data"]
                response_data["number_of_results"] = response["number_of_results"]
                return json.dumps(response_data), 200
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class AddEventTrigger(Resource):
    @admin_api
    @swag_from("endpoints_spec/add_event_trigger.yml")
    def post(self) -> json:
        try:
            event_trigger_data: dict = request.json
            if event_trigger_data:

                # If request data contain ID, use it as the event trigger id
                event_trigger_id: str = ""
                if "id" in event_trigger_data:
                    event_trigger_id = event_trigger_data["id"]

                new_event_trigger: dict = {}
                # Transfer all words to title case and replace _ with spaces
                new_event_trigger["event_name"] = event_trigger_data["event_name"].replace(
                    " ", "_").lower()
                new_event_trigger["send_alert"] = event_trigger_data["send_alert"]
                new_event_trigger["event_impact"] = event_trigger_data["event_impact"]
                new_event_trigger["event_enable"] = event_trigger_data["event_enable"]
                new_event_trigger["event_trigger"] = event_trigger_data["event_trigger"]
                response: dict = run(
                    db_add_event_trigger(
                        new_event_trigger,
                        event_trigger_id))
                if response["valid"]:
                    return Response(
                        response=response["message"],
                        status=response["code"])
                else:
                    return Response(
                        response=response["message"],
                        status=response["code"])
            else:
                return Response(response="Required data are missing..",
                                status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class UpdateEventTrigger(Resource):
    @admin_api
    @swag_from("endpoints_spec/update_event_trigger.yml")
    def post(self) -> Response:
        try:
            update_data: dict = request.json
            if update_data:
                updated_event_trigger: dict = {}
                updated_event_trigger["id"] = update_data["id"]
                updated_event_trigger["event_name"] = update_data["event_name"]
                updated_event_trigger["send_alert"] = update_data["send_alert"]
                updated_event_trigger["event_impact"] = update_data["event_impact"]
                updated_event_trigger["event_enable"] = update_data["event_enable"]
                updated_event_trigger["event_trigger"] = update_data["event_trigger"]
                updated_event_trigger["created_at"] = update_data["created_at"]
                updated_event_trigger["created_by"] = update_data["created_by"]
                response: dict = run(
                    db_update_event_trigger(
                        updated_event_trigger,
                        update_data["id"]))
                if response["valid"]:
                    return Response(
                        response=response["message"],
                        status=response["code"])
                else:
                    return Response(
                        response=response["message"],
                        status=response["code"])
            else:
                return Response(response="Required data are missing..",
                                status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class DeleteEventTrigger(Resource):
    @admin_api
    @swag_from("endpoints_spec/delete_event_trigger.yml")
    def delete(self) -> Response:
        try:
            event_trigger_id: dict = request.json
            if event_trigger_id:
                event_trigger_id: str = request.json["id"]
            else:
                return Response(response="Required data are missing..",
                                status=400)
            response: dict = run(db_delete_event_trigger(event_trigger_id))
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
