#!/usr/bin/env python3
from typing import List
from flask_setup import logger
from config.config import ES_HOSTS_URL
from db.db_requests import post_request


async def db_add_host(new_host_data: dict) -> dict:
    """
    Function that accepts data about new host and add it into database.
    """
    try:
        # Send db request to add new host
        post_request(ES_HOSTS_URL + "/_doc/" + new_host_data["id"], new_host_data)

        return {
            "valid": True,
            "code": 200,
            "message": "Host added succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_get_hosts(query: dict = {"query": {"match_all": {}}}) -> dict:
    """
    Function that returns data about all hosts in the database. We can specify
    the database query to get only hosts matching a specific keyword or to only
    retrieve part of the data.
    """
    try:
        # Send db request to get data about hosts
        resp = post_request(ES_HOSTS_URL + "/_search", query)

        # Variable to keep track of the number
        # of all results that match our query
        number_of_results: int = resp.json()["hits"]["total"]["value"]
        hosts: List[dict] = []

        # If we found any results
        if number_of_results > 0:
            for host in resp.json()["hits"]["hits"]:
                hosts.append(host["_source"])

        if hosts == [] or hosts == [{}]:
            return {
                "valid": False,
                "code": 404,
                "message": "No hosts found in the database..",
                "data": hosts,
                "number_of_results": number_of_results}
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Hosts found, returning data..",
                "data": hosts,
                "number_of_results": number_of_results}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
