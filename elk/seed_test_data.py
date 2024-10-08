#!/usr/bin/env python3
# autopep8: off
import json, time, sys, os.path
from string import ascii_letters
from random import randint, choices
from datetime import datetime, timezone

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
hostnames: dict = {}

def generate_lastrun() -> str:
    return datetime.now(timezone.utc).isoformat()[:-13] + 'Z'

def generate_ip() -> str:
  base_ip = "192.168."

  third_octet = randint(1, 254)
  fourth_octet = randint(1, 255)

  return f"{base_ip}{third_octet}.{fourth_octet}"

def hostname_incr(hostname) -> str:
    try:
        current_number = int(hostname.split("-")[-1])
    except ValueError:
        current_number = 0

    host_split = hostname.split("-")
    host_prefix = "-".join(host_split[:2]) + "-"

    while True:
        new_hostname = host_prefix + str(current_number)
        if new_hostname not in hostnames:
            hostnames[new_hostname] = ""
            return new_hostname
        else:
            current_number += 1

# ADDING HOSTS MOCK DATA
hosts_mock_data: list = []
with open("elk/notebook-ubuntu20-1.json", 'r') as server_file1:
    hosts_mock_data.append(json.load(server_file1))

with open("elk/desktop-clear-1.json", 'r') as server_file2:
    hosts_mock_data.append(json.load(server_file2))

with open("elk/pi4-ubuntu20-1.json", 'r') as server_file3:
    hosts_mock_data.append(json.load(server_file3))

with open("elk/desktop-win10-1.json", 'r') as server_file4:
    hosts_mock_data.append(json.load(server_file4))

with open("elk/vm-centos8-1.json", 'r') as server_file5:
    hosts_mock_data.append(json.load(server_file5))

with open("elk/vm-centos9-1.json", 'r') as server_file6:
    hosts_mock_data.append(json.load(server_file6))

with open("elk/vm-rocky9-1.json", 'r') as server_file7:
    hosts_mock_data.append(json.load(server_file7))

with open("elk/vm-winsrv2022-1.json", 'r') as server_file8:
    hosts_mock_data.append(json.load(server_file8))

with open("elk/desktop-win11-1.json", 'r') as server_file9:
    hosts_mock_data.append(json.load(server_file9))

while number_of_hosts > 0:
    for data in hosts_mock_data:
        if number_of_hosts > 0:
            data["hostname"] = hostname_incr(data["hostname"])
            data["ip_address"] = generate_ip()
            data["id"] = gen_id()
            data["last_run"] = generate_lastrun()
            print(data["hostname"] + " " + post_request(ES_HOSTS_URL + "/_doc/", data).text)
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
            "expire_at": "2024-03-25T15:17:49",
            "created_at": "2024-03-26T15:17:49",
            "updated_at": "2024-03-26T15:17:49",
            "last_signin": "2024-03-26T15:17:49",
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
            "hostname": "notebook-ubuntu20-1",
            "ip_address": "192.168.1.3",
            "platform": "ubuntu",
            "asset_type": "notebook",
            "cloud": "",
            "tags": [],
            "timestamp": "2024-04-11T21:57:23Z",
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
            "created_at": "2024-04-11T21:57:23Z",
            "created_by": "admin@paradrop.io",
            "updated_at": "2024-04-11T21:57:23Z",
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
            "created_at": "2024-04-11T21:57:23Z",
            "created_by": "admin@paradrop.io",
            "updated_at": "2024-04-11T21:57:23Z",
            "updated_by": "admin@paradrop.io"
        }
        data["report_name"] = "".join(choices(ascii_letters, k=10))
        data["id"] = gen_id()
        post_request(ES_REPORTS_URL + "/_doc/", data)
        number_of_reports -= 1
        time.sleep(.300)
    else:
        break
