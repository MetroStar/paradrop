#!/usr/bin/env python3
from typing import List
from flask_setup import logger
from config.config import ES_EVENTS_URL
from db.db_requests import post_request, bulk_post_request
from utils.alerts import (
    send_email_alert,
    send_slack_alert,
    send_ms_teams_alert,
    send_mattermost_alert,
)
from utils.id_generator import gen_id
from utils.timestamps import gen_timestamp


async def db_generate_events(
    host_data: dict, event_triggers: list, current_configurations: dict
) -> dict:
    """
    Function that goes through host data and compare values to all event triggers
    in the database. If event trigger is triggered, it will send alert and generate
    new event with informations about what triggered the event trigger.
    """
    try:
        events_data: list = []
        for event_trigger in event_triggers:

            event_trigger_field: str = event_trigger["event_trigger"]["field"]
            event_trigger_operator: str = event_trigger["event_trigger"]["operator"]

            if event_trigger["event_enable"] and event_trigger_field in host_data:

                host_data_value: str = str(host_data[event_trigger_field])
                event_trigger_expected_value: str = str(
                    event_trigger["event_trigger"]["expected_value"]
                )

                # DIGIT ONLY OPERATORS
                if event_trigger_operator == "<":
                    if not (
                        host_data_value.isdigit() and event_trigger_expected_value.isdigit()
                    ):
                        continue

                    if not (int(host_data_value) < int(event_trigger_expected_value)):
                        continue

                elif event_trigger_operator == ">":
                    if not (
                        host_data_value.isdigit() and event_trigger_expected_value.isdigit()
                    ):
                        continue

                    if not (int(host_data_value) > int(event_trigger_expected_value)):
                        continue

                elif event_trigger_operator == ">=":
                    if not (
                        host_data_value.isdigit() and event_trigger_expected_value.isdigit()
                    ):
                        continue

                    if not (int(host_data_value) >= int(event_trigger_expected_value)):
                        continue

                elif event_trigger_operator == "<=":
                    if not (
                        host_data_value.isdigit() and event_trigger_expected_value.isdigit()
                    ):
                        continue

                    if not (int(host_data_value) <= int(event_trigger_expected_value)):
                        continue

                # ANY VALUE OPERATORS
                elif event_trigger_operator == "==":
                    if not (host_data_value == event_trigger_expected_value):
                        continue

                elif event_trigger_operator == "!=":
                    if not (host_data_value != event_trigger_expected_value):
                        continue

                elif event_trigger_operator == "in":
                    if not (host_data_value in event_trigger_expected_value):
                        continue
                else:
                    return {
                        "valid": False,
                        "code": 400,
                        "message": f"{event_trigger_operator} is not a valid operator..",
                    }

                event_id: str = gen_id()
                events_data.append(
                    {"create": {"_index": "paradrop_events", "_id": event_id}}
                )

                event_details: dict = {
                    "event_id": event_id,
                    "id": host_data["id"],
                    "ip_address": host_data["ip_address"],
                    "timestamp": gen_timestamp(),
                    "event_name": event_trigger["event_name"],
                    "event_message": f"Event triggers if {event_trigger_field} {event_trigger_operator} {event_trigger_expected_value} -> Value of {event_trigger_field} field in host data is {host_data_value}.",
                    "event_impact": event_trigger["event_impact"],
                    "alert_sent": False,
                }

                # Adding required field if they are present in host data
                required_fields: list = [
                    "hostname",
                    "platform",
                    "cloud",
                    "tags",
                    "asset_type",
                ]
                for field in required_fields:
                    if field in host_data:
                        event_details[field] = host_data[field]
                    else:
                        event_details[field] = ""

                alerts_sent_to: list = []
                if event_trigger["send_alert"]:
                    if current_configurations["email_enable"]:
                        send_email_alert(current_configurations, event_details)
                        alerts_sent_to.append("email")
                        event_details["alert_sent"] = True

                    if current_configurations["slack_enable"]:
                        send_slack_alert(current_configurations, event_details)
                        alerts_sent_to.append("slack")
                        event_details["alert_sent"] = True

                    if current_configurations["ms_teams_enable"]:
                        send_ms_teams_alert(current_configurations, event_details)
                        alerts_sent_to.append("ms_teams")
                        event_details["alert_sent"] = True

                    if current_configurations["mattermost_enable"]:
                        send_mattermost_alert(current_configurations, event_details)
                        alerts_sent_to.append("mattermost")
                        event_details["alert_sent"] = True

                event_details["alerts_sent_to"] = alerts_sent_to
                events_data.append(event_details)

        if events_data != []:
            bulk_post_request(ES_EVENTS_URL, events_data)

    except BaseException as e:
        logger.error(e)
        return {"valid": False, "code": 500, "message": f"Something went wrong: {e}.."}


async def db_get_events(query: dict = {"query": {"match_all": {}}}) -> dict:
    """
    Function that returns data about all events in the database. We can specify
    the database query to get only events matching a specific keyword or to only
    retrieve part of the data.
    """
    try:
        # Send db request to get data about events
        resp = post_request(ES_EVENTS_URL + "/_search", query)

        # Variable to keep track of the number
        # of all results that match our query
        number_of_results: int = resp.json()["hits"]["total"]["value"]
        events: List[dict] = []

        # If we found any results
        if number_of_results > 0:
            for event in resp.json()["hits"]["hits"]:
                events.append(event["_source"])

        if events == [] or events == [{}]:
            return {
                "valid": False,
                "code": 404,
                "message": "No events found in the database..",
                "data": events,
                "number_of_results": number_of_results,
            }
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Events found, returning data..",
                "data": events,
                "number_of_results": number_of_results,
            }

    except BaseException as e:
        logger.error(e)
        return {"valid": False, "code": 500, "message": f"Something went wrong: {e}.."}
