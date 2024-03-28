#!/usr/bin/env python3
from db.users.create_users import hash_pwd
from db.users.read_users import db_get_user
from config.config import ES_USERS_URL
from flask_setup import logger
from db.db_requests import post_request
from utils.timestamps import gen_timestamp
from utils.audit_events import add_audit_event


async def db_update_user(email: str, new_email: str = "") -> dict:
    """
    Function that gets email from user's cookies and
    check if user exists in the database. If user
    exists and there is a new email provided as an argument,
    function then check if email isn't already used by
    another user and then makes an update of user's
    data if everything is valid.
    """
    try:
        # Check if user is in the db
        response: dict = await db_get_user(email)
        if not response["valid"]:
            return {
                "valid": False,
                "code": 404,
                "message": "No user was found.."}

        user_id: str = response["data"]["id"]
        updated_user_data: dict = response["data"]

        # If user specified new email,
        # check if it's not already in the database
        if new_email != "":
            email_used: dict = await db_get_user(new_email)
            if not email_used["valid"]:
                updated_user_data["email"] = new_email

        updated_user_data["updated_at"] = gen_timestamp()

        # Send db request to update user's data
        post_request(ES_USERS_URL + "/_doc/" + user_id, updated_user_data)

        # Adding event to Audit index and saving previous state of data into
        # it.
        add_audit_event(
            event_description=f"UPDATED User with ID {user_id}.",
            previous_state=response["data"])
        return {
            "valid": True,
            "code": 200,
            "message": "User's data updated succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_allow_pwd_reset(email: str) -> dict:
    """
    Function that accepts email as an argument,
    check if there is a user in the database binded to
    the email and if there is and he has his reset_password attribute
    set to false, it changes it to true. User is then
    able to change his password.
    """
    try:
        # Check if user is in the db
        response: dict = await db_get_user(email)
        if not response["valid"]:
            return {
                "valid": False,
                "code": 404,
                "message": "No user was found.."}

        updated_user_data: dict = response["data"]
        user_id: str = response["data"]["id"]

        if not response["data"]["reset_password"]:
            updated_user_data["reset_password"] = True
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Password reset allowed.."}

        updated_user_data["updated_at"] = gen_timestamp()

        # Send db request to allow user to change his password
        post_request(ES_USERS_URL + "/_doc/" + user_id, updated_user_data)

        # Adding event to Audit index and saving previous state of data into
        # it.
        add_audit_event(
            event_description=f"UPDATED User with ID {user_id} - Allowed password change.",
            previous_state=response["data"])

        return {
            "valid": True,
            "code": 200,
            "message": "Password reset allowed.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_pwd_reset(email: str, pwd: str) -> dict:
    """
    Function that accepts email and a password as an argument,
    check if there is a user in the database binded to the email
    and if his reset_password attribute is set to
    true. If it is, user's password gets
    changed to password that he provided as an argument
    and his reset_password attribute is changed to false.
    """
    try:
        # Check if user is in the database
        response: dict = await db_get_user(email)
        if not response["valid"]:
            return {
                "valid": False,
                "code": 404,
                "message": "No user was found.."}

        updated_user_data: dict = response["data"]
        user_id: str = response["data"]["id"]

        # Check if user is allowed to change his password
        if response["data"]["reset_password"]:
            # Hash new password and set it to user's data
            updated_user_data["password"] = await hash_pwd(pwd)
            updated_user_data["reset_password"] = False
        else:
            return {"valid": False,
                    "code": 400,
                    "message": "User isn't allowed to reset his password.."}

        updated_user_data["updated_at"] = gen_timestamp()
        updated_user_data["expire_at"] = gen_timestamp(expiration_days=60)

        # Send db request to change user's password
        post_request(ES_USERS_URL + "/_doc/" + user_id, updated_user_data)

        # Adding event to Audit index and saving previous state of data into
        # it.
        add_audit_event(
            event_description=f"UPDATED User with ID {user_id} - Password change.",
            previous_state=response["data"])

        return {
            "valid": True,
            "code": 200,
            "message": "Password reseted succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_update_user_attribute(user_email: str, attribute: str, new_value: str) -> dict:
    """
    Function that accepts email, attribute and a new value as an argument, then
    check if there is a user in the database binded to the email
    and then makes an update to specified attribute.
    """
    try:
        # Check if user is in the db
        response: dict = await db_get_user(user_email)
        if not response["valid"]:
            return {
                "valid": False,
                "code": 404,
                "message": "No user was found.."}

        user_id: str = response["data"]["id"]
        response["data"][attribute] = new_value

        # Send db request to update specified attribute
        post_request(ES_USERS_URL + "/_doc/" + user_id, response["data"])

        return {
            "valid": True,
            "code": 200,
            "message": f"Attribute {attribute} updated succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
