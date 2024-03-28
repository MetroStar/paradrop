#!/usr/bin/env python3
from flask_setup import logger
from config.config import ES_USERS_URL
from db.users.read_users import db_get_user
from db.db_requests import delete_request
from utils.audit_events import add_audit_event


async def db_delete_user(email: str) -> dict:
    """
    Function that accepts email as an argument, check if
    it's binded to any user in the database and deletes user
    account from the database if it is.
    """
    try:
        response: dict = await db_get_user(email)
        if not response["valid"]:
            return {
                "valid": False,
                "code": 404,
                "message": "No user was found.."}
        user_id: str = response["data"]["id"]

        # Send db request to delete user
        delete_request(ES_USERS_URL + "/_doc/" + user_id)

        # Adding event to Audit index and saving previous state of data into
        # it.
        add_audit_event(
            event_description=f"DELETED user with email {email}.",
            previous_state=response["data"])

        return {
            "valid": True,
            "code": 200,
            "message": "User deleted successfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
