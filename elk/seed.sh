#!/bin/sh
# shellcheck disable=SC2016

# Seed Mock Data to paradrop_hosts Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT 'https://127.0.0.1:9200/paradrop_hosts'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_close'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_settings' -d @es_settings.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_open'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_mapping' -d @paradrop_hosts_mapping.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/' -d @server1.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/' -d @server2.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/' -d @server3.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_doc/' -d @server4.json

# Seed Mock Data to paradrop_users Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT 'https://127.0.0.1:9200/paradrop_users'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_close'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_settings' -d @es_settings.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_open'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_mapping' -d @paradrop_users_mapping.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_doc/2db4ff61-3075-4721-b2c8-98f59690ae31' -d \
'{
  "id": "2db4ff61-3075-4721-b2c8-98f59690ae31",
  "name": "admin",
  "email": "admin@paradrop.io",
  "password": "$2a$12$0.5BYEgPH9GTIWiLZlpoXug9RwsPbstM2GTeGGBH3yIAHu8hY5dha",
  "role": "admin",
  "expire_at" : "2022-06-25T15:17:49",
  "created_at" : "2022-04-26T15:17:49",
  "updated_at" : "2022-04-26T15:17:49",
  "last_signin" : "2022-04-26T15:17:49",
  "locked": false,
  "reset_password": false
}'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_doc/38db035f-c40a-49c4-8319-fb373c86bf23' -d \
'{
  "id" : "38db035f-c40a-49c4-8319-fb373c86bf23",
  "email" : "user@paradrop.io",
  "name" : "user",
  "password" : "$2b$12$tgxzVHFP7dFJRbqlWncyaenNXwy/.9ofJUTzD5o7v99bMhi6lTtJK",
  "role" : "read-only",
  "expire_at" : "2022-06-25T15:17:49",
  "created_at" : "2022-04-26T15:17:49",
  "updated_at" : "2022-04-26T15:17:49",
  "last_signin" : "2022-04-26T15:17:49",
  "locked" : false,
  "reset_password" : false
}'

# Seed App Configurations Data to paradrop_configs Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_configs/_doc/1' -d \
'{
  "id": "1",
  "slack_url": "https://hooks.slack.com/services/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",
  "ms_teams_url": "",
  "mattermost_url": "",
  "email_server": "paradroptestingemail@gmail.com",
  "email_password": "ojiuwcejglsaqgry",
  "alert_email": "",
  "slack_enable": false,
  "ms_teams_enable": false,
  "mattermost_enable": false,
  "email_enable": false,
  "clean_hosts_days_interval": 0,
  "clean_events_count": 100000
}'

# Seed Reports Data to paradrop_reports Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT 'https://127.0.0.1:9200/paradrop_reports'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_close'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_settings' -d @es_settings.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_open'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_mapping' -d @paradrop_reports_mapping.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_reports/_doc/14vBoULXeqiZcRRTq' -d \
'{
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
}'

# Seed Mock Data to paradrop_event_triggers Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT 'https://127.0.0.1:9200/paradrop_event_triggers'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_close'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_settings' -d @es_settings.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_open'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_mapping' -d @paradrop_event_triggers_mapping.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/38db035f-c40a-49c4-8319-fb373c86bf23' -d \
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
  "created_at": "2022-04-25T16:59:07",
  "created_by": "admin@paradrop.io",
  "updated_at": "2022-04-25T16:59:07",
  "updated_by": "admin@paradrop.io"
}'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_doc/38db035f-c40a-49c4-8319-fb373c86bf24' -d \
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
  "created_at": "2022-04-25T16:59:07",
  "created_by": "admin@paradrop.io",
  "updated_at": "2022-04-25T16:59:07",
  "updated_by": "admin@paradrop.io"
}'

# Seed Event Data to paradrop_events Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT 'https://127.0.0.1:9200/paradrop_events'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_close'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_settings' -d @es_settings.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_open'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_mapping' -d @paradrop_events_mapping.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_doc/38db035f-c40a-49c4-8319-fb373c86bf23' -d \
'{
  "id": "38db035f-c40a-49c4-8319-fb373c86bf23",
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
  "alert_sent": true,
  "alerts_sent_to": ["slack"]
}'

# Seed data to paradrop_tokens Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_tokens/_doc/1' -d \
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
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT 'https://127.0.0.1:9200/paradrop_audit'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_close'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_settings' -d @es_settings.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_open'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_audit/_mapping' -d @paradrop_audit_mapping.json

# Add paradrop_changes Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT 'https://127.0.0.1:9200/paradrop_changes'

# To add settings, we have to close the index, update settings and then open index again.
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_close'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_settings' -d @es_settings.json

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_open'

curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_mapping' -d @paradrop_changes_mapping.json

# Seed Mock Data to paradrop_changes Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPOST -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_changes/_doc/41zt852v-g74x-65j2-1235-xy856s78ew65' -d @changes_data.json

# Increase Default Search Results Returned For paradrop_hosts Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_hosts/_settings' -d '{"index.max_result_window": 100000}'

# Increase Default Search Results Returned for paradrop_users Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_users/_settings' -d '{"index.max_result_window": 100000}'

# Increase Default Search Results Returned for paradrop_event_triggers Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_event_triggers/_settings' -d '{"index.max_result_window": 100000}'

# Increase Default Search Results Returned for paradrop_events Index
curl -k -u 'admin:dtYe2cKY2YtyBEJ49a' -XPUT -H 'Content-Type: application/json' 'https://127.0.0.1:9200/paradrop_events/_settings' -d '{"index.max_result_window": 100000}'
