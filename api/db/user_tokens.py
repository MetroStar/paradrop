#!/usr/bin/env python3
from flask_setup import logger
from db.db_requests import get_request
from config.config import ES_TOKENS_URL
from db.db_requests import post_request
from utils.audit_events import add_audit_event
from uuid import uuid4


async def db_add_user_token(email: str, role: str, user_token: str) -> dict:
    """
    Function that accepts user email and role, then generates new
    user token and add it into the database under user email.
    """
    try:
        current_tokens: dict = get_request(ES_TOKENS_URL + "/_doc/1").json()
        if current_tokens["found"]:

            # "_source" is a field is where the data is stored
            updated_tokens: dict = current_tokens["_source"]

            # Adding user token and user role under user email into database
            updated_tokens["user_tokens"][email] = {}
            updated_tokens["user_tokens"][email]["role"] = role

            # Check if there is a custom token and generate one if not
            if user_token:
                updated_tokens["user_tokens"][email]["token"] = user_token
            else:
                updated_tokens["user_tokens"][email]["token"] = uuid4()

            # Send db request to update user token
            post_request(ES_TOKENS_URL + "/_doc/1", updated_tokens)

            # Adding event to Audit index and saving previous state of data
            # into it.
            add_audit_event(
                event_description=f"UPDATED token of user with email {email} .",
                previous_state=current_tokens)

            return {
                "valid": True,
                "code": 200,
                "message": "User token updated succesfully.."}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "Tokens not found.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_get_user_token(user_email: str) -> dict:
    """
    Function that returns current user token.
    """
    try:
        user_token: dict = get_request(ES_TOKENS_URL + "/_doc/1").json()
        if user_token["found"]:
            if user_email in user_token["_source"]["user_tokens"].keys():
                return {
                    "valid": True,
                    "code": 200,
                    "message": "User token found..",
                    # "_source" is a field is where the data is stored
                    "data": user_token["_source"]["user_tokens"][user_email]["token"]}

            return {
                "valid": False,
                "code": 404,
                "message": "User token not found..",
                "data": {}}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "paradrop tokens index is missing.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_update_user_token(user_email: str, user_role: str) -> dict:
    """
    Function to update current user token with a new one.
    """
    try:
        current_user_token: dict = get_request(
            ES_TOKENS_URL + "/_doc/1").json()
        if current_user_token["found"]:
            # "_source" is a field is where the data is stored
            updated_tokens: dict = current_user_token["_source"]
            updated_tokens["user_tokens"][user_email] = {}
            updated_tokens["user_tokens"][user_email]["token"] = uuid4()
            updated_tokens["user_tokens"][user_email]["role"] = user_role

            # Send db request to update user token
            post_request(ES_TOKENS_URL + "/_doc/1", updated_tokens)

            # Adding event to Audit index and saving previous state of data
            # into it.
            add_audit_event(
                event_description=f"UPDATED User Token of user with email {user_email}.",
                previous_state=current_user_token)

            return {
                "valid": True,
                "code": 200,
                "message": "User token updated succesfully.."}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "paradrop tokens index is missing.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_delete_user_token(user_email: str) -> dict:
    """
    Function to delete user token binded to a specified email address.
    """
    try:
        current_user_token: dict = get_request(
            ES_TOKENS_URL + "/_doc/1").json()
        if current_user_token["found"]:
            # "_source" is a field is where the data is stored
            updated_tokens: dict = current_user_token["_source"]
            if updated_tokens["user_tokens"].pop(user_email, False):
                # Send db request to update user token
                post_request(ES_TOKENS_URL + "/_doc/1", updated_tokens)

            return {
                "valid": True,
                "code": 200,
                "message": "User token deleted succesfully.."}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "paradrop tokens index is missing.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
