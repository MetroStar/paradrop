#!/usr/bin/env python3
from flask import Response, request, make_response
from flask_restful import Resource
import json
from csv import writer as csv_writer
from io import StringIO
from typing import List
from asyncio import run
from flask_setup import logger
from flasgger import swag_from
from db.hosts import db_get_hosts
from db.reports import db_get_reports, db_add_report, db_update_report, db_delete_report
from api_auth import user_api, admin_api


class ListHostFields(Resource):
    @user_api
    @swag_from("endpoints_spec/list_host_fields.yml")
    def get(self) -> json:
        try:
            # List all keys in host dictionary
            response: dict = run(db_get_hosts())
            if response["valid"]:
                all_host_fields: dict = {}
                for field in response["data"][0].keys():
                    # Transfer all words to title case and replace _ with
                    # spaces
                    all_host_fields[field.replace("_", " ").title()] = field
                return json.dumps(all_host_fields), 200
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class ListReports(Resource):
    @user_api
    @swag_from("endpoints_spec/list_reports.yml")
    def get(self, query: str, data_part: str, sort: str) -> json:
        try:
            # If sorting specifications are specificed,
            # convert it to correct format
            if sort.split("-")[0] == "none":
                sort = {}
            else:
                if sort.split("-")[1] == "true":
                    sort = {sort.split("-")[0]: "asc"}
                else:
                    sort = {sort.split("-")[0]: "desc"}

            search_query: dict = {
                "from": data_part.split("-")[0],
                "size": data_part.split("-")[1],
                "sort": [sort],
                "query": {
                    "query_string": {
                        "query": f"*{query}*",
                        "fields": ["report_name", "report_description"]
                    }
                }
            }
            response: dict = run(db_get_reports(search_query))
            if response["valid"]:
                response_data: dict = {}
                response_data["data"] = response["data"]
                response_data["number_of_results"] = response["number_of_results"]
                return json.dumps(response_data), 200
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class AddReport(Resource):
    @admin_api
    @swag_from("endpoints_spec/add_report.yml")
    def post(self) -> Response:
        try:
            report_data: dict = request.json
            if report_data:

                # If request data contain ID, use it as the report id
                report_id: str = ""
                if "id" in report_data:
                    report_id = report_data["id"]

                new_report: dict = {}
                # Transfer all words to title case and replace _ with spaces
                new_report["report_name"] = report_data["report_name"].replace(
                    " ", "_").lower()
                new_report["report_description"] = report_data["report_description"]
                new_report["report_mappings"] = report_data["report_mappings"]

                response: dict = run(db_add_report(new_report, report_id))
                if response["valid"]:
                    return Response(
                        response=response["message"],
                        status=response["code"])
                else:
                    return Response(
                        response=response["message"],
                        status=response["code"])
            else:
                return Response(response="Required data are missing..",
                                status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class UpdateReport(Resource):
    @admin_api
    @swag_from("endpoints_spec/update_report.yml")
    def post(self) -> Response:
        try:
            report_data: dict = request.json
            if report_data:
                report_update: dict = {}
                report_update["id"] = report_data["id"]
                report_update["report_name"] = report_data["report_name"]
                report_update["report_description"] = report_data["report_description"]
                report_update["report_mappings"] = report_data["report_mappings"]
                report_update["created_at"] = report_data["created_at"]
                report_update["created_by"] = report_data["created_by"]
                response: dict = run(
                    db_update_report(
                        report_update,
                        report_data["id"]))

                if response["valid"]:
                    return Response(
                        response=response["message"],
                        status=response["code"])
                else:
                    return Response(
                        response=response["message"],
                        status=response["code"])
            else:
                return Response(response="Required data are missing..",
                                status=400)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class DeleteReport(Resource):
    @admin_api
    @swag_from("endpoints_spec/delete_report.yml")
    def delete(self) -> Response:
        try:
            report_data: dict = request.json
            if report_data:
                report_id: str = report_data["id"]
            else:
                return Response(response="Required data are missing..",
                                status=400)

            response: dict = run(db_delete_report(report_id))
            if response["valid"]:
                return Response(
                    response=response["message"],
                    status=response["code"])
            else:
                return Response(
                    response=response["message"],
                    status=response["code"])

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)


class DownloadReports(Resource):
    @user_api
    @swag_from("endpoints_spec/download_reports.yml")
    def get(self, table_headers: List[str],
            selected_fields: List[str], filename: str) -> Response:
        try:
            table_headers = table_headers.split("-")
            selected_fields = selected_fields.split("-")

            search_query: dict = {
                "_source": selected_fields,
                "query": {"match_all": {}}
            }

            response: dict = run(db_get_hosts(search_query))
            if response["valid"]:
                # Saving CSV into memory so we don't have to store the file
                csv_report = StringIO()

                # Creating writer for csv file
                writer = csv_writer(csv_report)

                # Headers of the CSV table
                csv_header: List[str] = table_headers
                writer.writerow(csv_header)

                # Loop over data and add it into the csv file
                for data in response["data"]:
                    all_fields: list = []
                    for field in selected_fields:
                        all_fields.append(data[field])
                    writer.writerow(all_fields)

                # Returning csv file to the user to download
                send_csv_file: Response = make_response(csv_report.getvalue())
                filename = filename.replace(" ", "_").lower()

                # Setting the filename and headers
                csv_filename: str = f"attachment; filename={filename}.csv"
                send_csv_file.headers['Content-Disposition'] = csv_filename
                send_csv_file.mimetype = 'text/csv'
                return send_csv_file
            else:
                return Response(response="Report not found..",
                                status=404)

        except BaseException as e:
            logger.error(e)
            return Response(response=f"Something went wrong..:{e}",
                            status=400)
