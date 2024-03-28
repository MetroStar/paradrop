#!/usr/bin/env python3
from typing import List
from flask import session
from flask_setup import logger
from config.config import ES_REPORTS_URL
from db.db_requests import post_request, delete_request, get_request
from utils.id_generator import gen_id
from utils.timestamps import gen_timestamp
from utils.audit_events import add_audit_event


async def db_get_reports(query: dict = {"query": {"match_all": {}}}) -> dict:
    """
    Function that returns data about all reports in the database. We can specify
    the database query to get only reports matching a specific keyword or to only
    retrieve part of the data.
    """
    try:
        # Send db request to get data about all reports
        resp = post_request(ES_REPORTS_URL + "/_search/", query)

        # Variable to keep track of the number
        # of all results that match our query
        number_of_results: int = resp.json()["hits"]["total"]["value"]
        reports: List[dict] = []

        # If we found any results
        if number_of_results > 0:
            for e in resp.json()["hits"]["hits"]:
                report: dict = e["_source"]
                report["_id"] = e["_id"]
                reports.append(report)

        if reports == [] or reports == [{}]:
            return {
                "valid": False,
                "code": 404,
                "message": "No reports found in the database..",
                "data": reports,
                "number_of_results": number_of_results}
        else:
            return {
                "valid": True,
                "code": 200,
                "message": "Reports found, returning data..",
                "data": reports,
                "number_of_results": number_of_results}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_add_report(new_report: dict, report_id: str) -> dict:
    """
    Function that accepts data about a new report and then add it into
    the database.
    """
    try:
        # If report id is empty, generate a new one
        if report_id == "":
            report_id = gen_id()
        new_report["id"] = report_id
        new_report["created_at"] = gen_timestamp()
        new_report["created_by"] = session.get("email")
        new_report["updated_at"] = gen_timestamp()
        new_report["updated_by"] = session.get("email")

        # Send db request to add new report
        post_request(ES_REPORTS_URL + "/_doc/" + report_id, new_report)

        # Adding event to Audit index
        add_audit_event(
            event_description=f"CREATED Report with ID {report_id}.")

        return {
            "valid": True,
            "code": 200,
            "message": "Report added succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_update_report(report_update: dict, report_id: str) -> dict:
    """
    Function that accepts data about an existing report and makes an update in the database.
    """
    try:
        current_state: dict = get_request(
            ES_REPORTS_URL + f"/_doc/{report_id}")
        current_state = current_state.json()["_source"]
        report_update["updated_at"] = gen_timestamp()
        report_update["updated_by"] = session.get("email")

        # Send db request to update report
        post_request(ES_REPORTS_URL + "/_doc/" + report_id, report_update)

        # Adding event to Audit index and saving previous state of data into
        # it.
        add_audit_event(
            event_description=f"UPDATED Report with ID {report_id}.",
            previous_state=current_state)

        return {
            "valid": True,
            "code": 200,
            "message": "Report updated succesfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


async def db_delete_report(report_id: str) -> dict:
    """
    Function that accepts id of existing report and deletes it from the database
    """
    try:
        current_state: dict = get_request(ES_REPORTS_URL + "/_doc/" +
                                          report_id).json()
        if current_state["found"]:

            # Send db request to delete user
            delete_request(ES_REPORTS_URL + "/_doc/" + report_id)

            # Adding event to Audit index and saving previous state of data
            # into it.
            add_audit_event(
                event_description=f"DELETED Report with ID {report_id}.",
                previous_state=current_state["_source"])

            return {
                "valid": True,
                "code": 200,
                "message": "Report deleted successfully.."}
        else:
            return {
                "valid": False,
                "code": 404,
                "message": "Report not found.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
