#!/usr/bin/env python3
from flask_setup import logger
from db.db_requests import post_request
from config.config import ES_CHANGES_URL
from typing import List
from utils.id_generator import gen_id
from utils.timestamps import gen_timestamp
import json


async def db_add_changes(original_host_data: dict, new_host_data: dict) -> dict:
    """
    Function that takes original host data and new host data, creates a new dictionary
    containing all differences between them and adds them into the Changes index.
    """
    try:
        # Base text for changes summary
        changes_summary: str = "Changes found in"

        # List of all keys that we don't want to include in the comparison.
        keys_to_skip: list = [
            "diskfree_gb",
            "diskused_gb",
            "diskused_pct",
            "docker_containers",
            "docker_images_count",
            "docker_images",
            "docker_labels",
            "id",
            "network_interfaces",
            "journalctl_logs",
            "last_run",
            "load1",
            "load5",
            "load15",
            "memoryfree_gb",
            "memoryused_gb",
            "memoryused_pct",
            "processes",
            "sysctl",
            "systemd_timers",
            "trivy",
            "uptime_days",
            "users_loggedin",
            "dmesg_errors",
        ]

        changes: dict = {}

        for key in original_host_data.keys():
            if key not in keys_to_skip:
                # Searching if any data from the original host was updated or deleted
                if key in new_host_data.keys():

                    # If data are not the same in original and new host data
                    if new_host_data[key] != original_host_data[key]:

                        # Add details to changes
                        changes_summary += f" - {key}"
                        changes[key] = json.dumps(
                            {"+++": new_host_data[key], "---": original_host_data[key]},
                            indent=1,
                        )
                else:
                    changes_summary += f" - {key}"
                    changes[key] = json.dumps(
                        {"---": original_host_data[key]}, indent=1
                    )

        for key in new_host_data.keys():
            if key not in keys_to_skip:

                # Searching for a key that is not present in the original host data
                if key not in original_host_data.keys():

                    # Add details to changes if there is a new key
                    changes_summary += f" - {key}"
                    changes[key] = json.dumps({"+++": new_host_data[key]}, indent=1)

        # If there were any changes made, add them to the Changes index
        if changes != {}:
            changes["id"] = gen_id()
            changes["changes_summary"] = changes_summary
            changes["changes_discovered"] = gen_timestamp()

            # Send db request to add new changes
            post_request(ES_CHANGES_URL + "/_doc/" + changes["id"], changes)

    except BaseException as e:
        logger.error(e)
        return {"valid": False, "code": 500, "message": f"Something went wrong: {e}.."}


async def db_get_changes(query: dict = {"query": {"match_all": {}}}) -> dict:
    """
    Function that returns data about all changes in the database. We can specify
    the database query to get only changes matching a specific keyword or to only
    retrieve part of the data.
    """
    try:
        # Send db request to get data about all changes
        resp = post_request(ES_CHANGES_URL + "/_search", query)

        # Variable to keep track of the number
        # of all results that match our query
        number_of_results: int = resp.json()["hits"]["total"]["value"]
        changes: List[dict] = []

        # If we found any results
        if number_of_results > 0:
            for change in resp.json()["hits"]["hits"]:
                # "_source" is a field is where the data is stored
                changes.append(change["_source"])

        if changes == [] or changes == [{}]:
            return {
                "valid": False,
                "code": 404,
                "message": "No changes found in the database..",
                "data": changes,
                "number_of_results": number_of_results,
            }
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Changes found, returning data..",
                "data": changes,
                "number_of_results": number_of_results,
            }

    except BaseException as e:
        logger.error(e)
        return {"valid": False, "code": 500, "message": f"Something went wrong: {e}.."}
