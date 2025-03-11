from datetime import datetime

import pytz
from config import DATE_FORMAT, USER_TZ, SERVER_TZ


def validate_time_format(time_str):
    """Checking the correctness of time format"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        return None


def format_datetime(date_str, timezone_str=USER_TZ):
    """Formates the date in the line, taking into account the watch zone of the server"""
    user_timezone = pytz.timezone(timezone_str)
    server_timezone = pytz.timezone(SERVER_TZ)
    server_datetime = datetime.fromisoformat(date_str)

    server_datetime = server_datetime.astimezone(server_timezone)
    user_datetime = server_datetime.astimezone(user_timezone)
    return user_datetime.strftime(DATE_FORMAT)
