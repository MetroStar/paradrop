#!/usr/bin/env python3
from flask_setup import logger
from db.db_requests import get_request
from config.config import ES_TOKENS_URL
from db.db_requests import post_request
from utils.audit_events import add_audit_event
from uuid import uuid4


async def db_get_agent_token() -> dict:
    """
    Function that returns current agent token.
    """
    try:
        agent_token: dict = get_request(ES_TOKENS_URL + "/_doc/1").json()
        if agent_token["found"]:
            return {
                "valid": True,
                "code": 200,
                "message": "Agent token found..",
                # "_source" is a field is where the data is stored
                "data": agent_token["_source"]["agent_token"]}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "Agent token not found..",
                "data": {}}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_update_agent_token(user_token: str = "") -> dict:
    """
    Function to update current agent token with a new one.
    """
    try:
        current_agent_token: dict = get_request(
            ES_TOKENS_URL + "/_doc/1").json()
        if current_agent_token["found"]:

            # "_source" is a field is where the data is stored
            updated_tokens: dict = current_agent_token["_source"]

            # If user specified his own token, set it as a new agent token
            if user_token:
                updated_tokens["agent_token"] = user_token
            else:
                updated_tokens["agent_token"] = uuid4()

            # Send db request to update agent token
            post_request(ES_TOKENS_URL + "/_doc/1", updated_tokens)

            # Adding event to Audit index and saving previous state of data
            # into it.
            add_audit_event(
                event_description="UPDATED Agent Token.",
                previous_state=current_agent_token)

            return {
                "valid": True,
                "code": 200,
                "message": "Agent token updated succesfully.."}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "Agent token not found.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
