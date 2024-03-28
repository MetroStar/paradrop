#!/usr/bin/env python3
import requests
from json import dumps
from config.config import ES_TLS_VERIFY, ES_USER, ES_PW, HEADERS, ES_AUDIT_URL
from flask import Response, session, request
from utils.id_generator import gen_id
from utils.timestamps import gen_timestamp


def add_audit_event(event_description: str,
                    previous_state: dict = {}) -> Response:
    """
    Function to generate paradrop audit event on every create/update/delete request.
    """
    random_id: str = gen_id()
    new_event: dict = {}
    new_event["id"] = random_id
    new_event["event"] = event_description
    new_event["updated_at"] = gen_timestamp()
    # If there is a session email, set is as a value of "updated_by"
    if session.get("email"):
        new_event["updated_by"] = session.get("email")
    else:
        # Otherwise use email from the header that is used when using agent
        # authorization
        new_event["updated_by"] = request.headers.get("X-Paradrop-Email")

    # Deleting password key from the previous_state dictionary if it's present
    if "password" in previous_state.keys():
        del previous_state["password"]
    new_event["previous_state"] = previous_state

    return requests.post(
        url=ES_AUDIT_URL + "/_doc/" + random_id,
        verify=ES_TLS_VERIFY,
        data=dumps(new_event, default=str),
        auth=(ES_USER, ES_PW),
        headers=HEADERS)
