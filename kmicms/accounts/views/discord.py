from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from authlib.integrations.django_client import OAuth
from crispy_forms import helper, layout
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm, Form
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, View

from accounts.models import DiscordAccount, DiscordConnection

oauth = OAuth()
oauth.register(
    "discord",
    client_id=settings.DISCORD_APP_CLIENT_ID,
    client_secret=settings.DISCORD_APP_CLIENT_SECRET,
    access_token_url=settings.DISCORD_ACCESS_TOKEN_URL,
    authorize_url=settings.DISCORD_AUTHORIZE_URL,
    revocation_url=settings.DISCORD_REVOCATION_URL,
    userinfo_endpoint=settings.DISCORD_USERINFO_ENDPOINT,
    client_kwargs=settings.DISCORD_CLIENT_KWARGS,
)


class DiscordOAuthProfileAuthorizeView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        if DiscordConnection.objects.filter(user=request.user).exists():
            messages.warning(request, "Your account is already connected to Discord.")
            return redirect("accounts:profile")

        redirect_uri = request.build_absolute_uri(reverse("accounts:discord_oauth_redirect"))
        return oauth.discord.authorize_redirect(request, redirect_uri)


class DiscordOAuthProfileRedirectView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        if DiscordConnection.objects.filter(user=request.user).exists():
            messages.warning(request, "Your account is already connected to Discord.")
            return redirect("accounts:profile")

        token = oauth.discord.authorize_access_token(request)
        userinfo = oauth.discord.userinfo(token=token)

        account, created = DiscordAccount.objects.get_or_create(
            discord_id=int(userinfo["id"]),
            defaults={
                "username": userinfo["username"],
            },
        )

        # If the discord account was already known, update the username
        if not created:
            account.username = userinfo["username"]
            account.save()

        if DiscordConnection.objects.filter(discord_account=account).exists():
            messages.error(
                request, "That Discord account is connected to another user. Please disconnect it and try again."
            )
            return redirect("accounts:profile")

        expires_at = datetime.fromtimestamp(token["expires_at"], ZoneInfo("UTC"))
        DiscordConnection.objects.create(
            user=request.user,
            discord_account=account,
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            access_token_expires_at=expires_at,
        )

        messages.success(request, f"Successfully connected to Discord account: {account}")
        return redirect("accounts:profile")


class DiscordAccountProfileDisconnectView(LoginRequiredMixin, DeleteView):
    template_name = "accounts/discord_account_disconnect.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self) -> DiscordConnection:
        return get_object_or_404(DiscordConnection, user=self.request.user)

    def get_form(self, form_class: type[BaseModelForm] | None = None) -> BaseModelForm:
        form = super().get_form(form_class)
        form.helper = helper.FormHelper()
        form.helper.add_input(layout.Submit("submit", "Disconnect", css_class="btn-danger"))
        return form

    def form_valid(self, form: Form) -> HttpResponseRedirect:
        resp = super().form_valid(form)

        # Revoke the refresh token
        oauth.discord._get_oauth_client().revoke_token(
            settings.DISCORD_REVOCATION_URL,
            token=self.object.refresh_token,
            token_type_hint="refresh_token",  # noqa: S106
        )

        messages.success(self.request, "Successfully disconnected from Discord")
        return resp
