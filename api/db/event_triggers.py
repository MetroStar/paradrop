#!/usr/bin/env python3
from typing import List
from flask import session
from flask_setup import logger
from config.config import ES_EVENT_TRIGGERS_URL
from db.db_requests import post_request, delete_request, get_request
from utils.id_generator import gen_id
from utils.timestamps import gen_timestamp
from utils.audit_events import add_audit_event


async def db_get_events_triggers(query: dict = {"query": {"match_all": {}}}) -> dict:
    """
    Function that returns data about all event triggers in the database. We can specify
    the database query to get only event trigger matching a specific keyword or to only
    retrieve part of the data.
    """
    try:
        # Send db request to get data about all event triggers
        resp = post_request(ES_EVENT_TRIGGERS_URL + "/_search/", query)

        # Variable to keep track of the number
        # of all results that match our query
        number_of_results: int = resp.json()["hits"]["total"]["value"]
        event_triggers: List[dict] = []

        # If we found any results
        if number_of_results > 0:
            for e in resp.json()["hits"]["hits"]:
                # "_source" is a field is where the data is stored
                e_trigger: dict = e["_source"]
                e_trigger["_id"] = e["_id"]
                event_triggers.append(e_trigger)

        if event_triggers == [] or event_triggers == [{}]:
            return {
                "valid": False,
                "code": 404,
                "message": "No event triggers found in the database..",
                "data": event_triggers,
                "number_of_results": number_of_results}
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Found event triggers, returning data..",
                "data": event_triggers,
                "number_of_results": number_of_results}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_add_event_trigger(new_event_trigger: dict, event_trigger_id: str) -> dict:
    """
    Function that accepts data about a new event trigger and add it into
    the database.
    """
    try:
        # If event trigger id is empty, generate a new one
        if event_trigger_id == "":
            event_trigger_id = gen_id()
        new_event_trigger["id"] = event_trigger_id
        new_event_trigger["created_at"] = gen_timestamp()
        new_event_trigger["created_by"] = session.get("email")
        new_event_trigger["updated_at"] = gen_timestamp()
        new_event_trigger["updated_by"] = session.get("email")

        # Send db request to add a new event trigger
        post_request(
            ES_EVENT_TRIGGERS_URL +
            "/_doc/" +
            event_trigger_id,
            new_event_trigger)

        # Adding event to Audit index
        add_audit_event(
            event_description=f"CREATED Event Trigger with ID {event_trigger_id}.")

        return {
            "valid": True,
            "code": 200,
            "message": "Event trigger added succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_update_event_trigger(event_trigger_update: dict, event_trigger_id: str) -> dict:
    """
    Function that accepts data about existing event trigger
    and send a database request to update it.
    """
    try:
        # "_source" is a field is where the data is stored
        current_state: dict = get_request(
            ES_EVENT_TRIGGERS_URL +
            f"/_doc/{event_trigger_id}").json()["_source"]
        event_trigger_update["updated_at"] = gen_timestamp()
        event_trigger_update["updated_by"] = session.get("email")

        # Send db request to update event trigger
        post_request(
            ES_EVENT_TRIGGERS_URL +
            "/_doc/" +
            event_trigger_id,
            event_trigger_update)

        # Adding event to Audit index and saving previous state of data into
        # it.
        add_audit_event(
            event_description=f"UPDATED Event Trigger with ID {event_trigger_id}.",
            previous_state=current_state)

        return {
            "valid": True,
            "code": 200,
            "message": "Event trigger updated succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_delete_event_trigger(event_trigger_id: str) -> dict:
    """
    Function that accepts id of an existing event trigger and deletes it from the database.
    """
    try:
        current_state: dict = get_request(ES_EVENT_TRIGGERS_URL + "/_doc/" +
                                          event_trigger_id).json()

        if current_state["found"]:
            # Send db request to delete event trigger
            delete_request(ES_EVENT_TRIGGERS_URL + "/_doc/" + event_trigger_id)

            # Adding event to Audit index and saving previous state of data
            # into it.
            add_audit_event(
                event_description=f"DELETED Event Trigger with ID {event_trigger_id}.",
                previous_state=current_state["_source"])

            return {
                "valid": True,
                "code": 200,
                "message": "Event trigger deleted successfully.."}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "Event trigger not found.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
