#!/usr/bin/env python3
import config.config as configs
from asyncio import run
from hypercorn.config import Config
from hypercorn.asyncio import serve
from flask_setup import asgi_app as app
from api_setup import add_resources
from os.path import exists
from config.initialization import validate_configs
from db.db_requests import put_request, post_request, get_request
from utils.timestamps import gen_timestamp
from db.users.create_users import hash_pwd


# Configure hypercorn ASGI server
config = Config()
config.bind = [configs.FLASK_HOST]

if exists('./localhost.pem') and exists('./localhost.key'):
    config.certfile = './localhost.pem'
    config.keyfile = './localhost.key'


def first_run() -> bool:
    # Defining elasticsearch settings and index mappings
    es_index_settings: dict = {
        "analysis": {
            "normalizer": {
                "lowercase_normalizer": {
                    "type": "custom",
                    "filter": ["lowercase"]
                }
            }
        }
    }
    paradrop_audit_mapping: dict = {
        "properties": {
            "event": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "updated_by": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "updated_at": {
                "type": "keyword"
            }
        }
    }
    paradrop_changes_mapping: dict = {
        "properties": {
            "changes_summary": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "changes_discovered": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            }
        }
    }
    paradrop_event_triggers_mapping: dict = {
        "properties": {
            "event_name": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "event_impact": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "event_enable": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "send_alert": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "event_trigger": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer"
                    }
                }
            }
        }
    }
    paradrop_events_mapping: dict = {

        "properties": {
            "hostname": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "ip_address": {
                "type": "ip",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "timestamp": {
                "type": "keyword"
            },
            "event_impact": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "event_name": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "event_message": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            }
        }
    }
    paradrop_hosts_mapping: dict = {
        "properties": {
            "os": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "hostname": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "ip_address": {
                "type": "ip",
                "fields": {
                    "raw": {
                        "type": "keyword"
                    }
                }
            },
            "platform": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "asset_type": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "cloud": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "tags": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "last_run": {
                "type": "keyword"
            },
            "docker_stopped": {
                "type": "keyword",
                "fields": {
                    "raw": {
                        "type": "long"
                    }
                }
            },
            "docker_paused": {
                "type": "keyword",
                "fields": {
                    "raw": {
                        "type": "long"
                    }
                }
            },
            "docker_running": {
                "type": "keyword",
                "fields": {
                    "raw": {
                        "type": "long"
                    }
                }
            },
            "docker_images_count": {
                "type": "long"
            },
            "docker_images": {
                "type": "nested",
                "include_in_parent": True,
                "properties": {
                    "name": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer"
                    },
                    "size": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer"
                    },
                    "created": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer"
                    }
                }
            },
            "docker_containers": {
                "type": "nested",
                "include_in_parent": True,
                "properties": {
                    "name": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer",
                        "fields": {
                            "raw": {
                                "type": "keyword"
                            }
                        }
                    },
                    "image": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer",
                        "fields": {
                            "raw": {
                                "type": "keyword"
                            }
                        }
                    },
                    "state": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer",
                        "fields": {
                            "raw": {
                                "type": "keyword"
                            }
                        }
                    },
                    "status": {
                        "type": "keyword",
                        "normalizer": "lowercase_normalizer",
                        "fields": {
                            "raw": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "openscap": {
                "type": "object",
                "properties": {
                    "checks": {
                        "type": "keyword",
                        "fields": {
                            "raw": {
                                "type": "long"
                            }
                        }
                    },
                    "pass_total": {
                        "type": "keyword",
                        "fields": {
                            "raw": {
                                "type": "long"
                            }
                        }
                    },
                    "fixed_total": {
                        "type": "keyword",
                        "fields": {
                            "raw": {
                                "type": "long"
                            }
                        }
                    },
                    "fail_total": {
                        "type": "keyword",
                        "fields": {
                            "raw": {
                                "type": "long"
                            }
                        }
                    }

                }
            },
            "trivy": {
                "type": "object",
                "properties": {
                    "vulnerabilities_total": {
                        "type": "keyword",
                        "fields": {
                            "raw": {
                                "type": "long"
                            }
                        }
                    },
                    "vulnerabilities_low": {
                        "type": "long"
                    },
                    "vulnerabilities_medium": {
                        "type": "long"
                    },
                    "vulnerabilities_high": {
                        "type": "long"
                    },
                    "vulnerabilities_critical": {
                        "type": "long"
                    },
                    "vulnerabilities_unknown": {
                        "type": "long"
                    },
                    "trivy_results": {
                        "type": "nested",
                        "properties": {
                            "Target": {
                                "type": "keyword",
                                "normalizer": "lowercase_normalizer"
                            },
                            "Class": {
                                "type": "keyword",
                                "normalizer": "lowercase_normalizer"
                            },
                            "Type": {
                                "type": "keyword",
                                "normalizer": "lowercase_normalizer"
                            },
                            "Vulnerabilities": {
                                "type": "nested",
                                "properties": {
                                    "VulnerabilityID": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "PkgName": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "InstalledVersion": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "FixedVersion": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "Layer": {
                                        "type": "object"
                                    },
                                    "SeveritySource": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "PrimaryURL": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "DataSource": {
                                        "type": "object",
                                        "properties": {
                                            "ID": {
                                                "type": "keyword",
                                                "normalizer": "lowercase_normalizer"
                                            },
                                            "Name": {
                                                "type": "keyword",
                                                "normalizer": "lowercase_normalizer"
                                            },
                                            "URL": {
                                                "type": "keyword",
                                                "normalizer": "lowercase_normalizer"
                                            }
                                        }
                                    },
                                    "Title": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "Description": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "Severity": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "CVSS": {
                                        "type": "object",
                                        "properties": {
                                            "nvd": {
                                                "type": "object",
                                                "properties": {
                                                    "V2Vector": {
                                                        "type": "keyword",
                                                        "normalizer": "lowercase_normalizer"
                                                    },
                                                    "V3Vector": {
                                                        "type": "keyword",
                                                        "normalizer": "lowercase_normalizer"
                                                    },
                                                    "V2Score": {
                                                        "type": "float"
                                                    },
                                                    "V3Score": {
                                                        "type": "float"
                                                    }
                                                }
                                            },
                                            "redhat": {
                                                "type": "object",
                                                "properties": {
                                                    "V3Vector": {
                                                        "type": "keyword",
                                                        "normalizer": "lowercase_normalizer"
                                                    },
                                                    "V3Score": {
                                                        "type": "float"
                                                    },
                                                    "V2Vector": {
                                                        "type": "keyword",
                                                        "normalizer": "lowercase_normalizer"
                                                    },
                                                    "V2Score": {
                                                        "type": "float"
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "References": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    },
                                    "PublishedDate": {
                                        "type": "date"
                                    },
                                    "LastModifiedDate": {
                                        "type": "date"
                                    },
                                    "CweIDs": {
                                        "type": "keyword",
                                        "normalizer": "lowercase_normalizer"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    paradrop_reports_mapping: dict = {
        "properties": {
            "report_name": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "report_description": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            }
        }
    }
    paradrop_users_mapping: dict = {
        "properties": {
            "email": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "name": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "role": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "last_signin": {
                "type": "keyword",
                "normalizer": "lowercase_normalizer"
            },
            "created_at": {
                "type": "keyword"
            },
            "expire_at": {
                "type": "keyword"
            }
        }
    }

    # Check if Users index exists and if there are any data
    find_users: dict = get_request(configs.ES_USERS_URL + "/_search")
    if find_users.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_USERS_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_USERS_URL + "/_close/", "")
        put_request(configs.ES_USERS_URL + "/_settings/", es_index_settings)
        post_request(configs.ES_USERS_URL + "/_open/", "")

        # Updating index mapping
        post_request(
            configs.ES_USERS_URL +
            "/_mapping/",
            paradrop_users_mapping)

        # ADDING DEFAULT USER DATA
        # ADDING ADMIN ACCOUNT
        new_admin_user: dict = {}
        new_admin_user["id"] = "2db4ff61-3075-4721-b2c8-98f59690ae31"
        new_admin_user["name"] = "admin"
        new_admin_user["email"] = configs.PARADROP_ADMIN_USER
        new_admin_user["password"] = run(hash_pwd(configs.PARADROP_ADMIN_PW))
        new_admin_user["role"] = "admin"
        new_admin_user["expire_at"] = gen_timestamp(expiration_days=60)
        new_admin_user["created_at"] = gen_timestamp()
        new_admin_user["updated_at"] = gen_timestamp()
        new_admin_user["last_signin"] = gen_timestamp()
        new_admin_user["locked"] = False
        new_admin_user["reset_password"] = False
        # Sending request to ES to add default admin user
        post_request(
            configs.ES_USERS_URL +
            "/_doc/" +
            new_admin_user["id"],
            new_admin_user)

    # Check if Configs index exists and if there are any data
    find_configs: dict = get_request(configs.ES_CONFIGS_URL + "/_search")
    if find_configs.status_code == 404:
        # ADDING DEFAULT CONFIG DATA
        new_configs: dict = {}
        new_configs["id"] = "1"
        new_configs["slack_url"] = ""
        new_configs["ms_teams_url"] = ""
        new_configs["mattermost_url"] = ""
        new_configs["email_server"] = ""
        new_configs["email_password"] = ""
        new_configs["alert_email"] = ""
        new_configs["slack_enable"] = False
        new_configs["ms_teams_enable"] = False
        new_configs["mattermost_enable"] = False
        new_configs["email_enable"] = False
        new_configs["clean_hosts_days_interval"] = 0
        new_configs["clean_events_count"] = 100000
        # Sending request to ES to add default config data
        post_request(configs.ES_CONFIGS_URL + "/_doc/1", new_configs)

    # Check if Reports index exists and if there are any data
    find_reports: dict = get_request(configs.ES_REPORTS_URL + "/_search")
    if find_reports.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_REPORTS_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_REPORTS_URL + "/_close/", "")
        put_request(configs.ES_REPORTS_URL + "/_settings/", es_index_settings)
        post_request(configs.ES_REPORTS_URL + "/_open/", "")

        # Updating index mapping
        post_request(
            configs.ES_REPORTS_URL +
            "/_mapping/",
            paradrop_reports_mapping)

    # Check if Event Triggers index exists and if there are any data
    find_event_triggers: dict = get_request(
        configs.ES_EVENT_TRIGGERS_URL + "/_search")
    if find_event_triggers.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_EVENT_TRIGGERS_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_EVENT_TRIGGERS_URL + "/_close/", "")
        put_request(
            configs.ES_EVENT_TRIGGERS_URL +
            "/_settings/",
            es_index_settings)
        post_request(configs.ES_EVENT_TRIGGERS_URL + "/_open/", "")

        # Updating index mapping
        post_request(
            configs.ES_EVENT_TRIGGERS_URL +
            "/_mapping/",
            paradrop_event_triggers_mapping)

    # Check if Tokens index exists and if there are any data
    find_tokens: dict = get_request(configs.ES_TOKENS_URL + "/_search")
    if find_tokens.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_TOKENS_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_TOKENS_URL + "/_close/", "")
        put_request(configs.ES_TOKENS_URL + "/_settings/", es_index_settings)
        post_request(configs.ES_TOKENS_URL + "/_open/", "")

        # ADDING DEFAULT TOKENS
        new_tokens: dict = {}
        new_tokens["agent_token"] = configs.PARADROP_ADMIN_TOKEN
        new_tokens["user_tokens"] = {}

        # Sending request to ES to add default tokens
        post_request(
            configs.ES_TOKENS_URL +
            "/_doc/1",
            new_tokens)

    # Check if Audit index exists and if there are any data
    find_audit: dict = get_request(configs.ES_AUDIT_URL + "/_search")

    # If index doesn't exist yet, create it
    if find_audit.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_AUDIT_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_AUDIT_URL + "/_close/", "")
        put_request(configs.ES_AUDIT_URL + "/_settings/", es_index_settings)
        put_request(configs.ES_AUDIT_URL + "/_settings/",
                    {"index.max_result_window": 100000})
        post_request(configs.ES_AUDIT_URL + "/_open/", "")

        # Updating index mapping
        post_request(
            configs.ES_AUDIT_URL +
            "/_mapping/",
            paradrop_audit_mapping)

    # Check if Changes index exists and if there are any data
    find_changes: dict = get_request(configs.ES_CHANGES_URL + "/_search")

    # If index doesn't exist yet, create it
    if find_changes.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_CHANGES_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_CHANGES_URL + "/_close/", "")
        put_request(configs.ES_CHANGES_URL + "/_settings/", es_index_settings)
        post_request(configs.ES_CHANGES_URL + "/_open/", "")

        # Updating index mapping
        post_request(
            configs.ES_CHANGES_URL +
            "/_mapping/",
            paradrop_changes_mapping)

    # Check if Events index exists and if there are any data
    find_events: dict = get_request(configs.ES_EVENTS_URL + "/_search")

    # If index doesn't exist yet, create it and update it's settings
    if find_events.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_EVENTS_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_EVENTS_URL + "/_close/", "")
        put_request(configs.ES_EVENTS_URL + "/_settings/", es_index_settings)
        put_request(configs.ES_EVENTS_URL + "/_settings/",
                    {"index.max_result_window": 100000})
        post_request(configs.ES_EVENTS_URL + "/_open/", "")

        # Updating index mapping
        post_request(
            configs.ES_EVENTS_URL +
            "/_mapping/",
            paradrop_events_mapping)

    # Check if Hosts index exists and if there are any data
    find_hosts: dict = get_request(configs.ES_HOSTS_URL + "/_search")

    # If index doesn't exist yet, create it and update it's settings
    if find_hosts.status_code == 404:
        # Initizalizing index
        post_request(configs.ES_HOSTS_URL + "/_doc/", "")

        # Updating index settings
        post_request(configs.ES_HOSTS_URL + "/_close/", "")
        put_request(configs.ES_HOSTS_URL + "/_settings/", es_index_settings)
        put_request(configs.ES_HOSTS_URL + "/_settings/",
                    {"index.max_result_window": 100000})
        post_request(configs.ES_HOSTS_URL + "/_open/", "")

        # Updating index mapping
        post_request(
            configs.ES_HOSTS_URL +
            "/_mapping/",
            paradrop_hosts_mapping)
    return True


# Running function to add endpoints
run(add_resources())

# RUN FLASK APP FROM HERE
if __name__ == "__main__" and validate_configs():
    first_run()
    run(serve(app, config))
