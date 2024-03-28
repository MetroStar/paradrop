#!/usr/bin/env python3

# Global Constants
ES_HOSTS_INDEX: str = "paradrop_hosts"
ES_USERS_INDEX: str = "paradrop_users"
ES_EVENT_TRIGGERS_INDEX: str = "paradrop_event_triggers"
ES_EVENTS_INDEX: str = "paradrop_events"
ES_REPORTS_INDEX: str = "paradrop_reports"
ES_CONFIG_INDEX: str = "paradrop_configs"
ES_TOKENS_INDEX: str = "paradrop_tokens"
ES_AUDIT_INDEX: str = "paradrop_audit"
ES_CHANGES_INDEX: str = "paradrop_changes"

HEADERS: dict = {"Content-Type": "application/json"}

ES_URL: str = "https://127.0.0.1:9200/"
ES_USER: str = "admin"
ES_PW: str = "dtYe2cKY2YtyBEJ49a"
ES_TLS_VERIFY: bool = False
FLASK_HOST: str = "0.0.0.0:5000"
FLASK_DEBUG: bool = False
PARADROP_ADMIN_USER: str = "admin@paradrop.io"
PARADROP_ADMIN_PW: str = "Paradrop789!"
PARADROP_ADMIN_TOKEN: str = None
PARADROP_SECRET_KEY: str = "randomsecretkey"

# Elasticsearch variables
ES_HOSTS_URL: str = ES_URL + ES_HOSTS_INDEX
ES_USERS_URL: str = ES_URL + ES_USERS_INDEX
ES_EVENTS_URL: str = ES_URL + ES_EVENTS_INDEX
ES_EVENT_TRIGGERS_URL: str = ES_URL + ES_EVENT_TRIGGERS_INDEX
ES_REPORTS_URL: str = ES_URL + ES_REPORTS_INDEX
ES_CONFIGS_URL: str = ES_URL + ES_CONFIG_INDEX
ES_TOKENS_URL: str = ES_URL + ES_TOKENS_INDEX
ES_AUDIT_URL: str = ES_URL + ES_AUDIT_INDEX
ES_CHANGES_URL: str = ES_URL + ES_CHANGES_INDEX
