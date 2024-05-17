#!/bin/sh
# shellcheck disable=SC2016

USER="admin"
PASSWD='dtYe2cKY2YtyBEJ49a'

# Seed Mock Data to paradrop_hosts Index
curl -k -u "$USER:$PASSWD" -XPUT 'https://127.0.0.1:9200/paradrop_hosts'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_close'

curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_settings' -d @es_settings.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_open'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_mapping' -d @./mappings/paradrop_hosts_mapping.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/d07cad08fe26184300eb8b90a705bb5a753f58986131f577143be53d39a69e40' -d @./hosts/notebook-ubuntu20-1.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/15a7117d10552dfa2aec759d76628397f1c73dd9069c9623136f43fbbf325f16' -d @./hosts/desktop-clear-1.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/b7d523dab0f328039d889160823f9cf58574dbb9ac454daa033ff37ec4e7fdc1' -d @./hosts/pi4-ubuntu20-1.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/c4c3989e55a61e26bee4fe95475355a73124137e439e0cd66e763695e66ec018' -d @./hosts/desktop-win10-1.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/77f26a9d6a23d47fe328597c29fede19231ee1a28cc0668b6f634d1a77e80f99' -d @./hosts/vm-centos8-1.json
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/7df309c1722acd385c8c0eb6c2b3b02b853556998b71317ab304ad914740a74e' -d @./hosts/vm-centos9-1.json
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/fff03470dacec51e21fcb7dcdae3e86c9ff764ff8aab0baf1ac6199aaa6570d9' -d @./hosts/vm-rocky9-1.json
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/9d1b098f1a14c3a8b5192f552e5c4e9a185055a0144f9b44a7671c54cf7dec41' -d @./hosts/vm-winsrv2022-1.json
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/efdc88abb696c777d6242161194aadb7c1c94fcfd7013e9058a05501f993f010' -d @./hosts/demo.paradrop.io.json
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/70048f0024b3dcf1367df019b787be477af37cb03b11ea0f5add348af6f7e575' -d @./hosts/desktop-win11-1.json


# Seed Mock Data to paradrop_users Index
curl -k -u "$USER:$PASSWD" -XPUT 'https://127.0.0.1:9200/paradrop_users'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_close'

curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_settings' -d @es_settings.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_open'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_mapping' -d @./mappings/paradrop_users_mapping.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_doc/2db4ff61-3075-4721-b2c8-98f59690ae31' -d \
'{
  "id": "2db4ff61-3075-4721-b2c8-98f59690ae31",
  "name": "admin",
  "email": "admin@paradrop.io",
  "password": "$2a$12$0.5BYEgPH9GTIWiLZlpoXug9RwsPbstM2GTeGGBH3yIAHu8hY5dha",
  "role": "admin",
  "expire_at" : "2024-03-25T15:17:49",
  "created_at" : "2024-03-26T15:17:49",
  "updated_at" : "2024-03-26T15:17:49",
  "last_signin" : "2024-03-26T15:17:49",
  "locked": false,
  "reset_password": false
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_doc/38db035f-c40a-49c4-8319-fb373c86bf23' -d \
'{
  "id" : "38db035f-c40a-49c4-8319-fb373c86bf23",
  "email" : "user@paradrop.io",
  "name" : "user",
  "password" : "$2b$12$tgxzVHFP7dFJRbqlWncyaenNXwy/.9ofJUTzD5o7v99bMhi6lTtJK",
  "role" : "read-only",
  "expire_at" : "2024-03-25T15:17:49",
  "created_at" : "2024-03-26T15:17:49",
  "updated_at" : "2024-03-26T15:17:49",
  "last_signin" : "2024-03-26T15:17:49",
  "locked" : false,
  "reset_password" : false
}'

# Seed App Configurations Data to paradrop_configs Index
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_configs/_doc/1' -d \
'{
  "id": "1",
  "slack_url": "",
  "ms_teams_url": "",
  "mattermost_url": "",
  "email_server": "",
  "email_password": "",
  "alert_email": "",
  "slack_enable": false,
  "ms_teams_enable": false,
  "mattermost_enable": false,
  "email_enable": false,
  "clean_hosts_days_interval": 0,
  "clean_events_count": 100000
}'

# Seed Reports Data to paradrop_reports Index
curl -k -u "$USER:$PASSWD" -XPUT 'https://127.0.0.1:9200/paradrop_reports'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_close'

curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_settings' -d @es_settings.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_open'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_mapping' -d @./mappings/paradrop_reports_mapping.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/14vBoULXeqiZcRRTq' -d \
'{
  "id": "14vBoULXeqiZcRRTq",
  "report_name": "fedramp_inventory",
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
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/YIvlbVBoqasTGlFQ' -d \
'{
  "report_name": "software_inventory",
  "report_description": "Show all software installed on assets",
  "report_mappings": {
    "Environment": "environment",
    "Gems": "gem",
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Packages": "packages",
    "Pip3": "pip3",
    "Windows Software": "windows_software"
  },
  "id": "YIvlbVBoqasTGlFQ",
  "created_at": "2024-04-12T15:28:36",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:28:36",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/ySvpy7c6SsJBbkq7' -d \
'{
  "report_name": "failed_or_critical_errors",
  "report_description": "Show failed software and critical errors",
  "report_mappings": {
    "Dmesg Errors": "dmesg_errors",
    "Docker Stopped": "docker_stopped",
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Journalctl Logs": "journalctl_logs",
    "Systemctl Failed": "systemctl_failed"
  },
  "id": "ySvpy7c6SsJBbkq7",
  "created_at": "2024-04-12T15:19:18",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:19:18",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/dIzIHRorTjMkUywM' -d \
'{
  "report_name": "virtualization",
  "report_description": "Show which systems are virtual machines and the environment theyre in",
  "report_mappings": {
    "Environment": "environment",
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Virtualization": "virtualization",
    "Virtualization System": "virtualization_system"
  },
  "id": "dIzIHRorTjMkUywM",
  "created_at": "2024-04-12T15:20:46",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:20:46",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/pM7DQWpI8uXQcUz6' -d \
'{
  "id": "pM7DQWpI8uXQcUz6",
  "report_name": "network_processes",
  "report_description": "Show open network ports and local processes mapping to ports",
  "report_mappings": {
    "Hostname": "hostname",
    "Ip Address": "ip_address",
    "Network Interfaces": "network_interfaces",
    "Open Ports": "open_ports",
    "Processes": "processes"
  },
  "created_at": "2024-04-12T15:17:06",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:17:38",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/72ryFQZoH6PJl9x1' -d \
'{
  "report_name": "daily_vulnerability",
  "report_description": "Get the latest Trivy vulnerabilities data",
  "report_mappings": {
    "Asset Type": "asset_type",
    "CPU Vulnerabilities": "cpu_vulnerabilities",
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Vulnerabilities ": "trivy"
  },
  "id": "72ryFQZoH6PJl9x1",
  "created_at": "2024-04-12T15:10:38",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:10:38",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/oWBMYKKZxNs7YGiN' -d \
'{
  "report_name": "scheduled_jobs",
  "report_description": "Show scheduled jobs like cronjobs, systemd-timers, Windows scheduled tasks",
  "report_mappings": {
    "Crontabs": "crontabs",
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Systemd Timers": "systemd_timers"
  },
  "id": "oWBMYKKZxNs7YGiN",
  "created_at": "2024-04-12T15:24:38",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:24:38",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/QFw7PTalmGIhB3Am' -d \
'{
  "report_name": "cloud_inventory",
  "report_description": "Show all assets that are hosted in a cloud provider",
  "report_mappings": {
    "Cloud": "cloud",
    "Environment": "environment",
    "Hostname": "hostname",
    "IP Address": "ip_address"
  },
  "id": "QFw7PTalmGIhB3Am",
  "created_at": "2024-04-12T15:27:01",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:27:01",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/5hPJgHaZoQhEnm2k' -d \
'{
  "report_name": "openscap_compliance",
  "report_description": "Show OpenScap compliance scan results",
  "report_mappings": {
    "Environment": "environment",
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Openscap": "openscap"
  },
  "id": "5hPJgHaZoQhEnm2k",
  "created_at": "2024-04-12T15:22:06",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:22:06",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/jITJT43igqVq3wKo' -d \
'{
  "report_name": "loggedin_users",
  "report_description": "Show users logged into the assets across the network",
  "report_mappings": {
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Users Loggedin": "users_loggedin"
  },
  "id": "jITJT43igqVq3wKo",
  "created_at": "2024-04-12T15:30:23",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:30:23",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/6runHG5hOFdn1us0' -d \
'{
  "id": "6runHG5hOFdn1us0",
  "report_name": "system_performance",
  "report_description": "Show system performance across all assets ",
  "report_mappings": {
    "Disk Used Pct": "diskused_pct",
    "Environment": "environment",
    "Hostname": "hostname",
    "IP Address": "ip_address",
    "Load 1 Min": "load1",
    "Load 15 Min": "load15",
    "Load 5 Min": "load5",
    "Memory Used Pct": "memoryused_pct"
  },
  "created_at": "2024-04-12T15:32:47",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:34:00",
  "updated_by": "admin@paradrop.io"
}'

# Seed Mock Data to paradrop_event_triggers Index
curl -k -u "$USER:$PASSWD" -XPUT 'https://127.0.0.1:9200/paradrop_event_triggers'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_close'

curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_settings' -d @es_settings.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_open'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_mapping' -d @./mappings/paradrop_event_triggers_mapping.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/38db035f-c40a-49c4-8319-fb373c86bf23' -d \
'{
  "id": "38db035f-c40a-49c4-8319-fb373c86bf23",
  "event_name": "low_disk_space",
  "send_alert": true,
  "event_impact": "high",
  "event_enable": true,
  "event_trigger": {
    "field": "diskused_pct",
    "operator": ">",
    "expected_value": "90"},
  "created_at": "2024-04-11T21:57:23Z",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-11T21:57:23Z",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/38db035f-c40a-49c4-8319-fb373c86bf24' -d \
'{
  "id": "38db035f-c40a-49c4-8319-fb373c86bf24",
  "event_name": "low_memory",
  "send_alert": true,
  "event_impact": "high",
  "event_enable": true,
  "event_trigger": {
    "field": "memoryused_pct",
    "operator": ">",
    "expected_value": "90"},
  "created_at": "2024-04-11T21:57:23Z",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-11T21:57:23Z",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/pjH2trDESeHlTVAE' -d \
'{
  "event_name": "critical_vulnerabilities",
  "send_alert": true,
  "event_impact": "high",
  "event_enable": true,
  "event_trigger": {
    "field": "trivy['"'"'vulnerabilities_critical'"'"']",
    "operator": ">",
    "expected_value": "0"
  },
  "id": "pjH2trDESeHlTVAE",
  "created_at": "2024-04-12T15:03:06",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:03:06",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/io0cr5NH9rufVynW' -d \
'{
  "event_name": "high_vulnerabilities",
  "send_alert": true,
  "event_impact": "medium",
  "event_enable": true,
  "event_trigger": {
    "field": "trivy['"'"'vulnerabilities_high'"'"']",
    "operator": ">",
    "expected_value": "0"
  },
  "id": "io0cr5NH9rufVynW",
  "created_at": "2024-04-12T15:03:45",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:03:45",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/joQ8SSlm2M2MhjpM' -d \
'{
  "event_name": "compliance_failures",
  "send_alert": true,
  "event_impact": "medium",
  "event_enable": true,
  "event_trigger": {
    "field": "openscap['"'"'fail_total'"'"']",
    "operator": ">",
    "expected_value": "5"
  },
  "id": "joQ8SSlm2M2MhjpM",
  "created_at": "2024-04-12T15:02:33",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:02:33",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/8ikdznQ86P1roTvW' -d \
'{
  "event_name": "ntp_not_running",
  "send_alert": true,
  "event_impact": "medium",
  "event_enable": true,
  "event_trigger": {
    "field": "ntp_running-bool",
    "operator": "==",
    "expected_value": "false"
  },
  "id": "8ikdznQ86P1roTvW",
  "created_at": "2024-04-12T15:01:45",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:01:45",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/OvO28UftXxVucASG' -d \
'{
  "event_name": "cpu_vulnerabilities",
  "send_alert": true,
  "event_impact": "high",
  "event_enable": true,
  "event_trigger": {
    "field": "cpu_vulnerabilities",
    "operator": ">",
    "expected_value": "0"
  },
  "id": "OvO28UftXxVucASG",
  "created_at": "2024-04-12T14:59:03",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T14:59:03",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/ybz05mqrEJ6Wzcmc' -d \
'{
  "event_name": "stopped_containers",
  "send_alert": true,
  "event_impact": "medium",
  "event_enable": true,
  "event_trigger": {
    "field": "docker_stopped",
    "operator": ">",
    "expected_value": "0"
  },
  "id": "ybz05mqrEJ6Wzcmc",
  "created_at": "2024-04-12T14:59:50",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T14:59:50",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/bORu8uvnd0x5sO44' -d \
'{
  "event_name": "expired_certs",
  "send_alert": true,
  "event_impact": "high",
  "event_enable": true,
  "event_trigger": {
    "field": "expired_certs",
    "operator": ">",
    "expected_value": "0"
  },
  "id": "bORu8uvnd0x5sO44",
  "created_at": "2024-04-12T15:00:10",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:00:10",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/GJLfIrcfOxcfPpTo' -d \
'{
  "event_name": "failed_logins",
  "send_alert": true,
  "event_impact": "high",
  "event_enable": true,
  "event_trigger": {
    "field": "failed_logins",
    "operator": ">",
    "expected_value": "10"
  },
  "id": "GJLfIrcfOxcfPpTo",
  "created_at": "2024-04-12T15:00:34",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:00:34",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/c04wi2cKUu0GVGDl' -d \
'{
  "event_name": "high_cpu",
  "send_alert": true,
  "event_impact": "medium",
  "event_enable": true,
  "event_trigger": {
    "field": "cpu_pct",
    "operator": ">",
    "expected_value": "95"
  },
  "id": "c04wi2cKUu0GVGDl",
  "created_at": "2024-04-12T14:58:38",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T14:58:38",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/BpbBmtUKD6HvL51r' -d \
'{
  "event_name": "high_load",
  "send_alert": true,
  "event_impact": "medium",
  "event_enable": true,
  "event_trigger": {
    "field": "load15",
    "operator": ">",
    "expected_value": "5"
  },
  "id": "BpbBmtUKD6HvL51r",
  "created_at": "2024-04-12T15:01:06",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:01:06",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/p8fYdOM3bbNlPoAJ' -d \
'{
  "event_name": "systemctl_failures",
  "send_alert": true,
  "event_impact": "medium",
  "event_enable": true,
  "event_trigger": {
    "field": "systemctl_failed",
    "operator": ">",
    "expected_value": "0"
  },
  "id": "p8fYdOM3bbNlPoAJ",
  "created_at": "2024-04-12T15:04:18",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:04:18",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/60xhW8vd43t7iZb9' -d \
'{
  "event_name": "low_memory_info",
  "send_alert": true,
  "event_impact": "info",
  "event_enable": true,
  "event_trigger": {
    "field": "memoryused_pct",
    "operator": ">",
    "expected_value": "80"
  },
  "id": "60xhW8vd43t7iZb9",
  "created_at": "2024-04-12T15:05:41",
  "created_by": "admin@paradrop.io",
  "updated_at": "2024-04-12T15:05:41",
  "updated_by": "admin@paradrop.io"
}'

# Seed Event Data to paradrop_events Index
curl -k -u "$USER:$PASSWD" -XPUT 'https://127.0.0.1:9200/paradrop_events'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_close'

curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_settings' -d @es_settings.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_open'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_mapping' -d @./mappings/paradrop_events_mapping.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_doc/38db035f-c40a-49c4-8319-fb373c86bf23' -d \
'{
  "id": "38db035f-c40a-49c4-8319-fb373c86bf23",
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
  "alert_sent": true,
  "alerts_sent_to": ["slack"]
}'

# Seed data to paradrop_tokens Index
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_tokens/_doc/1' -d \
'{
    "agent_token": "b97a81c5-3c2b-4a96-8881-38af26dc8407",
    "user_tokens": {
        "admin@paradrop.io": {
        "token": "b35bf90e-dd28-4208-8cc5-62ca12c3f5bb",
        "role": "admin"
        }
    }
}'

# Add paradrop_audit Index
curl -k -u "$USER:$PASSWD" -XPUT 'https://127.0.0.1:9200/paradrop_audit'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_close'

curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_settings' -d @es_settings.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_open'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_mapping' -d @./mappings/paradrop_audit_mapping.json

# Add paradrop_changes Index
curl -k -u "$USER:$PASSWD" -XPUT 'https://127.0.0.1:9200/paradrop_changes'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_close'

curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_settings' -d @es_settings.json

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_open'

curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_mapping' -d @./mappings/paradrop_changes_mapping.json

# Seed Mock Data to paradrop_changes Index
curl -k -u "$USER:$PASSWD" -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_doc/41zt852v-g74x-65j2-1235-xy856s78ew65' -d @changes_data.json

# Increase Default Search Results Returned For paradrop_hosts Index
curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_settings' -d '{"index.max_result_window": 100000}'

# Increase Default Search Results Returned for paradrop_users Index
curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_settings' -d '{"index.max_result_window": 100000}'

# Increase Default Search Results Returned for paradrop_event_triggers Index
curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_settings' -d '{"index.max_result_window": 100000}'

# Increase Default Search Results Returned for paradrop_events Index
curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_settings' -d '{"index.max_result_window": 100000}'

# Setup Single Node Cluster Index Replica Count
curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop*/_settings' -d'{"index":{"number_of_replicas":0}}'
curl -k -u "$USER:$PASSWD" -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/security*/_settings' -d'{"index":{"number_of_replicas":0}}'
