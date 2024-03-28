#!/usr/bin/env python3
import re
from typing import List
from flask_setup import logger
from flask_setup import bcrypt
from config.config import ES_USERS_URL, ES_TOKENS_URL
from db.db_requests import post_request, get_request


async def validate_email(email: str) -> bool:
    """
    Function that accepts an email and check if it's in a correct
    "example@email.com" format.
    """
    try:
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if email is not None:
            if (re.fullmatch(email_regex, email)):
                return True
        return False

    except BaseException as e:
        logger.error(e)
        return False


async def check_pwd(email: str, pwd: str) -> dict:
    """
    Function that accepts email and a password from the user as an arguments.
    If email match a user in the database, check
    if the password from the user match the password
    binded to that email from the database.
    """
    try:
        response: dict = await db_get_user(email)
        if not response["valid"]:
            return {
                "valid": False,
                "code": 404,
                "message": f"User {email} not found.."}

        # Check if given password match the password in the database
        password_match: bool = bcrypt.check_password_hash(
            response["data"]["password"], pwd)
        if password_match:
            return {
                "valid": True,
                "code": 200,
                "message": f"Email and pwd match. User {email} can now login.."}
        else:
            return {
                "valid": False,
                "code": 401,
                "message": "Invalid password.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_get_user(email: str) -> dict:
    """
    Function that validates if email is in a correct email format, then
    makes db call, and returns user data as a dictionary, if user was found.
    """
    try:
        valid_email: bool = await validate_email(email)
        if not valid_email:
            return {
                "valid": False,
                "code": 400,
                "message": "Email is in a wrong format.."}

        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": f'("{email}")',
                                "default_field": "email",
                            }
                        }
                    ]
                }
            },
        }

        # Send db request to get user's data
        response: dict = post_request(ES_USERS_URL + "/_search", query)

        # If we have found any results
        if response.json()["hits"]["total"]["value"]:

            # "_source" is a field is where the data is stored
            user_data: dict = response.json()["hits"]["hits"][0]["_source"]

            return {
                "valid": True,
                "code": 200,
                "message": "User found, returning data..",
                "data": user_data}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "User not found..",
                "data": {}}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_get_all_users(query: dict = {"query": {"match_all": {}}}) -> dict:
    """
    Function that returns data about all users in the database. We can specify
    the database query to get only users matching a specific keyword or to only
    retrieve part of the data.
    """
    try:
        # Send db request to get user's data
        response: dict = post_request(ES_USERS_URL + "/_search", query)

        # Variable to keep track of the number
        # of all results that match our query
        number_of_results: int = response.json()["hits"]["total"]["value"]
        users: List[dict] = []

        # If we have found any results
        if response.json()["hits"]["total"]["value"]:
            for user in response.json()["hits"]["hits"]:
                users.append(user["_source"])

        if users == [] or users == [{}]:
            return {
                "valid": False,
                "code": 404,
                "message": "No users found in the database..",
                "data": users,
                "number_of_results": number_of_results}
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Users found, returning data..",
                "data": users,
                "number_of_results": number_of_results}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_get_user_token(email: str) -> dict:
    """
    Function that search for user's email in paradrop_tokens
    index and if there is a token binded to the email address, it returns it.
    """
    try:
        # Send db request to get data about user tokens
        response: dict = get_request(ES_TOKENS_URL + "/_search")

        # If we found user in paradrop_tokens index, return the token
        # binded to user's email address
        if email in response.json()[
                "hits"]["hits"][0]["_source"]["user_tokens"]:
            return {
                "valid": True,
                "code": 200,
                "message": "User token was found..",
                "data": response.json()["hits"]["hits"][0]["_source"]["user_tokens"][email]}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "No user token found..",
                "data": {}}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
