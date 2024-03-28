#!/usr/bin/env python3
from flask_setup import logger
from db.db_requests import get_request
from config.config import ES_CONFIGS_URL
from db.db_requests import post_request
from utils.audit_events import add_audit_event


async def db_get_configurations() -> dict:
    """
    Function that returns current configurations.
    """
    try:

        paradrop_configs: dict = get_request(ES_CONFIGS_URL + "/_doc/1").json()
        if paradrop_configs["found"]:
            return {
                "valid": True,
                "code": 200,
                "message": "Configurations found..",
                # "_source" is a field is where the data is stored
                "data": paradrop_configs["_source"]}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "Configurations not found..",
                "data": {}}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_update_configurations(current_configs: dict, configs_update: dict) -> dict:
    """
    Function that accepts current and new configurations data as an argument
    and updates current configurations with new ones.
    """
    try:

        # Creating dictionary to store updated configurations
        new_configs: dict = current_configs

        for field in configs_update:
            if field in current_configs.keys():
                if "enable" in field:
                    # When changing enable_* fields, we want to ensure
                    # that it's a type boolean
                    if not (isinstance(configs_update[field], bool)):
                        return {
                            "valid": False,
                            "code": 400,
                            "message": f"Parameter {field} has to be type boolean..",
                            "data": {}}

                # Updating current configurations with new data
                new_configs[field] = configs_update[field]
            else:
                return {
                    "valid": False,
                    "code": 400,
                    "message": f"No {field} parameter found in paradrop configurations..",
                    "data": {}}

        # Send db request to update configurations
        post_request(ES_CONFIGS_URL + "/_doc/1", new_configs)

        # Adding event to Audit index and saving previous state of data
        # into it.
        add_audit_event(
            event_description="UPDATED Configurations.",
            previous_state=current_configs)

        return {
            "valid": True,
            "code": 200,
            "message": "Configurations updated succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
