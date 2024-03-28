#!/usr/bin/env python3
import config.config as config
from requests import get
from os import getenv
from urllib.parse import urlparse
from urllib3 import disable_warnings
from flask_setup import logger
from uuid import uuid4

disable_warnings()

# Validates URLs


def is_url(url: str) -> bool:

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])

    except ValueError:
        return False


# Is Elasticsearch reachable
def is_db_up() -> bool:

    resp = get(
        url=config.ES_URL,
        verify=config.ES_TLS_VERIFY,
        auth=(config.ES_USER, config.ES_PW))

    if resp.status_code != 200:
        return False

    return True

# Override Defaults if ENV is present


def override_default_configs():

    if getenv('ES_URL') is not None:
        config.ES_URL = getenv('ES_URL')

    if getenv('ES_USER') is not None:
        config.ES_USER = getenv('ES_USER')

    if getenv('ES_PW') is not None:
        config.ES_PW = getenv('ES_PW')

    if getenv('ES_TLS_VERIFY') is not None:
        config.ES_TLS_VERIFY = getenv('ES_TLS_VERIFY')

    if getenv('FLASK_HOST') is not None:
        config.FLASK_HOST = getenv('FLASK_HOST')

    if getenv('FLASK_DEBUG') is not None:
        config.FLASK_DEBUG = getenv('FLASK_DEBUG')

    if getenv('PARADROP_ADMIN_USER') is not None:
        config.PARADROP_ADMIN_USER = getenv('PARADROP_ADMIN_USER')

    if getenv('PARADROP_ADMIN_PW') is not None:
        config.PARADROP_ADMIN_PW = getenv('PARADROP_ADMIN_PW')

    if getenv('PARADROP_ADMIN_TOKEN') is not None:
        config.PARADROP_ADMIN_TOKEN = getenv('PARADROP_ADMIN_TOKEN')


# Validate config.py
def validate_configs() -> bool:

    override_default_configs()

    if config.ES_HOSTS_INDEX is None:
        logger.debug("ES_HOSTS_INDEX is not present in config.py")
        exit(1)

    if config.ES_USERS_INDEX is None:
        logger.debug("ES_USERS_INDEX is not present in config.py")
        exit(1)

    if config.ES_CONFIG_INDEX is None:
        logger.debug("ES_CONFIG_INDEX is not present in config.py")
        exit(1)

    if config.ES_EVENT_TRIGGERS_INDEX is None:
        logger.debug("ES_EVENT_TRIGGERS_INDEX is not present in config.py")
        exit(1)

    if config.ES_EVENTS_INDEX is None:
        logger.debug("ES_EVENTS_INDEX is not present in config.py")
        exit(1)

    if config.ES_REPORTS_INDEX is None:
        logger.debug("ES_REPORTS_INDEX is not present in config.py")
        exit(1)

    if is_url(config.ES_URL) is False:
        logger.debug("ES_URL is not present in config.py")
        exit(1)

    if config.ES_USER is None:
        logger.debug("ES_USER is not present in config.py")
        exit(1)

    if config.ES_PW is None:
        logger.debug("ES_PW is not present in config.py")
        exit(1)

    if config.FLASK_HOST is None:
        logger.debug("FLASK_HOST is not present in config.py")
        exit(1)

    if config.FLASK_DEBUG is None:
        logger.debug("FLASK_DEBUG is not present in config.py")
        exit(1)

    if config.PARADROP_ADMIN_USER is None:
        logger.debug("PARADROP_ADMIN_USER is not present in config.py")
        exit(1)

    if config.PARADROP_ADMIN_PW is None:
        logger.debug("PARADROP_ADMIN_PW is not present in config.py")
        exit(1)

    if config.PARADROP_ADMIN_TOKEN is None:
        config.PARADROP_ADMIN_TOKEN = uuid4()

    if config.ES_TLS_VERIFY is None:
        logger.debug("ES_TLS_VERIFY is not present in config.py")
        exit(1)

    if not is_db_up():
        logger.debug(
            "ES is not reachable, please check config.py and try again")
        exit(1)

    return True
