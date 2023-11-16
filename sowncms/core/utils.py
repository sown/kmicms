from datetime import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator
from zoneinfo import ZoneInfo


def current_year() -> int:
    tz = ZoneInfo(settings.TIME_ZONE)
    return datetime.now(tz=tz).year

def last_year() -> int:
    return current_year() - 1

def max_value_current_year(value: int) -> MaxValueValidator:
    return MaxValueValidator(current_year())(value)
