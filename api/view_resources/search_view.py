#!/usr/bin/env python3
from flask import Response
from flask_restful import Resource
import json
from asyncio import run, gather
from flask_setup import logger
from flasgger import swag_from
from db.db_requests import post_request
from config.config import ES_HOSTS_URL, ES_EVENTS_URL
from db.hosts import db_get_hosts
from db.events import db_get_events
from db.audit import db_get_audit_events
from db.changes import db_get_changes
from api_auth import user_api
from typing import Callable


def get_data_for_view(query: str, query_filter: dict, required_fields: str, data_part: str, sort: dict,
                      get_view_data: Callable, get_data_cards_data: Callable) -> dict:
    """
    This functions gets data based on specified parameters and
    then runs provided function to process data for data cards.
    When it's done, it returns all the data as a response.
    Arguments:
        query: String that we want to search in the database. To get all the data, set the value to "*".
        query_filter: Query filter to include only results that match specified query.
        required_fields: Fields that we want to retrieve from the database.
        data_part: Part of the data that we want to retrieve. Must be hyphen separated.
            5-5 will retrieve results from 5 to 10.
        sort: Sorting settings that we want to add to the query.
        get_view_data: Function to send request to the database.
        get_data_cards_data: Function to process the data for data cards.
    """
    # Default query
    query = {
        "bool": {
            "must": {
                "query_string": {
                    "query": f"*{query}*"
                }
            }
        }
    }

    # If there is a filter selected, add it to query
    if query_filter != "none":
        query["bool"]["filter"] = query_filter

    # If sorting specifications are specificed,
    # convert it to correct format
    if sort.split("-")[0] == "none":
        sort = {}
    else:
        if sort.split("-")[1] == "true":
            sort = {sort.split("-")[0]: "asc"}
        else:
            sort = {sort.split("-")[0]: "desc"}

    # This variable will store updated list of required fields
    query_fields: str = required_fields

    # For ip_address field, we need to use different mapping
    if "ip_address" in query_fields:
        query_fields = query_fields.replace("ip_address", "ip_address.raw")

    query_fields = query_fields.split("-")

    if required_fields == "allFields":
        search_query: dict = {
            "from": data_part.split("-")[0],
            "size": data_part.split("-")[1],
            "sort": [sort],
            "query": query
        }
    else:
        # Updating search query to search only in specified fields
        query["bool"]["must"]["query_string"]["fields"] = query_fields

        search_query: dict = {
            "from": data_part.split("-")[0],
            "size": data_part.split("-")[1],
            "_source": {
                "include": required_fields.split("-")
            },
            "sort": [sort],
            "query": query
        }

    # First element of data_part array is a starting position to get
    # the data from the database and if the position is zero,
    # that means to get the data from the beginning.
    # Since the data are the same no matter what the position is, we don't need
    # to get data cards data on every call, so we return empty dictionary
    # instead.
    if data_part.split("-")[0] == "0":

        # Function to make multiple function calls concurrently
        # This function will get both data needed for the table in Search view
        # and data for the data cards.
        async def make_multiple_db_calls():
            return await gather(
                get_view_data(search_query),
                get_data_cards_data(query_fields))

        db_calls_results: list = run(make_multiple_db_calls())
    else:
        # Getting only data for the table in Search view
        db_calls_results: list = [run(get_view_data(search_query)), {}]

    processed_data: dict = {}

    # Data for the data cards
    processed_data["data_cards_data"] = db_calls_results[1]

    response: dict = db_calls_results[0]
    if response["valid"]:

        # Data for the table in Search view
        processed_data["table_data"] = response["data"]
        response["data"] = processed_data

    return response


class GetModalData(Resource):
    @user_api
    @swag_from("endpoints_spec/get_modal_data.yml")
    def get(self, index: str, id: str, required_fields: str,
            selected_field: str, search_word: str, data_part: str) -> json:
        try:
            if required_fields == "allFields":
                search_query: dict = {
                    "query": {"match": {
                        "id": {"query": id}
                    }
                    }
                }
            else:
                search_query: dict = {
                    "_source": required_fields.split("-"),
                    "query": {"match": {
                        "id": {"query": id}
                    }
                    }
                }

            if index == "hosts":
                response: dict = run(db_get_hosts(search_query))
            elif index == "events":
                response: dict = run(db_get_events(search_query))
            elif index == "audit":
                response: dict = run(db_get_audit_events(search_query))
            elif index == "changes":
                response: dict = run(db_get_changes(search_query))

            if response["valid"]:

                # This needs to be done because results are returned in dict
                # as a value of key 0 .
                response["data"] = response["data"][0]

                # This must be done so we only get a value without a key
                # This is specific for trivy and openscap data
                if "trivy" == required_fields:
                    response["data"] = response["data"]["trivy"]

                if "openscap" == required_fields:
                    response["data"] = response["data"]["openscap"]

                modal_data: dict = {}

                # List to store all current fields of the data
                modal_data["current_fields"] = []

                # List to store all fields of current host
                modal_data["all_host_fields"] = []

                # Add current fields only if no field is currently selected
                if selected_field == "allFields":
                    # Looping over all keys of host data
                    for key in response["data"]:

                        # Adding all keys into the current_fields list
                        modal_data["current_fields"].append(key)
                else:
                    # Looping over all keys of host data
                    for key in response["data"]:

                        # Adding all keys into the current_fields array stored
                        # in modal_data dictionary
                        modal_data["all_host_fields"].append(key)

                if search_word == "no_search_word":

                    # Add only the value without key if selected_field isn't
                    # equal to "allFields"
                    if selected_field != "allFields":

                        # If there is only one selected field
                        if len(selected_field.split("-")) == 1:
                            response["data"] = response["data"][selected_field]
                        else:
                            multiple_fields: dict = {}
                            for field in selected_field.split("-"):
                                multiple_fields[field] = response["data"][field]

                            if multiple_fields != {}:
                                response["data"] = multiple_fields

                    # If data part is 0-0, return complete data
                    if data_part == "0-0":
                        modal_data["data_length"] = len(str(response["data"]))
                        modal_data["data_for_modal"] = json.dumps(
                            response["data"], indent=1)
                        return modal_data, 200
                    # Otherwise, return only selected part of the data
                    else:
                        modal_data["data_length"] = len(str(response["data"]))
                        modal_data["data_for_modal"] = json.dumps(response["data"], indent=1)[
                            int(data_part.split("-")[0]):int(data_part.split("-")[1])]
                        return modal_data, 200
                else:

                    # List to store all current fields of the data
                    modal_data["current_fields"] = []

                    # Dictionary to store processed data for modal
                    filtered_dictionary: dict = {}

                    # Looping over data
                    for key in response["data"]:

                        # Checking if search word is valid
                        if len(search_word) >= 3:

                            # If value of the field is a list
                            if isinstance(response["data"][key], list):

                                # Set empty list for filtered data
                                filtered_data = []

                                # Loop over the list items and check if it
                                # contains a search word
                                for item in response["data"][key]:

                                    # If they do, add it to the list
                                    if search_word.lower() in str(item).lower():
                                        filtered_data.append(item)

                                        # If key not already in modal_data["current_fields"],
                                        # add it into it. This way when user search for something
                                        # we only display keys containing that
                                        # search word
                                        if key not in modal_data["current_fields"]:
                                            modal_data["current_fields"].append(
                                                key)

                            # If value of the field is a dictionary
                            elif isinstance(response["data"][key], dict):

                                # Set empty dictionary for filtered data
                                filtered_data = {}

                                # Loop over values of all keys and check if it
                                # contains a search word
                                for current_key in response["data"][key]:

                                    # If they do, add it to the dictionary
                                    if search_word.lower() in str(
                                            response["data"][key][current_key]).lower():
                                        filtered_data[current_key] = response["data"][key][current_key]

                                        # If key not already in modal_data["current_fields"],
                                        # add it into it. This way when user search for something
                                        # we only display keys containing that
                                        # search word
                                        if key not in modal_data["current_fields"]:
                                            modal_data["current_fields"].append(
                                                key)
                            else:
                                # For all other types, check for a search word
                                # and set the value of it to the filtered_data
                                # variable if there is a match
                                filtered_data = ""
                                if search_word.lower() in str(
                                        response["data"][key]).lower():
                                    filtered_data = response["data"][key]

                                    # If key not already in modal_data["current_fields"],
                                    # add it into it. This way when user search for something
                                    # we only display keys containing that
                                    # search word
                                    if key not in modal_data["current_fields"]:
                                        modal_data["current_fields"].append(
                                            key)

                        # If the variable isn't empty
                        if filtered_data:

                            # Add it into data variable under it's key
                            filtered_dictionary[key] = filtered_data

                    # Add only the value without key if selected_field isn't
                    # equal to "allFields"
                    if selected_field != "allFields":

                        # If there is only one field selected
                        if len(selected_field.split("-")) == 1:
                            if filtered_dictionary and selected_field in filtered_dictionary:
                                filtered_dictionary = filtered_dictionary[selected_field]
                        else:

                            # Dictionary to store data for all selected fields
                            # that also match the search word
                            multiple_fields: dict = {}

                            for field in selected_field.split("-"):

                                if filtered_dictionary and field in filtered_dictionary:
                                    multiple_fields[field] = filtered_dictionary[field]

                            if multiple_fields != {}:
                                filtered_dictionary = multiple_fields

                    # Check for all occurencies of the search word in host data
                    modal_data["search_word_occurrences"] = str(
                        filtered_dictionary).lower().count(search_word.lower())

                    # If data part is 0-0, return complete data
                    if data_part == "0-0":
                        modal_data["data_length"] = len(
                            str(filtered_dictionary))
                        modal_data["data_for_modal"] = json.dumps(
                            filtered_dictionary, indent=1)
                        return modal_data, 200

                    # Otherwise, return only selected part of the data
                    else:
                        modal_data["data_length"] = len(
                            str(filtered_dictionary))
                        modal_data["data_for_modal"] = json.dumps(filtered_dictionary, indent=1)[
                            int(data_part.split("-")[0]):int(data_part.split("-")[1])]
                        return modal_data, 200

            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class HostsView(Resource):
    @user_api
    @swag_from("endpoints_spec/hosts_view.yml")
    def get(self, query: str, required_fields: str,
            data_part: str, sort: str, query_filter: str) -> json:
        try:
            async def getDataCardsData(query_fields: list):

                data_cards_data: dict = {}
                data_cards_data["total"] = 0
                data_cards_data["linux"] = 0
                data_cards_data["windows"] = 0

                os_summary_query: dict = {
                    "_source": "os",
                    "query": {
                        "query_string":
                            {"query": f"*{query}*",
                             "fields": query_fields}
                    },
                    "aggs": {
                        "os_count": {
                            "terms": {"field": "os.raw"}
                        }
                    }
                }

                os_summary: dict = post_request(
                    ES_HOSTS_URL + "/_search", os_summary_query)
                os_summary = os_summary.json(
                )["aggregations"]["os_count"]["buckets"]

                for os in os_summary:

                    if os["key"] == "windows":
                        data_cards_data["windows"] = os["doc_count"]
                        data_cards_data["total"] += os["doc_count"]

                    elif os["key"] == "linux":
                        data_cards_data["linux"] = os["doc_count"]
                        data_cards_data["total"] += os["doc_count"]

                return data_cards_data

            # If query filter is set to none or total,
            # we want to show all results without filter
            if query_filter not in ["none", "total"]:
                query_filter = {"term": {"os": query_filter}}
            else:
                query_filter = "none"

            data_for_view: dict = get_data_for_view(
                query, query_filter, required_fields, data_part, sort, db_get_hosts, getDataCardsData)

            if data_for_view["valid"]:
                return json.dumps(data_for_view), 200
            else:
                return Response(
                    response=data_for_view["message"],
                    status=data_for_view["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class ContainersView(Resource):
    @user_api
    @swag_from("endpoints_spec/containers_view.yml")
    def get(self, query: str, required_fields: str, data_part: str,
            query_filter: str, sort: str = "none") -> json:
        try:
            async def getDataCardsData():

                data_cards_data: dict = {}
                data_cards_data["docker_images"] = 0
                data_cards_data["total_containers"] = 0
                data_cards_data["running_containers"] = 0
                data_cards_data["paused_containers"] = 0
                data_cards_data["stopped_containers"] = 0

                docker_summary_query: str = {
                    "_source": ["docker_stopped", "docker_paused", "docker_running", "docker_images_count"],
                    "query": {
                        "query_string": {
                            "query": f"*{query}*",
                            "fields": [
                                "id", "hostname",
                                "docker_containers.name", "docker_containers.image", "docker_containers.state", "docker_containers.status",
                                "docker_images.name", "docker_images.size", "docker_images.created",
                                "docker_running", "docker_paused", "docker_stopped"
                            ]
                        }
                    },
                    "aggs": {
                        "docker_stopped": {"sum": {"field": "docker_stopped.raw"}},
                        "docker_paused": {"sum": {"field": "docker_paused.raw"}},
                        "docker_running": {"sum": {"field": "docker_running.raw"}},
                        "docker_images": {"sum": {"field": "docker_images_count"}}
                    }
                }
                docker_summary: dict = post_request(
                    ES_HOSTS_URL + "/_search", docker_summary_query)
                docker_summary = docker_summary.json()["aggregations"]

                data_cards_data["total_containers"] = docker_summary["docker_running"]["value"] + \
                    docker_summary["docker_paused"]["value"] + \
                    docker_summary["docker_stopped"]["value"]
                data_cards_data["running_containers"] = docker_summary["docker_running"]["value"]
                data_cards_data["paused_containers"] = docker_summary["docker_paused"]["value"]
                data_cards_data["stopped_containers"] = docker_summary["docker_stopped"]["value"]
                data_cards_data["docker_images"] = docker_summary["docker_images"]["value"]

                return data_cards_data

            # Setting default query
            search_query = {
                "bool": {
                    "must": {
                        "query_string": {
                            "query": f"*{query}*",
                            "fields": [
                                "id", "hostname",
                                "docker_containers.name", "docker_containers.image", "docker_containers.state", "docker_containers.status",
                                "docker_images.name", "docker_images.size", "docker_images.created",
                                "docker_running.keyword", "docker_paused.keyword", "docker_stopped.keyword"
                            ]
                        }
                    }
                }
            }
            # Split required fields into list
            required_fields = required_fields.split("-")
            if query_filter in ["total_containers", "none"]:
                # For container filters, we want to only show docker containers,
                # so we delete docker_images from results
                if "docker_images" in required_fields:
                    required_fields.pop(required_fields.index("docker_images"))

            elif query_filter == "docker_images":
                # For docker images filter, we want to only show docker images,
                # so we delete docker_containers from results
                if "docker_containers" in required_fields:
                    required_fields.pop(
                        required_fields.index("docker_containers"))

            elif query_filter in ["running_containers", "paused_containers", "stopped_containers"]:

                if "docker_images" in required_fields:
                    required_fields.pop(required_fields.index("docker_images"))

                # Filter out all results not matching selected container state
                search_query["bool"]["filter"] = {
                    "nested": {
                        "path": "docker_containers",
                        "query": {
                            "match": {
                                "docker_containers.state": query_filter.split("_")[0]
                            }
                        }
                    }
                }

            # There is no sorting in container view, so
            # we set it to empty dictionary
            if sort.split("-")[0] == "none":
                sort = {}

            if required_fields == "allFields":
                search_query = {
                    "from": data_part.split("-")[0],
                    "size": data_part.split("-")[1],
                    "sort": [sort],
                    "query": search_query
                }
            else:
                search_query: dict = {
                    "from": data_part.split("-")[0],
                    "size": data_part.split("-")[1],
                    "_source": required_fields,
                    "sort": [sort],
                    "query": search_query
                }

            # Function to make multiple function calls concurrently
            async def make_multiple_db_calls():
                return await gather(
                    db_get_hosts(search_query),
                    getDataCardsData())

            db_calls_results: list = run(make_multiple_db_calls())

            response: dict = db_calls_results[0]
            if response["valid"]:

                table_data: list = []
                for host_data in response["data"]:
                    # Check if host has any docker containers
                    if "docker_containers" in host_data:
                        # Looping over data in docker_containers attribute
                        for container in host_data["docker_containers"]:
                            # Filtering data we want to display
                            filtered_data: dict = {}
                            filtered_data["id"] = host_data["id"]
                            filtered_data["hostname"] = host_data["hostname"]
                            filtered_data["container"] = container["name"]
                            filtered_data["image_name"] = container["image"]
                            if query_filter in [
                                    "running_containers", "paused_containers", "stopped_containers"]:
                                if query_filter.split(
                                        "_")[0] == container["state"]:
                                    filtered_data["state"] = container["state"]
                                else:
                                    continue
                            else:
                                filtered_data["state"] = container["state"]
                            filtered_data["status"] = container["status"]
                            filtered_data["size"] = ""
                            filtered_data["created"] = ""
                            filtered_data["image"] = False
                            if filtered_data != {}:
                                table_data.append(filtered_data)

                    # Check if host has any docker images
                    if "docker_images" in host_data:
                        # Filtering data we want to display
                        for image in host_data["docker_images"]:
                            filtered_data: dict = {}
                            filtered_data["id"] = host_data["id"]
                            filtered_data["hostname"] = host_data["hostname"]
                            filtered_data["container"] = ""
                            filtered_data["image_name"] = image["name"]
                            filtered_data["state"] = ""
                            filtered_data["status"] = ""
                            filtered_data["size"] = image["size"]
                            filtered_data["created"] = image["created"]
                            filtered_data["image"] = True
                            if filtered_data != {}:
                                table_data.append(filtered_data)

                containers_data: dict = {}
                # First element of data_part array is a starting position to get
                # the data from the database and if the position is zero,
                # that means to get the data from the beginning.
                # Since the data are the same no matter what the position is, we don't need
                # to get data cards data on every call but only for the first
                # one
                if data_part.split("-")[0] == "0":
                    containers_data["data_cards_data"] = db_calls_results[1]
                else:
                    containers_data["data_cards_data"] = {}
                containers_data["table_data"] = table_data
                response["data"] = containers_data

                # Adding number of results based on what filter is currently
                # selected
                if query_filter == "docker_images":
                    response["number_of_containers"] = db_calls_results[1]["docker_images"]
                elif query_filter == "running_containers":
                    response["number_of_containers"] = db_calls_results[1]["running_containers"]
                elif query_filter == "paused_containers":
                    response["number_of_containers"] = db_calls_results[1]["paused_containers"]
                elif query_filter == "stopped_containers":
                    response["number_of_containers"] = db_calls_results[1]["stopped_containers"]
                else:
                    response["number_of_containers"] = db_calls_results[1]["total_containers"]

                return json.dumps(response), 200
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class SoftwareView(Resource):
    @user_api
    @swag_from("endpoints_spec/software_view.yml")
    def get(self, query: str, required_fields: str,
            data_part: str, sort: str, query_filter: str) -> json:
        try:
            async def getDataCardsData(query_fields: list):

                data_cards_data: dict = {}
                data_cards_data["total"] = 0
                data_cards_data["linux"] = 0
                data_cards_data["windows"] = 0

                os_summary_query: dict = {
                    "_source": "os",
                    "query": {
                        "query_string":
                            {"query": f"*{query}*",
                             "fields": query_fields}
                    },
                    "aggs": {
                        "os_count": {
                            "terms": {"field": "os.raw"}
                        }
                    }
                }
                os_summary: dict = post_request(
                    ES_HOSTS_URL + "/_search", os_summary_query)
                os_summary = os_summary.json(
                )["aggregations"]["os_count"]["buckets"]

                for os in os_summary:

                    if os["key"] == "windows":
                        data_cards_data["windows"] = os["doc_count"]
                        data_cards_data["total"] += os["doc_count"]

                    elif os["key"] == "linux":
                        data_cards_data["linux"] = os["doc_count"]
                        data_cards_data["total"] += os["doc_count"]

                return data_cards_data

            # If query filter is set to none or total,
            # we want to show all results without filter
            if query_filter not in ["none", "total"]:
                query_filter = {"term": {"os": query_filter}}
            else:
                query_filter = "none"

            data_for_view: dict = get_data_for_view(
                query, query_filter, required_fields, data_part, sort, db_get_hosts, getDataCardsData)

            if data_for_view["valid"]:
                return json.dumps(data_for_view), 200
            else:
                return Response(
                    response=data_for_view["message"],
                    status=data_for_view["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class VulnerabilitiesView(Resource):
    @user_api
    @swag_from("endpoints_spec/vulnerabilities_view.yml")
    def get(self, query: str, required_fields: str,
            data_part: str, sort: str, query_filter: str) -> json:
        try:
            async def getDataCardsData(query_fields: list):

                data_cards_data: dict = {}
                data_cards_data["total_vulnerabilities"] = 0
                data_cards_data["critical_vulnerabilities"] = 0
                data_cards_data["high_vulnerabilities"] = 0

                vulnerabilities_summary_query = {
                    "_source": ["trivy.vulnerabilities_total", "trivy.vulnerabilities_critical", "trivy.vulnerabilities_high"],
                    "query": {
                        "query_string":
                            {"query": f"*{query}*",
                             "fields": query_fields}
                    },
                    "aggs": {
                        "vulnerabilities_total": {"sum": {"field": "trivy.vulnerabilities_total.raw"}},
                        "vulnerabilities_critical": {"sum": {"field": "trivy.vulnerabilities_critical"}},
                        "vulnerabilities_high": {"sum": {"field": "trivy.vulnerabilities_high"}}
                    }
                }
                vulnerabilities_summary = post_request(
                    ES_HOSTS_URL + "/_search", vulnerabilities_summary_query)
                vulnerabilities_summary = vulnerabilities_summary.json()[
                    "aggregations"]

                data_cards_data["total_vulnerabilities"] = vulnerabilities_summary["vulnerabilities_total"]["value"]
                data_cards_data["critical_vulnerabilities"] = vulnerabilities_summary["vulnerabilities_critical"]["value"]
                data_cards_data["high_vulnerabilities"] = vulnerabilities_summary["vulnerabilities_high"]["value"]

                return data_cards_data

            # If query filter is set to none or total_vulnerabilities,
            # we want to show all results without filter
            if query_filter not in ["none", "total_vulnerabilities"]:
                query_filter = {
                    "range": {
                        "trivy.vulnerabilities_" +
                        query_filter.split("_")[0]: {
                            "gt": "0"}}}
            else:
                query_filter = "none"

            data_for_view: dict = get_data_for_view(
                query, query_filter, required_fields, data_part, sort, db_get_hosts, getDataCardsData)

            if data_for_view["valid"]:
                return json.dumps(data_for_view), 200
            else:
                return Response(
                    response=data_for_view["message"],
                    status=data_for_view["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class HostAssessmentView(Resource):
    @user_api
    @swag_from("endpoints_spec/host_assessment_view.yml")
    def get(self, query: str, required_fields: str,
            data_part: str, sort: str, query_filter: str) -> json:
        try:
            async def getDataCardsData(query_fields: list):

                data_cards_data: dict = {}
                data_cards_data["openscap_checks_total"] = 0
                data_cards_data["openscap_pass_total"] = 0
                data_cards_data["openscap_fixed_total"] = 0
                data_cards_data["openscap_fail_total"] = 0

                host_assessment_summary_query = {
                    "_source": query_fields,
                    "query": {
                        "query_string":
                            {"query": f"*{query}*",
                             "fields": query_fields}
                    },
                    "aggs": {
                        "openscap_checks": {"sum": {"field": "openscap.checks.raw"}},
                        "openscap_pass_total": {"sum": {"field": "openscap.pass_total.raw"}},
                        "openscap_fixed_total": {"sum": {"field": "openscap.fixed_total.raw"}},
                        "openscap_fail_total": {"sum": {"field": "openscap.fail_total.raw"}}
                    }
                }
                host_assessment_summary = post_request(
                    ES_HOSTS_URL + "/_search", host_assessment_summary_query)
                host_assessment_summary = host_assessment_summary.json()[
                    "aggregations"]

                data_cards_data["openscap_checks_total"] = host_assessment_summary["openscap_checks"]["value"]
                data_cards_data["openscap_pass_total"] = host_assessment_summary["openscap_pass_total"]["value"]
                data_cards_data["openscap_fixed_total"] = host_assessment_summary["openscap_fixed_total"]["value"]
                data_cards_data["openscap_fail_total"] = host_assessment_summary["openscap_fail_total"]["value"]

                return data_cards_data

            # If query filter is set to none or openscap_checks_total,
            # we want to show all results without filter
            if query_filter not in ["none", "openscap_checks_total"]:
                query_filter = {
                    "range": {
                        "openscap." +
                        query_filter.split("openscap_")[1] +
                        ".raw": {
                            "gt": "0"}}}
            else:
                query_filter = "none"

            data_for_view: dict = get_data_for_view(
                query, query_filter, required_fields, data_part, sort, db_get_hosts, getDataCardsData)

            if data_for_view["valid"]:
                return json.dumps(data_for_view), 200
            else:
                return Response(
                    response=data_for_view["message"],
                    status=data_for_view["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class EventsView(Resource):
    @user_api
    @swag_from("endpoints_spec/events_view.yml")
    def get(self, query: str, required_fields: str,
            data_part: str, sort: str, query_filter: str) -> json:
        try:
            async def getDataCardsData(query_fields: list):

                data_cards_data: dict = {}
                data_cards_data["total_events"] = 0
                data_cards_data["high_impact_events"] = 0
                data_cards_data["medium_impact_events"] = 0
                data_cards_data["low_impact_events"] = 0
                data_cards_data["info_impact_events"] = 0

                event_impact_summary_query: dict = {
                    "_source": "event_impact",
                    "query": {
                        "query_string":
                            {"query": f"*{query}*",
                             "fields": query_fields}
                    },
                    "aggs": {
                        "event_impact_count": {
                            "terms": {"field": "event_impact.raw"}
                        }
                    }
                }
                event_impact_summary: dict = post_request(
                    ES_EVENTS_URL + "/_search", event_impact_summary_query)
                event_impact_summary = event_impact_summary.json(
                )["aggregations"]["event_impact_count"]["buckets"]

                for event_impact in event_impact_summary:

                    if event_impact["key"] == "high":
                        data_cards_data["high_impact_events"] = event_impact["doc_count"]
                        data_cards_data["total_events"] += event_impact["doc_count"]

                    elif event_impact["key"] == "medium":
                        data_cards_data["medium_impact_events"] = event_impact["doc_count"]
                        data_cards_data["total_events"] += event_impact["doc_count"]

                    elif event_impact["key"] == "low":
                        data_cards_data["low_impact_events"] = event_impact["doc_count"]
                        data_cards_data["total_events"] += event_impact["doc_count"]

                    elif event_impact["key"] == "info":
                        data_cards_data["info_impact_events"] = event_impact["doc_count"]
                        data_cards_data["total_events"] += event_impact["doc_count"]

                return data_cards_data

            # If query filter is set to none or total_events,
            # we want to show all results without filter
            if query_filter not in ["none", "total_events"]:
                query_filter = {
                    "term": {
                        "event_impact": query_filter.split("_impact_events")[0]}}
            else:
                query_filter = "none"

            data_for_view: dict = get_data_for_view(
                query, query_filter, required_fields, data_part, sort, db_get_events, getDataCardsData)

            if data_for_view["valid"]:
                return json.dumps(data_for_view), 200
            else:
                return Response(
                    response=data_for_view["message"],
                    status=data_for_view["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class AuditView(Resource):
    @user_api
    @swag_from("endpoints_spec/audit_view.yml")
    def get(self, query: str, required_fields: str,
            data_part: str, sort: str, query_filter: str) -> json:
        try:
            async def getDataCardsData(query_fields: list):
                return {}

            data_for_view: dict = get_data_for_view(
                query, query_filter, required_fields, data_part, sort, db_get_audit_events, getDataCardsData)

            if data_for_view["valid"]:
                return json.dumps(data_for_view), 200
            else:
                return Response(
                    response=data_for_view["message"],
                    status=data_for_view["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class ChangesView(Resource):
    @user_api
    @swag_from("endpoints_spec/changes_view.yml")
    def get(self, query: str, required_fields: str,
            data_part: str, sort: str, query_filter: str) -> json:
        try:
            async def getDataCardsData(query_fields: list):
                return {}

            data_for_view: dict = get_data_for_view(
                query, query_filter, required_fields, data_part, sort, db_get_changes, getDataCardsData)

            if data_for_view["valid"]:
                return json.dumps(data_for_view), 200
            else:
                return Response(
                    response=data_for_view["message"],
                    status=data_for_view["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)
