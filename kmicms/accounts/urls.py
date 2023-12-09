from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.auth.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", views.profile.UserProfileView.as_view(), name="profile"),
    path(
        "integrations/discord/setup/",
        views.discord.DiscordOAuthProfileAuthorizeView.as_view(),
        name="discord_oauth_setup",
    ),
    path(
        "integrations/discord/redirect/",
        views.discord.DiscordOAuthProfileRedirectView.as_view(),
        name="discord_oauth_redirect",
    ),
    path(
        "integrations/discord/disconnect/",
        views.discord.DiscordAccountProfileDisconnectView.as_view(),
        name="discord_oauth_disconnect",
    ),
    path(
        "oidc/redirect/",
        views.auth.SSOOIDCRedirectView.as_view(),
        name="sso_oidc_redirect",
    ),
]
