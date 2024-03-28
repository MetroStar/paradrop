#!/usr/bin/env python3
import requests
from json import dumps
from config.config import ES_TLS_VERIFY, ES_USER, ES_PW, HEADERS
from flask import Response
from utils.id_generator import gen_id


def post_request(request_url: str, request_data: dict) -> Response:
    """
    Function to make POST request to the database.
    """
    # If request target is /_doc/ endpoint and it doesn't include an id,
    # generate and bind one to it
    if request_url[-6:] == "/_doc/":
        random_id: str = gen_id()
        request_url = request_url + random_id
    return requests.post(
        url=request_url,
        verify=ES_TLS_VERIFY,
        data=dumps(request_data, default=str),
        auth=(ES_USER, ES_PW),
        headers=HEADERS)


def bulk_post_request(request_url: str, request_data: list) -> Response:
    """
    Function to make bulk POST request to the database.
    Data for bulk request should always be in a list.
    Example of correctly formatted data for bulk request:

    [
    { "create" : {"_index" : "paradrop_events"}},
    { "event_name" : "New Event Name", "event_id" : 5},
    { "create" : {"_index" : "paradrop_hosts"}},
    { "hostname" : "New Hostname", "host_id" : 2 }
    ]
    """

    # Updating format of request data
    bulk_request_data = '\n'.join([dumps(line)
                                  for line in request_data]) + '\n'

    return requests.post(
        url=request_url + "/_bulk",
        verify=ES_TLS_VERIFY,
        data=bulk_request_data,
        auth=(ES_USER, ES_PW),
        headers=HEADERS)


def put_request(request_url: str, request_data: dict) -> Response:
    """
    Function to make PUT request to the database.
    """
    return requests.put(
        url=request_url,
        verify=ES_TLS_VERIFY,
        data=dumps(request_data, default=str),
        auth=(ES_USER, ES_PW),
        headers=HEADERS)


def get_request(request_url: str) -> Response:
    """
    Function to make GET request to the database.
    """
    try:
        return requests.get(
            url=request_url,
            verify=ES_TLS_VERIFY,
            auth=(ES_USER, ES_PW),
            headers=HEADERS)
    except BaseException:
        return Response(response="Index not found..",
                        status=404, mimetype='application/json')


def delete_request(request_url: str) -> Response:
    """
    Function to make DELETE request to the database.
    """
    return requests.delete(
        url=request_url,
        verify=ES_TLS_VERIFY,
        auth=(ES_USER, ES_PW),
        headers=HEADERS)
