from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import (
    DiscordAccountProfileDisconnectView,
    DiscordOAuthProfileAuthorizeView,
    DiscordOAuthProfileRedirectView,
    UserProfileView,
)

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("oauth/discord/setup", DiscordOAuthProfileAuthorizeView.as_view(), name="discord_oauth_setup"),
    path("oauth/discord/redirect", DiscordOAuthProfileRedirectView.as_view(), name="discord_oauth_redirect"),
    path("oauth/discord/disconnect", DiscordAccountProfileDisconnectView.as_view(), name="discord_oauth_disconnect"),
]
