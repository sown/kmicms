from datetime import datetime
from functools import lru_cache
from typing import NamedTuple
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.validators import MaxValueValidator


def current_year() -> int:
    tz = ZoneInfo(settings.TIME_ZONE)
    return datetime.now(tz=tz).year


def last_year() -> int:
    return current_year() - 1


def max_value_current_year(value: int) -> MaxValueValidator:
    return MaxValueValidator(current_year())(value)


class SocialMediaService(NamedTuple):
    slug: str
    name: str
    icon: str


@lru_cache
def get_social_media_services() -> dict[str, SocialMediaService]:
    services: list[SocialMediaService] = [
        SocialMediaService(slug="discord", name="Discord", icon="discord"),
        SocialMediaService(slug="facebook", name="Facebook", icon="facebook"),
        SocialMediaService(slug="github", name="GitHub", icon="github"),
        SocialMediaService(slug="mastodon", name="Mastodon", icon="mastodon"),
        SocialMediaService(slug="snapchat", name="Snapchat", icon="snapchat"),
        SocialMediaService(slug="twitter", name="Twitter / X", icon="twitter-x"),
        SocialMediaService(slug="whatsapp", name="WhatsApp", icon="whatsapp"),
        SocialMediaService(slug="youtube", name="YouTube", icon="youtube"),
    ]
    return {service.slug: service for service in services}


@lru_cache
def get_social_media_service_choices() -> list[tuple[str, str]]:
    services = get_social_media_services()
    return [(service.slug, service.name) for service in services.values()]
