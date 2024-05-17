#!/usr/bin/env python3
from flask_setup import api, logger
from view_resources.search_view import GetModalData, HostsView, ContainersView, SoftwareView, VulnerabilitiesView, HostAssessmentView, EventsView, AuditView, ChangesView
from health_resources.health_check import HealthCheck
from host_resources.add_host import AddHost
from auth_resources.auth_tokens import AddUserToken, GetUserToken, UpdateUserToken, GetAgentToken, UpdateAgentToken#, GetCsrfToken
from configs_resources.configs import ListConfigurations, UpdateConfigurations
from event_resources.event_triggers import ListEventTriggers, AddEventTrigger, UpdateEventTrigger, DeleteEventTrigger
from report_resources.reports import ListHostFields, ListReports, AddReport, UpdateReport, DeleteReport, DownloadReports
from user_resources.users import ListUsers, CreateAccount, AllowPasswordReset, ResetPassword, UpdateUser, DeleteUser
from auth_resources.login import UserLogin, UserLogout
from auth_resources.auth_check import AuthorizationCheck
from typing import Optional


async def add_resources() -> Optional[bool]:
    try:
        # HEALTH CHECK ENDPOINT
        api.add_resource(
            HealthCheck,
            "/v1/health")

        # HOST OPERATIONS ENDPOINTS
        api.add_resource(
            AddHost,
            "/v1/add-host")

        # SEARCH VIEW ENDPOINTS
        api.add_resource(
            GetModalData,
            "/v1/get-modal-data/<string:index>/<string:id>/<string:required_fields>/<string:selected_field>/<string:search_word>/<string:data_part>")

        api.add_resource(
            HostsView,
            "/v1/list-hosts/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        api.add_resource(
            ContainersView,
            "/v1/list-containers/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        api.add_resource(
            SoftwareView,
            "/v1/list-software/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        api.add_resource(
            VulnerabilitiesView,
            "/v1/list-vulnerabilities/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        api.add_resource(
            HostAssessmentView,
            "/v1/list-host-assessment/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        api.add_resource(
            EventsView,
            "/v1/list-events/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        api.add_resource(
            AuditView,
            "/v1/list-audit/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        api.add_resource(
            ChangesView,
            "/v1/list-changes/<string:query>/<string:required_fields>/<string:data_part>/<string:sort>/<string:query_filter>")

        # EVENTS ENDPOINTS
        api.add_resource(
            ListEventTriggers,
            "/v1/list-event-triggers/<string:query>/<string:data_part>/<string:sort>")

        api.add_resource(
            AddEventTrigger,
            "/v1/add-event-triggers")

        api.add_resource(
            UpdateEventTrigger,
            "/v1/update-event-triggers")

        api.add_resource(
            DeleteEventTrigger,
            "/v1/delete-event-triggers")

        # ADDING REPORTS VIEW ENDPOINT
        api.add_resource(
            ListHostFields,
            "/v1/list-host-fields")

        api.add_resource(
            ListReports,
            "/v1/list-reports/<string:query>/<string:data_part>/<string:sort>")

        api.add_resource(
            AddReport,
            "/v1/add-reports")

        api.add_resource(
            UpdateReport,
            "/v1/update-reports")

        api.add_resource(
            DeleteReport,
            "/v1/delete-reports")

        api.add_resource(
            DownloadReports,
            "/v1/download-report/<string:table_headers>/<string:selected_fields>/<string:filename>")

        # ALERT ENDPOINTS
        api.add_resource(ListConfigurations, "/v1/list-configurations")

        api.add_resource(UpdateConfigurations, "/v1/update-configurations")

        # AGENT TOKEN ENDPOINTS
        api.add_resource(
            GetAgentToken,
            "/v1/get-agent-token")

        api.add_resource(
            UpdateAgentToken,
            "/v1/update-agent-token")

        # USER TOKEN ENDPOINTS
        api.add_resource(
            AddUserToken,
            "/v1/add-user-token")

        api.add_resource(
            GetUserToken,
            "/v1/get-user-token")

        api.add_resource(
            UpdateUserToken,
            "/v1/update-user-token")

        # USER OPERATIONS ENDPOINTS
        api.add_resource(
            ListUsers,
            "/v1/list-users/<string:query>/<string:data_part>/<string:sort>")

        api.add_resource(UserLogin, "/v1/user-login")

        api.add_resource(UserLogout, "/v1/logout")

        api.add_resource(AuthorizationCheck, "/v1/authorization-check")

        # api.add_resource(GetCsrfToken, "/v1/get-csrf-token")

        api.add_resource(CreateAccount, "/v1/create-user")

        api.add_resource(UpdateUser, "/v1/update-user")

        api.add_resource(AllowPasswordReset, "/v1/allow-pwd-reset")

        api.add_resource(ResetPassword, "/v1/reset-pwd")

        api.add_resource(DeleteUser, "/v1/delete-user")

        return True

    except Exception as e:
        logger.error(f"Adding API resources failed because of error:{e}")
        exit(1)
