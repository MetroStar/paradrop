#!/usr/bin/env python3
from flask import request, Response
from flask_restful import Resource
from flask_setup import logger
from flasgger import swag_from
from db.hosts import db_add_host
from db.events import db_generate_events
from db.agent_token import db_get_agent_token
from db.event_triggers import db_get_events_triggers
from db.configurations import db_get_configurations
from db.db_requests import get_request
from db.changes import db_add_changes
from config.config import ES_HOSTS_URL
from asyncio import run

class AddHost(Resource):
    @swag_from("endpoints_spec/add_host.yml")
    def post(self) -> Response:
        try:
            # Check if token from user match the agent auth token from our
            # database.
            user_token: str = request.headers.get("X-Paradrop-Token")
            if user_token:
                agent_auth_token: dict = run(db_get_agent_token())
                if agent_auth_token["valid"]:
                    if agent_auth_token["data"] != user_token:
                        return Response(
                            response="Invalid agent auth token.",
                            status=403)
                else:
                    return Response(
                        response=agent_auth_token["message"],
                        status=agent_auth_token["code"])
            else:
                return Response(
                    response="Request header must include valid agent auth token.",
                    status=400)

            new_host_data: dict = request.json
            if "id" in new_host_data and "ip_address" in new_host_data:

                # Request to get original data if host already is in our database.
                # "_source" is a field is where the data is stored
                original_host_data: dict = get_request(
                    ES_HOSTS_URL +
                    "/_doc/" + new_host_data["id"]).json()
                
                if original_host_data["found"]:
                    original_host_data = original_host_data["_source"]

                    # Compare old and new data and add the differences into Changes index
                    run(db_add_changes(original_host_data, new_host_data))

                response: dict = run(db_add_host(new_host_data))
                if response["valid"]:
                    event_triggers: dict = run(db_get_events_triggers())
                    current_configurations: dict = run(db_get_configurations())
                    run(db_generate_events(new_host_data,
                                           event_triggers["data"],
                        current_configurations["data"]))
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
