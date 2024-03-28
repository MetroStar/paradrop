#!/usr/bin/env python3
# autopep8: off
import json, time, sys, os.path
from string import ascii_letters
from random import choices
# Changing path from paradrop/elk to paradrop/api to be able to import things from that folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/api/')
from config.config import ES_HOSTS_URL, ES_USERS_URL, ES_EVENTS_URL, ES_EVENT_TRIGGERS_URL, ES_REPORTS_URL
from db.db_requests import post_request
from utils.id_generator import gen_id

# Specifying number of data we want to seed
number_of_hosts: int = 9999
number_of_users: int = 0
number_of_events: int = 0
number_of_event_triggers: int = 0
number_of_reports: int = 0

# ADDING HOSTS MOCK DATA
hosts_mock_data: list = []
with open("elk/server1.json", 'r') as server_file1:
    hosts_mock_data.append(json.load(server_file1))

with open("elk/server2.json", 'r') as server_file2:
    hosts_mock_data.append(json.load(server_file2))

with open("elk/server3.json", 'r') as server_file3:
    hosts_mock_data.append(json.load(server_file3))

with open("elk/server4.json", 'r') as server_file4:
    hosts_mock_data.append(json.load(server_file4))

while number_of_hosts > 0:
    for data in hosts_mock_data:
        if number_of_hosts > 0:
            data["hostname"] = "".join(choices(ascii_letters, k=10))
            data["id"] = gen_id()
            post_request(ES_HOSTS_URL + "/_doc/", data)
            number_of_hosts -= 1
        else:
            break

# ADDING USERS MOCK DATA
while number_of_users > 0:
    if number_of_users > 0:
        data: dict = {
            "id": "2db4ff61-3075-4721-b2c8-98f59690ae31",
            "name": "admin",
            "email": "admin@paradrop.io",
            "password": "$2a$12$0.5BYEgPH9GTIWiLZlpoXug9RwsPbstM2GTeGGBH3yIAHu8hY5dha",
            "role": "admin",
            "expire_at": "2022-06-25T15:17:49",
            "created_at": "2022-04-26T15:17:49",
            "updated_at": "2022-04-26T15:17:49",
            "last_signin": "2022-04-26T15:17:49",
            "locked": False,
            "reset_password": False
        }
        data["email"] = "".join(choices(ascii_letters, k=10)) + "@paradrop.io"
        data["id"] = gen_id()
        post_request(ES_USERS_URL + "/_doc/", data)
        number_of_users -= 1
        time.sleep(.300)
    else:
        break

# ADDING EVENTS MOCK DATA
while number_of_events > 0:
    if number_of_events > 0:
        data: dict = {
            "event_id": "38db035f-c40a-49c4-8319-fb373c86bf23",
            "id": "d07cad08fe26184300eb8b90a705bb5a753f58986131f577143be53d39a69e40",
            "hostname": "skeeter",
            "ip_address": "192.168.1.3",
            "platform": "ubuntu",
            "asset_type": "notebook",
            "cloud": "",
            "tags": [],
            "timestamp": "2022-04-25T16:59:07",
            "event_name": "low_disk_space",
            "event_message": "diskused_pct = 91 if diskused_pct > 90",
            "event_impact": "high",
            "alert_sent": True,
            "alerts_sent_to": ["slack"]
        }
        data["event_name"] = "".join(choices(ascii_letters, k=10))
        data["id"] = gen_id()
        data["event_id"] = gen_id()
        post_request(ES_EVENTS_URL + "/_doc/", data)
        number_of_events -= 1
        time.sleep(.300)
    else:
        break

# ADDING EVENT TRIGGERS MOCK DATA
while number_of_event_triggers > 0:
    if number_of_event_triggers > 0:
        data: dict = {
            "id": "38db035f-c40a-49c4-8319-fb373c86bf23",
            "event_name": "low_disk_space",
            "send_alert": True,
            "event_impact": "high",
            "event_enable": True,
            "event_trigger": {
                "field": "diskused_pct",
                "operator": ">",
                "expected_value": "90"},
            "created_at": "2022-04-25T16:59:07",
            "created_by": "admin@paradrop.io",
            "updated_at": "2022-04-25T16:59:07",
            "updated_by": "admin@paradrop.io"
        }
        data["event_name"] = "".join(choices(ascii_letters, k=10))
        data["id"] = gen_id()
        post_request(ES_EVENT_TRIGGERS_URL + "/_doc/", data)
        number_of_event_triggers -= 1
        time.sleep(.300)
    else:
        break

# ADDING REPORTS MOCK DATA
while number_of_reports > 0:
    if number_of_reports > 0:
        data: dict = {
            "id": "14vBoULXeqiZcRRTq",
            "report_name": "inventory_report",
            "report_description": "SSP-A13 FedRAMP Integrated Inventory CSV",
            "report_mappings": {
                "Host ID": "id",
                "IP Address": "ip_address",
                "Virtualization": "virtualization",
                "Public": "public",
                "Domain": "domain",
                "Hostname": "hostname",
                "Platform": "platform",
                "Platform Version": "platform_version",
                "Asset Type": "asset_type"},
            "created_at": "2022-04-25T16:59:07",
            "created_by": "admin@paradrop.io",
            "updated_at": "2022-04-25T16:59:07",
            "updated_by": "admin@paradrop.io"
        }
        data["report_name"] = "".join(choices(ascii_letters, k=10))
        data["id"] = gen_id()
        post_request(ES_REPORTS_URL + "/_doc/", data)
        number_of_reports -= 1
        time.sleep(.300)
    else:
        break
