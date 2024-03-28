#!/usr/bin/env python3
from flask_setup import logger
import json
# Slack Alert imports
from slack_sdk.webhook import WebhookClient
# Email Alert imports
from smtplib import SMTP_SSL
from ssl import create_default_context
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# MS Teams imports
from pymsteams import connectorcard


def send_email_alert(current_configurations: dict, alert_data: dict):
    """
    Function that takes current configurations and data that we want to
    include in alert as an argument and sends it to specified email address.
    """
    try:
        # Specifying required data
        subject: str = "Paradrop Alert"
        sender_email: str = current_configurations["email_server"]
        recipient_email: str = current_configurations["alert_email"]
        password: str = current_configurations["email_password"]

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Add alert data to email
        message.attach(MIMEText(json.dumps(alert_data, indent=1)))

        text: str = message.as_string()
        # Log in to server using secure context and send email
        context = create_default_context()
        with SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient_email, text)

        return {
            "valid": True,
            "code": 200,
            "message": "Alert sent successfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


def send_slack_alert(current_configurations: dict, alert_data: dict):
    """
    Function that takes current configurations and data that we want to
    include in alert as an argument and sends it to specified Slack url.
    """
    try:
        webhook_url = current_configurations["slack_url"]
        webhook = WebhookClient(webhook_url)
        res = webhook.send(text=json.dumps(alert_data, indent=1))
        assert res.status_code == 200
        assert res.body == "ok"
        return {
            "valid": True,
            "code": 200,
            "message": "Alert sent successfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


def send_ms_teams_alert(current_configurations: dict, alert_data: dict):
    """
    Function that takes current configurations and data that we want to
    include in alert as an argument and sends it to specified MS Teams server.
    """
    try:
        # TODO: MS Teams Alerts
        ms_teams_url: str = current_configurations["ms_teams_url"]
        # Validate user's URL
        myTeamsMessage = connectorcard(ms_teams_url)
        myTeamsMessage.text(alert_data)
        myTeamsMessage.send()
        return {
            "valid": True,
            "code": 200,
            "message": "Alert sent successfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}


def send_mattermost_alert(current_configurations: dict, alert_data: dict):
    """
    Function that takes current configurations and data that we want to
    include in alert as an argument and sends it to specified Mattermost server.
    """
    try:
        # TODO: Mattermost Alerts
        return {
            "valid": True,
            "code": 200,
            "message": "Alert sent successfully.."}

    except BaseException as e:
        logger.error(e)
        return {
            "valid": False,
            "code": 500,
            "message": f"Something went wrong: {e}.."}
