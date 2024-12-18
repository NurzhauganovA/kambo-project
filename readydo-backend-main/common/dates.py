from datetime import datetime
import pytz
from django.utils.timezone import get_current_timezone


def server_tz() -> pytz.timezone:
    return get_current_timezone()


def server_now() -> datetime:
    return datetime.now(server_tz())
