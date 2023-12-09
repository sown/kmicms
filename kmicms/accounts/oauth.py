from authlib.integrations.django_client import OAuth
from django.conf import settings

oauth_config = OAuth()

# Discord Integration
oauth_config.register(
    "discord",
    client_id=settings.DISCORD_APP_CLIENT_ID,
    client_secret=settings.DISCORD_APP_CLIENT_SECRET,
    access_token_url=settings.DISCORD_ACCESS_TOKEN_URL,
    authorize_url=settings.DISCORD_AUTHORIZE_URL,
    revocation_url=settings.DISCORD_REVOCATION_URL,
    userinfo_endpoint=settings.DISCORD_USERINFO_ENDPOINT,
    client_kwargs=settings.DISCORD_CLIENT_KWARGS,
)
