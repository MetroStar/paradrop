#!/usr/bin/env python3
from flask_setup import logger
from db.db_requests import post_request
from config.config import ES_AUDIT_URL
from typing import List


async def db_get_audit_events(query: dict = {"query": {"match_all": {}}}) -> dict:
    """
    Function that returns data about all audit events in the database. We can specify
    the database query to get only events matching a specific keyword or to only
    retrieve part of the data.
    """
    try:
        # Send db request to get data about all audit events
        response: dict = post_request(ES_AUDIT_URL + "/_search", query)

        # Variable to keep track of the number of all results that match our
        # query
        number_of_results: int = response.json()["hits"]["total"]["value"]
        events: List[dict] = []

        # If we found any results
        if number_of_results > 0:
            for event in response.json()["hits"]["hits"]:
                # "_source" is a field is where the data is stored
                events.append(event["_source"])

        if events == [] or events == [{}]:
            return {
                "valid": False,
                "code": 404,
                "message": "No audit events found in the database..",
                "data": events,
                "number_of_results": number_of_results}
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Audit events found, returning data..",
                "data": events,
                "number_of_results": number_of_results}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
