#!/usr/bin/env python3
from typing import Dict, List, Optional, Union
from config.config import FLASK_HOST

# URL of our website
URL = "http://" + FLASK_HOST

# auth_type variable can have different values to simulate requests from different sources
# Possible values are:
# UNAUTHORIZED - request is coming from someone who has no authorization
# READ-ONLY - request is coming from our user that has read-only rights
# ADMIN - request is coming from our user that has admin rights

# So with all three specified, we will run all tests three times: unauthorized,
#  with read-only rights and with admin rights because we are looping through
# this list and running all defined test cases on every iteration. If we want to
# skip all test for non-authorized users, we simply delete {"auth_type": "UNAUTHORIZED", "email":None}
# from auth_types list.

auth_types: List[Union[Dict[str, str], Dict[str, Optional[str]]]] = [{"auth_type": "UNAUTHORIZED", "email": None},
                                                                     {"auth_type": "READ-ONLY",
                                                                         "email": "test@test.com"},
                                                                     {"auth_type": "ADMIN",
                                                                         "email": "testadmin@test.com"}
                                                                     ]

tests = [
    # Format of data we need for testing
    # url - url of route we testing
    # method - method of request
    # code_unauth - status code we expect when request is coming from someone unauthorized
    # code_user - status code we expect when request is coming from our user with read-only rights
    # code_admin - status code we expect when request is coming from our user with admin rights
    # json - data that are required for request in a json format, leave as {} if no data are required
    # for - For what users test is:
    #  Possible values are:
    #   all - test with all types of authorization
    #   UNAUTHORIZED - test as a non-authorized user
    #   READ-ONLY - test as a user with read-only rights
    #   ADMIN - test as a user with admin rights
    #   We can specify as many types we want
    # pause - Some operations like changing password, deleting user, creating user etc. need some time
    #   to apply. We don't want to slow all tests, so I added pause attribute to pause tests only
    #   when we have to do it. It should be set to 0 for no pause.
    # test_case - brief explanation of purpose of the test

    # Generating data needed for testing using user token auth
    # Using user token auth to create admin account that we will use for
    # testing purposes
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"name": "test", "email": "testadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!", "role": "admin"}, "for": ["UNAUTHORIZED"],
        "pause":2, "headers": {"X-Paradrop-Token": "b35bf90e-dd28-4208-8cc5-62ca12c3f5bb", "X-Paradrop-Email": "admin@paradrop.io"},
     "test_case": "Using user token auth to create admin account that we will use for testing purposes"},

    # Using user token auth to add new user token that we will use for testing
    # purposes
    {"url": "/v1/add-user-token", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"email": "testadmin@test.com", "token": "5338d5e4-6f3e-45fe-8af5-e2d96213b3f0"}, "for": ["UNAUTHORIZED"], "pause":2,
     "headers": {"X-Paradrop-Token": "b35bf90e-dd28-4208-8cc5-62ca12c3f5bb", "X-Paradrop-Email": "admin@paradrop.io"},
     "test_case": "Using user token auth to add new user token that we will use for testing purposes"},

    # Using user token auth to set our custom agent token so we can use it to
    # add host
    {"url": "/v1/update-agent-token", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"custom_agent_token": "b97a81c5-3c2b-4a96-8881-38af26dc8407"}, "for": ["UNAUTHORIZED"], "pause":2, "headers": {"X-Paradrop-Token": "b35bf90e-dd28-4208-8cc5-62ca12c3f5bb",
                                                                                                                             "X-Paradrop-Email": "admin@paradrop.io"}, "test_case": "Using user token auth to set our custom agent token so we can use it to add host"},

    # Using user token auth to create user account that we will use for
    # testing purposes
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"name": "test", "email": "test@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!", "role": "read-only"}, "for": ["UNAUTHORIZED"],
     "pause":2, "headers": {"X-Paradrop-Token": "5338d5e4-6f3e-45fe-8af5-e2d96213b3f0", "X-Paradrop-Email": "testadmin@test.com"},
     "test_case": "Using user token auth to create user account that we will use for testing purposes"},

    # Using user token auth to add new event trigger so we don't have an empty
    # index
    {"url": "/v1/add-event-triggers", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"id": "event-trigger-id1", "event_name": "low_disk_space", "send_alert": True, "event_impact": "high", "event_enable": True,
              "event_trigger": {"field": "diskused_pct", "operator": ">", "expected_value": "90"}, "created_at": "2024-04-11T21:57:23Z", "created_by": "admin@paradrop.io",
              "updated_at": "2024-04-11T21:57:23Z", "updated_by": "admin@paradrop.io"}, "for": ["UNAUTHORIZED"], "pause":2,
     "headers": {"X-Paradrop-Token": "5338d5e4-6f3e-45fe-8af5-e2d96213b3f0", "X-Paradrop-Email": "testadmin@test.com"},
     "test_case": "Using user token auth to add event trigger so we don't have an empty index"},

    # Using user token auth to add new report so we don't have an empty index
    {"url": "/v1/add-reports", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"id": "report-id1", "report_description": "Report containing chassis type and cpu count information.",
              "report_mappings": {"Chass. Ty.": "chassis_type", "Cpu C.": "cpu_count"}, "report_name": "Some Report Name"},
     "for": ["UNAUTHORIZED"], "pause":2, "headers": {"X-Paradrop-Token": "5338d5e4-6f3e-45fe-8af5-e2d96213b3f0", "X-Paradrop-Email": "testadmin@test.com"},
     "test_case": "Using user token auth to add new report so we don't have an empty index"},

    # Using user token auth to add new host so we don't have an empty index
    {"url": "/v1/add-host", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"asset_type": "", "audit_rules": [], "chassis_type":"", "cloud":"", "cpu_count":1, "cpu_vulnerabilities":[],
              "clamav_defs":"", "crontabs":[], "diskfree_gb":195, "disktotal_gb":231, "diskused_gb":36, "diskused_pct":91, "dns_nameserver":[],
              "dmesg_errors":[], "docker_containers":[{"name": "perlogix.com", "image": "perlogix.com:20220510", "command": "nginx -g 'daemon off;'", "ports": [], "state":"running", "status":"Up 14 hours"},
                                                      {
                  "name": "filebrowser",
                  "image": "filebrowser/filebrowser",
                  "command": "/filebrowser -t /localhost.pem -k /localhost.key",
                  "ports": [],
                  "state":"running",
                  "status":"Up 14 hours (healthy)"},
         {"name": "kibana",
                  "image": "amazon/opendistro-for-elasticsearch-kibana:latest",
                  "command": "/usr/local/bin/kibana-docker",
                  "ports": [],
                  "state":"running",
                  "status":"Up 14 hours"},
         {"name": "es",
                  "image": "amazon/opendistro-for-elasticsearch:latest",
                  "command": "/usr/local/bin/docker-entrypoint.sh eswrapper",
                  "ports": [],
                  "state":"running",
                  "status":"Up 14 hours"},
         {"name": "bot", "image": "perlogix:bot", "command": "/bot",
             "ports": [], "state":"running", "status":"Up 14 hours"},
         {"name": "contactform-slack", "image": "perlogix:contactform-slack", "command": "/contactform-slack", "ports": [{"IP": "127.0.0.1", "PrivatePort": 8080, "PublicPort": 8080, "Type": "tcp"}],
                  "state": "running", "status": "Up 14 hours"}], "docker_running": 6, "docker_paused": 0, "docker_stopped": 0, "docker_images_count": 21, "docker_images": [{"name": "<none>:<none>", "size": "35.66MB",
                                                                                                                                                                             "created": "2024-04-11T21:57:23Z"}, {"name": "perlogix.com:20220510", "size": "42.58MB", "created": "2024-04-11T21:57:23Z"}, {"name": "<none>:<none>",
                                                                                                                                                                                                                                                                                                                     "size": "42.58MB", "created": "2024-04-11T21:57:23Z"}, {"name": "<none>:<none>", "size": "35.65MB", "created": "2024-04-11T21:57:23Z"}, {"name": "<none>:<none>", "size": "35.66MB",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        "created": "2024-04-11T21:57:23Z"}, {"name": "<none>:<none>", "size": "35.65MB", "created": "2024-03-10T17:04:08-04:00"},
                                                                                                                                                                            {"name": "<none>:<none>", "size": "35.65MB", "created": "2024-03-10T17:04:08-04:00"}, {
                      "name": "<none>:<none>", "size": "35.64MB", "created": "2024-03-09T17:26:53-04:00"},
         {"name": "<none>:<none>", "size": "5.311MB", "created": "2024-03-08T01:16:25-04:00"}, {
             "name": "<none>:<none>", "size": "5.108MB", "created": "2024-03-08T01:16:25-04:00"},
         {"name": "perlogix:bot", "size": "5.311MB", "created": "2024-03-08T01:16:25-04:00"}, {
             "name": "filebrowser/filebrowser:latest", "size": "31.15MB", "created": "2024-03-22T05:11:39-05:00"},
         {"name": "amazon/opendistro-for-elasticsearch:latest", "size": "1.319GB", "created": "2021-12-10T21:19:33-05:00"}, {
             "name": "<none>:<none>", "size": "69.9MB", "created": "2021-11-17T16:42:42-05:00"},
         {"name": "perlogix:contactform-slack", "size": "69.9MB", "created": "2021-11-17T16:42:42-05:00"}, {
             "name": "<none>:<none>", "size": "69.68MB", "created": "2021-11-17T16:42:41-05:00"},
         {"name": "<none>:<none>", "size": "69.68MB", "created": "2021-11-17T16:42:41-05:00"}, {
             "name": "<none>:<none>", "size": "69.9MB", "created": "2021-11-17T16:42:41-05:00"},
         {"name": "<none>:<none>", "size": "5.784MB", "created": "2021-11-17T16:42:41-05:00"}, {
             "name": "<none>:<none>", "size": "69.68MB", "created": "2021-11-17T16:42:41-05:00"},
         {"name": "amazon/opendistro-for-elasticsearch-kibana:latest", "size": "1.166GB", "created": "2021-04-05T17:51:20-04:00"}], "docker_labels": [], "docker_running":0, "docker_paused":0,
         "docker_stopped":0, "docker_images_count":0,
         "docker_images":[], "docker_labels":[], "domain":"", "ec2_ami_id":"", "ec2_availability_zone":"", "ec2_instance_id":"", "ec2_instance_type":"",
         "ec2_profile":"", "ec2_public_ip4":"", "ec2_security_groups":[], "environment":"", "expired_certs":[], "failed_logins":[], "gem":[],
         "hostname":"desktop-win10-1", "id":"c4c3989e55a61e26bee4fe95475355a73124137e439e0cd66e763695e66ec018", "ip_route":[], "ip_address":"192.168.1.165",
         "iptables":[], "network_interfaces":[], "journalctl_logs":[], "kernel_arch":"x86_64", "kernel_version":"10.0.19043 Build 19043",
         "last_run":"2024-03-12T20:15:13-04:00", "load1":0, "load15":0, "load5":0, "loaded_kernel_modules":[], "memoryfree_gb":13,
         "memorytotal_gb":15, "memoryused_gb":2, "memoryused_pct":16, "ntp_servers":[], "ntp_running":False,
         "open_ports":[{"address": "0.0.0.0", "port": 135, "name": "svchost.exe", "protocol": "tcp"}, {"address": "0.0.0.0", "port": 445, "name": "System", "protocol": "tcp"},
                       {"address": "0.0.0.0", "port": 1536, "name": "lsass.exe", "protocol": "tcp"}, {
                           "address": "0.0.0.0", "port": 1537, "name": "wininit.exe", "protocol": "tcp"},
                       {"address": "0.0.0.0", "port": 1538, "name": "svchost.exe", "protocol": "tcp"}, {
             "address": "0.0.0.0", "port": 1539, "name": "svchost.exe", "protocol": "tcp"},
         {"address": "0.0.0.0", "port": 1540, "name": "spoolsv.exe", "protocol": "tcp"}, {
             "address": "0.0.0.0", "port": 1541, "name": "svchost.exe", "protocol": "tcp"},
         {"address": "0.0.0.0", "port": 1542, "name": "services.exe", "protocol": "tcp"}, {
             "address": "0.0.0.0", "port": 2869, "name": "System", "protocol": "tcp"},
         {"address": "0.0.0.0", "port": 5040, "name": "svchost.exe", "protocol": "tcp"}, {
             "address": "0.0.0.0", "port": 5357, "name": "System", "protocol": "tcp"},
         {"address": "0.0.0.0", "port": 5900, "name": "tvnserver.exe", "protocol": "tcp"}, {
             "address": "192.168.1.165", "port": 139, "name": "System", "protocol": "tcp"},
         {"address": "::", "port": 135, "name": "svchost.exe", "protocol": "tcp"}, {
             "address": "::", "port": 445, "name": "System", "protocol": "tcp"},
         {"address": "::", "port": 1536, "name": "lsass.exe", "protocol": "tcp"}, {
             "address": "::", "port": 1537, "name": "wininit.exe", "protocol": "tcp"},
         {"address": "::", "port": 1538, "name": "svchost.exe", "protocol": "tcp"}, {
             "address": "::", "port": 1539, "name": "svchost.exe", "protocol": "tcp"},
         {"address": "::", "port": 1540, "name": "spoolsv.exe", "protocol": "tcp"}, {
             "address": "::", "port": 1541, "name": "svchost.exe", "protocol": "tcp"},
         {"address": "::", "port": 1542, "name": "services.exe", "protocol": "tcp"}, {
             "address": "::", "port": 2869, "name": "System", "protocol": "tcp"},
         {"address": "::", "port": 5357, "name": "System", "protocol": "tcp"}], "openscap": {"status": True, "checks": 0, "pass_total": 0, "fixed_total": 0, "informational_total": 0,
                                                                                             "fail_total": 0, "error_total": 0, "unknown_total": 0, "notchecked_total": 0, "notselected_total": 0, "notapplicable_total": 0, "failed": [], "warnings":[]}, "os":"windows",
         "packages":[], "pip":[], "pip3":[], "platform":"Microsoft Windows 10 Home", "platform_family":"Standalone Workstation", "platform_version":"10.0.19043 Build 19043",
         "processes":[{"pid": 7944, "ppid": 6112, "name": "tvnserver.exe", "user": "WIN10-DESKTOP\\timski"}], "public": False, "snaps": [], "sysctl":[], "systemctl_failed":[], "systemd_timers":[],
         "tags":["PROD=False", "APP=windows-test"], "timezone":"", "trivy":{"vulnerabilities_total": 0, "vulnerabilities_low": 0, "vulnerabilities_medium": 0, "vulnerabilities_high": 0,
                                                                            "vulnerabilities_critical": 0, "vulnerabilities_unknown": 0, "trivy_results": []}, "uptime_days":1, "users":[], "users_loggedin":[],
         "windows_software":[{"display_name": "Windows PC Health Check", "display_version": "3.3.2110.22002", "install_date": "2021-11-13T00:00:00-05:00", "publisher": "Microsoft Corporation"},
                             {"display_name": "Update for Windows 10 for x64-based Systems (KB4023057)", "display_version": "2.63.0.0",
                              "install_date": "2019-11-11T00:00:00-05:00", "publisher": "Microsoft Corporation"},
                             {"display_name": "Update for Windows 10 for x64-based Systems (KB4480730)", "display_version": "2.53.0.0", "install_date": "2019-11-11T00:00:00-05:00",
                              "publisher": "Microsoft Corporation"}, {"display_name": "Microsoft Update Health Tools", "display_version": "3.67.0.0", "install_date": "2024-03-05T00:00:00-04:00",
                                                                      "publisher": "Microsoft Corporation"}, {"display_name": "Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.24.28127", "display_version": "14.24.28127",
                                                                                                              "install_date": "2020-10-31T00:00:00-04:00", "publisher": "Microsoft Corporation"}, {"display_name": "Microsoft Visual C++ 2019 X64 Additional Runtime - 14.24.28127",
                                                                                                                                                                                                   "display_version": "14.24.28127", "install_date": "2020-10-31T00:00:00-04:00", "publisher": "Microsoft Corporation"}, {"display_name": "TightVNC", "display_version": "2.8.59.0",
                                                                                                                                                                                                                                                                                                                          "install_date": "2021-07-03T00:00:00-04:00", "publisher": "GlavSoft LLC."}, {"display_name": "Google Chrome", "display_version": "101.0.4951.64",
                                                                                                                                                                                                                                                                                                                                                                                                       "install_date": "2024-03-11T00:00:00-04:00", "publisher": "Google LLC"}, {"display_name": "Microsoft Edge", "display_version": "101.0.1210.39", "install_date": "2024-03-07T00:00:00-04:00",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 "publisher": "Microsoft Corporation"}, {"display_name": "Microsoft Visual C++ 2015-2019 Redistributable (x64) - 14.24.28127", "display_version": "14.24.28127.4",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         "install_date": "0001-01-01T00:00:00Z", "publisher": "Microsoft Corporation"}, {"display_name": "Microsoft Visual C++ 2019 X86 Minimum Runtime - 14.24.28127",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         "display_version": "14.24.28127", "install_date": "2020-10-31T00:00:00-04:00", "publisher": "Microsoft Corporation"}, {"display_name": "Google Update Helper", "display_version": "1.3.36.31",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "install_date": "2020-10-31T00:00:00-04:00", "publisher": "Google LLC"}, {"display_name": "Microsoft Visual C++ 2015-2019 Redistributable (x86) - 14.24.28127",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          "display_version": "14.24.28127.4", "install_date": "0001-01-01T00:00:00Z", "publisher": "Microsoft Corporation"},
                             {"display_name": "Microsoft Visual C++ 2019 X86 Additional Runtime - 14.24.28127", "display_version": "14.24.28127", "install_date": "2020-10-31T00:00:00-04:00",
                              "publisher": "Microsoft Corporation"}, {"display_name": "Intel(R) Processor Graphics", "display_version": "10.18.10.5161", "install_date": "0001-01-01T00:00:00Z",
                                                                      "publisher": "Intel Corporation"}, {"display_name": "Realtek High Definition Audio Driver", "display_version": "6.0.9151.1", "install_date": "0001-01-01T00:00:00Z",
                                                                                                          "publisher": "Realtek Semiconductor Corp."}], "virtualization": False, "virtualization_system": ""},
     "for": ["UNAUTHORIZED"], "pause":2,
     "headers": {"X-Paradrop-Token": "b97a81c5-3c2b-4a96-8881-38af26dc8407"},
     "test_case": "Using user token auth to add new host so we don't have an empty index"},

    # Api routes
    # Testing access

    {"url": "/v1/get-modal-data/hosts/c4c3989e55a61e26bee4fe95475355a73124137e439e0cd66e763695e66ec018/*/allFields/no_search_word/0-200000",
     "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200, "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-hosts/*/id-hostname-ip_address-docker_containers-os-platform-asset_type-cloud-tags-last_run/0-20/none-false/none", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-events/*/allFields/0-20/none-false/none", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-audit/*/allFields/0-20/none-false/none", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-vulnerabilities/*/id-hostname-ip_address-platform-trivy-last_run/0-20/none-false/none", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-host-assessment/*/id-hostname-ip_address-platform-openscap-last_run/0-20/none-false/none", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-containers/*/id-hostname-docker_containers-docker_images-docker_running-docker_paused-docker_stopped/0-20/none-false/none", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-software/*/id-hostname-ip_address-docker_containers-os-platform-asset_type-cloud-tags-last_run/0-20/none-false/none", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-event-triggers/*/0-20/none-false", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-reports/*/0-20/none-false", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/list-users/*/0-20/none-false", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    {"url": "/v1/authorization-check", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Access"},

    # Testing login
    # CAUTION: Succesful login will change session cookie and tests might not run
    # properly!

    # Login - Wrong password
    {"url": "/v1/user-login", "method": "POST", "code_unauth": 401, "code_user": 401, "code_admin": 401,
     "json": {"email": "admin@paradrop.io", "pwd": "asdsadad"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Login - Wrong password"},

    # Login - Wrong email and password
    {"url": "/v1/user-login", "method": "POST", "code_unauth": 404, "code_user": 404, "code_admin": 404,
     "json": {"email": "adasdasdas", "pwd": "asdadasds"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Login - Wrong email and password"},

    # Login - Request with empty data"
    {"url": "/v1/user-login", "method": "POST", "code_unauth": 404, "code_user": 404, "code_admin": 404,
     "json": {"email": "adasdasdas", "pwd": "asdadasds"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Login - Request with empty data"},

    # Login - Request without data
    {"url": "/v1/user-login", "method": "POST", "code_unauth": 404, "code_user": 404, "code_admin": 404,
     "json": {"email": "", "pwd": ""}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Login - Request without data"},

    # Testing creating users
    # Create - Creating user and passwords don't match
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"name": "test", "email": "test@gmail.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!s", "role": "admin"}, "for": ["all"],
     "pause":0, "pause":0, "headers": "", "test_case": "Create - Creating user and passwords don't match"},

    # Create - Creating user with valid data
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"name": "test", "email": "test@gmail.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!", "role": "admin"}, "for": ["all"],
        "pause":1, "headers": "", "test_case": "Create - Creating user with valid data"},

    # Create - Creating user with email that's already in use
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"name": "test", "email": "test@gmail.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!", "role": "admin"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Create - Creating user with email that's already in use"},

    # Create - Creating user without name
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"name": "", "email": "noname@gmail", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!", "role": "admin"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Create - Creating user without name"},

    # Create - Creating user without password
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"name": "name", "email": "nopass@gmail", "pwd1": "", "pwd2": "", "role": "admin"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Create - Creating user without password"},

    # Create - Request empty parameters
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"name": "", "email": "", "pwd1": "", "pwd2": "", "role": ""}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Create - Request empty parameters"},

    # Create - Request without data
    {"url": "/v1/create-user", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Create - Request without data"},

    # Testing updating user data

    # Update user data - With valid data - ADMIN only
    {"url": "/v1/update-user", "method": "PUT", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {"email": "updatedtestadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["ADMIN"],
     "pause":3, "headers": "", "test_case": "Update user data - With valid data - ADMIN only"},

    # Update user data - With valid data - USER only
    {"url": "/v1/update-user", "method": "PUT", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {"email": "updatedtest@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["READ-ONLY"],
     "pause":3, "headers": "", "test_case": "Update user data - With valid data - USER only"},

    # Update user data back to old values - ADMIN only
    {"url": "/v1/update-user", "method": "PUT", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {"email": "testadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["ADMIN"],
     "pause":3, "headers": "", "test_case": "Update user data back to old values - ADMIN only"},

    # Update user data back to old values - USER only
    {"url": "/v1/update-user", "method": "PUT", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {"email": "test@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["READ-ONLY"],
     "pause":3, "headers": "", "test_case": "Update user data back to old values - USER only"},

    # Update password - Reset password with empty values
    {"url": "/v1/reset-pwd", "method": "PUT", "code_unauth": 400, "code_user": 400, "code_admin": 400,
     "json": {"email": "", "pwd1": "", "pwd2": ""}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Update password - Reset password with empty values"},

    # Update password - Reset password with no data
    {"url": "/v1/reset-pwd", "method": "PUT", "code_unauth": 400, "code_user": 400, "code_admin": 400,
     "json": {}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Update password - Reset password with no data"},

    # Update password - Reset password without reset_password attribute set to
    # True
    {"url": "/v1/reset-pwd", "method": "PUT", "code_unauth": 400, "code_user": 400, "code_admin": 400,
     "json": {"email": "testadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Update password - Reset password without reset_password attribute set to True"},

    # Update password - Allow password reset
    {"url": "/v1/allow-pwd-reset", "method": "PUT", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"email": "testadmin@test.com"}, "for": ["all"],
     "pause":1, "headers": "", "test_case": "Update password - Allow password reset"},

    # Update password - Reset password with passwords not matching
    {"url": "/v1/reset-pwd", "method": "PUT", "code_unauth": 400, "code_user": 400, "code_admin": 400,
     "json": {"email": "testadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!s"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Update password - Reset password with paswords not matching"},

    # Update password - Reset password - ADMIN only
    {"url": "/v1/reset-pwd", "method": "PUT", "code_unauth": 200, "code_user": 200, "code_admin": 200,
     "json": {"email": "testadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["ADMIN"],
     "pause":1, "headers": "", "test_case": "Update password - Reset testadmin@test.com password"},

    # Update password - Allow password reset again - ADMIN only
    {"url": "/v1/allow-pwd-reset", "method": "PUT", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"email": "testadmin@test.com"}, "for": ["ADMIN"],
     "pause":1, "headers": "", "test_case": "Update password - Allow password reset AGAIN"},

    # Update password - Reset password AGAIN back to the old one - ADMIN only
    {"url": "/v1/reset-pwd", "method": "PUT", "code_unauth": 200, "code_user": 200, "code_admin": 200,
     "json": {"email": "testadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["ADMIN"],
     "pause":1, "headers": "", "test_case": "Update password - Reset password AGAIN back to the old one"},

    # Update user data - Using email of the user that already exists
    {"url": "/v1/update-user", "method": "PUT", "code_unauth": 401, "code_user": 400, "code_admin": 400,
     "json": {"email": "testadmin@test.com", "pwd1": "Paradrop123456789!", "pwd2": "Paradrop123456789!"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Update user data - Using email of the user that already exists"},

    # Update user data - Using wrong password
    {"url": "/v1/update-user", "method": "PUT", "code_unauth": 401, "code_user": 401, "code_admin": 401,
     "json": {"email": "new@email.io", "pwd1": "sdfsdafas", "pwd2": "sdfsdafas"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Update user data - Wrong password"},

    # Update user data - Empty request
    {"url": "/v1/update-user", "method": "PUT", "code_unauth": 401, "code_user": 400, "code_admin": 400,
     "json": {}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Update user data - Empty request"},


    # Testing deleting user data
    # Delete - Delete user that doesn't exist
    {"url": "/v1/delete-user", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 404,
     "json": {"email": "noexisto@gmail.com"}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Delete - Delete user that doesnt exist"},

    # Hosts API test
    # Updating configurations through update-configurations endpoint
    # Trying to change configurations with valid data
    {"url": "/v1/update-configurations", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"alert_email": "testing@gmail.com", "email_enable": True}, "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to change configurations with valid data"},

    # Trying to change configurations with non-valid data
    {"url": "/v1/update-configurations", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"alert_email": "testing@gmail.com", "non_existent_field": False, "email_enable": False},
     "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to change alert configuration with non-valid data"},

    # Trying to change configurations with non-valid data type
    {"url": "/v1/update-configurations", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"email_enable": "string"}, "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to change alert configuration with non-valid data type"},

    # Trying to change configurations with valid data back to old values
    {"url": "/v1/update-configurations", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"alert_email": "", "email_enable": False}, "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to change configurations with valid data back to old values"},

    # Event Triggers Action tests
    # Add Event Triggers test cases
    # Trying to add event trigger with valid data
    {"url": "/v1/add-event-triggers", "method": "POST", "code_unauth": 200, "code_user": 403, "code_admin": 200,
     "json": {"id": "event-trigger-id2", "event_name": "low_disk_space", "send_alert": True, "event_impact": "high", "event_enable": True,
              "event_trigger": {"field": "diskused_pct", "operator": ">", "expected_value": "90"}, "created_at": "2024-04-11T21:57:23Z", "created_by": "admin@paradrop.io",
              "updated_at": "2024-04-11T21:57:23Z", "updated_by": "admin@paradrop.io"}, "for": ["UNAUTHORIZED"], "pause":2,
     "headers": {"X-Paradrop-Token": "5338d5e4-6f3e-45fe-8af5-e2d96213b3f0", "X-Paradrop-Email": "testadmin@test.com"},
     "test_case": "Trying to add event trigger with valid data"},

    # Trying to add event trigger with non-valid data
    {"url": "/v1/add-event-triggers", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"event_name": "low_disk_space", "send_alert": True, "event_impact": "high", "event_enable": True,
              "e_trigger": {"field": "diskused_pct", "operator": ">", "expected_value": "90"}, "created_at": "2024-03-25",
              "created_by": "admin@paradrop.io", "updated_at": "2024-03-25", "updated_by": "admin@paradrop.io"}, "for": ["all"], "pause":0,
     "headers": "", "test_case": "Trying to add event trigger with non-valid data"},

    # Update Event Triggers test cases
    # Trying to update event trigger with valid data
    {"url": "/v1/update-event-triggers", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"event_name": "low_disk_space", "send_alert": True, "event_impact": "high", "event_enable": True,
              "event_trigger": {"field": "diskused_pct", "operator": ">", "expected_value": "90"}, "created_at": "2024-03-25",
              "created_by": "admin@paradrop.io", "updated_at": "2024-03-25", "updated_by": "admin@paradrop.io", "id": "event-trigger-id2"},
     "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to update event trigger with valid data"},

    # Trying to update event trigger with non-valid data
    {"url": "/v1/update-event-triggers", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"event_name": "low_disk_space", "send_alert": True, "event_impact": "high", "event_enable": True,
              "e_trigger": {"field": "diskused_pct", "operator": ">", "expected_value": "90"}, "created_at": "2024-03-25",
              "created_by": "admin@paradrop.io", "updated_at": "2024-03-25", "updated_by": "admin@paradrop.io", "id": "event-trigger-id2"},
     "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to update event trigger with non-valid data"},

    # Report builder tests
    # Add Reports test cases
    # Trying to add report with valid data
    {"url": "/v1/add-reports", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"id": "report-id2", "report_description": "Report containing chassis type and cpu count information.",
              "report_mappings": {"Chass. Ty.": "chassis_type", "Cpu C.": "cpu_count"}, "report_name": "Some Report Name"}, "for": ["all"], "pause":0,
     "headers": "", "test_case": "Trying to add report with valid data"},

    # Trying to add report with non-valid data
    {"url": "/v1/add-reports", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"report_nme": "R1", "report_filename": "r1", "report_description": "test report",
              "report_mappings": {"Asset": "asset_type", "Clouds": "cloud"}, "created_at": "2024-03-25",
              "created_by": "admin@paradrop.io", "updated_at": "2024-03-25", "updated_by": "admin@paradrop.io"}, "for": ["all"], "pause":0,
     "headers": "", "test_case": "Trying to add report with non-valid data"},

    # Update Reports test cases
    # Trying to update report with valid data
    {"url": "/v1/update-reports", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"id": "report-id1", "report_description": "Report containing chassis type and cpu count information.",
              "report_mappings": {"Chass. Ty.": "chassis_type", "Cpu C.": "cpu_count"}, "report_name": "Some Report Name", "created_at": "2024-03-25",
              "created_by": "testadmin@test.com"}, "for": ["all"], "pause":0,
     "headers": "", "test_case": "Trying to update report with valid data"},

    # Trying to update report with non-valid data
    {"url": "/v1/update-reports", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 400,
     "json": {"id": "report-id1", "report_description": "Report containing chassis type and cpu count information.",
              "report_mappings": {"Chass. Ty.": "chassis_type", "Cpu C.": "cpu_count"}, "report_name": "Some Report Name"}, "for": ["all"], "pause":0,
     "headers": "", "test_case": "Trying to update report with non-valid data"},

    # Trying to download report
    {"url": "/v1/download-report/HostID/id/inventory_report.csv", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Downloading report"},

    # AUTH TOKENS API test
    # AGENT TOKENS TEST
    # Trying to get the agent token
    {"url": "/v1/get-agent-token", "method": "GET", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to get the agent token"},

    # Trying to update the agent token
    {"url": "/v1/update-agent-token", "method": "POST", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to update the agent token"},

    # USER TOKENS TEST
    # Trying to update the user token
    {"url": "/v1/update-user-token", "method": "POST", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":1, "headers": "", "test_case": "Trying to update the user token"},

    # Trying to get the user token
    {"url": "/v1/get-user-token", "method": "GET", "code_unauth": 401, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to get the user token"},

    # DELETING DATA CREATED FOR TESTING PURPOSES
    # Delete Event Triggers test cases
    # Trying to delete existing event trigger
    {"url": "/v1/delete-event-triggers", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"id": "event-trigger-id1"},
     "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to delete existing event trigger"},

    {"url": "/v1/delete-event-triggers", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"id": "event-trigger-id2"},
     "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to delete existing event trigger"},

    # Delete Report test cases
    # Trying to delete existing report
    {"url": "/v1/delete-reports", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"id": "report-id1"},
     "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to delete existing report"},

    {"url": "/v1/delete-reports", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"id": "report-id2"},
     "for": ["all"], "pause":0, "headers": "", "test_case": "Trying to delete existing report"},


    # Deleting users we created for testing purposes
    # Delete - Delete admin user we created previously - ADMIN only
    {"url": "/v1/delete-user", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"email": "test@test.com"}, "for": ["ADMIN"],
     "pause":1, "headers": "", "test_case": "Delete - Delete admin user we created previously - ADMIN only"},

    # Delete - Delete test user we created previously - ADMIN only
    {"url": "/v1/delete-user", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"email": "test@gmail.com"}, "for": ["ADMIN"],
     "pause":1, "headers": "", "test_case": "Delete - Delete admin user we created previously - ADMIN only"},

    # Delete - Delete user we created previously - ADMIN only
    {"url": "/v1/delete-user", "method": "DELETE", "code_unauth": 401, "code_user": 403, "code_admin": 200,
     "json": {"email": "testadmin@test.com"}, "for": ["ADMIN"],
     "pause":1, "headers": "", "test_case": "Delete - Delete user we created previously - ADMIN only"},

    # Logout test - has to be in the end because it will reset session email
    # Logout - logout user
    {"url": "/v1/logout", "method": "GET", "code_unauth": 200, "code_user": 200, "code_admin": 200,
     "json": {}, "for": ["all"],
     "pause":0, "headers": "", "test_case": "Logout - Logout user"}
]

# Success and Error messages to save to log_file
success_message = """
Auth type: {}
Test case : {}
URL : {}
Method : {}
Expected code : {}
Response code : {}
Response message: {}
OK!\n
"""

fail_message = """
Auth type: {}
Test case : {}
URL : {}
Method : {}
Expected code : {}
Response code : {}
Response message: {}
Error message : {}
FAILED!\n
"""

# Test count to save to log_file
test_count = """
All tests: {}
Succesful tests: {}
Failed tests: {}
"""
