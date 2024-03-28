#!/usr/bin/env python3
from flask_setup import logger
from flask_setup import bcrypt
from config.config import ES_USERS_URL
from db.users.read_users import db_get_user
from db.db_requests import post_request
from utils.id_generator import gen_id
from utils.timestamps import gen_timestamp
from utils.audit_events import add_audit_event


async def hash_pwd(pwd: str) -> str:
    """
    Function that uses bcrypt to hash passwords.
    """
    try:
        password = bcrypt.generate_password_hash(pwd).decode("utf-8")
        return str(password)
    except BaseException as e:
        logger.error(e)
        return ""


async def db_create_user(email: str, name: str, pwd: str, role: str) -> dict:
    """
    Function that accepts email, name, pwd and a role as an arguments,
    check if there already isn't a user with that email in
    the database and if there isn't, it creates a new user account.
    """
    try:
        response: dict = await db_get_user(email)
        if response["valid"]:
            return {"valid": False, "code": 400, "message":
                    "User with this email already exists.."}

        new_user: dict = {}
        generated_id: str = gen_id()
        new_user["id"] = generated_id
        new_user["email"] = email
        new_user["name"] = name
        hashed_pwd: str = await hash_pwd(pwd)

        # If there was a problem with password hashing, return an error 400
        if not hashed_pwd:
            return {"valid": False, "code": 400, "message":
                    "There is an issue with password hashing..."}
        else:
            new_user["password"] = hashed_pwd

        if role == "admin" or role == "read-only":
            new_user["role"] = role
        else:
            return {"valid": False, "code": 400, "message":
                    f"{role} isn't a valid role.."}

        new_user["expire_at"] = gen_timestamp(expiration_days=60)
        new_user["created_at"] = gen_timestamp()
        new_user["updated_at"] = gen_timestamp()
        new_user["last_signin"] = gen_timestamp()
        new_user["locked"] = False
        new_user["reset_password"] = False

        # Send db request to add a new user
        post_request(ES_USERS_URL + "/_doc/" + generated_id, new_user)

        # Adding event to Audit index
        add_audit_event(
            event_description=f"CREATED {role} user with email {email}.")

        return {
            "valid": True,
            "code": 200,
            "message": "User created succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
