#!/usr/bin/env python3
from datetime import datetime, timezone, timedelta


def gen_timestamp(expiration_days: int = 0) -> str:
    """
    Function to generate current date and time.
    """
    timestamp: str = datetime.now(
        timezone.utc) + timedelta(days=expiration_days)
    timestamp = timestamp.isoformat().split('.', 1)[0]
    return timestamp
