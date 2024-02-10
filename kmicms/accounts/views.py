from __future__ import annotations

from typing import Any

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from wagtail.models import Site

from .models import User
from .oauth import oauth_config


class LoginView(auth_views.LoginView):
    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        # Redirect a user that is already logged in.
        # Borrowed from django.contrib.auth.views.LoginView.dispatch
        if self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return http.HttpResponseRedirect(redirect_to)

        # If SSO is enabled, redirect immediately.
        if not settings.USE_CONVENTIONAL_AUTH:
            request.session["sso_next"] = self.get_redirect_url()

            redirect_uri = request.build_absolute_uri(reverse("accounts:sso_oidc_redirect"))
            return oauth_config.sown.authorize_redirect(request, redirect_uri)

        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self) -> str:
        site = Site.find_for_request(self.request)
        return site.root_page.get_url()


class SSOOIDCRedirectView(View):
    def get(self, request: http.HttpRequest) -> http.HttpResponseRedirect:
        token = oauth_config.sown.authorize_access_token(request)
        userinfo = token.get("userinfo", {})

        try:
            username = userinfo["sub"]
        except KeyError:
            messages.error(request, "Invalid response from SSO.")
            return redirect("accounts:login")

        user, _ = User.objects.get_or_create(username=username)

        self.update_user(user, userinfo)

        login(request, user)

        from_session = request.session.pop("sso_next", None)

        redirect_to = from_session or self.get_default_redirect_url()
        messages.info(request, f"Signed in via SOWN SSO. Welcome {user.get_short_name()}")
        return redirect(redirect_to)

    def get_default_redirect_url(self) -> str:
        site = Site.find_for_request(self.request)
        return site.root_page.get_url()

    def update_user(self, user: User, claims: dict[str, bool | str | list[str]]) -> User:
        full_name = claims.get("given_name", "")

        name_parts = full_name.split(" ")

        if len(name_parts) == 0:
            return user
        elif len(name_parts) == 1:
            user.first_name = name_parts[0]
            user.last_name = ""
        else:
            user.first_name = name_parts.pop(0)
            user.last_name = " ".join(name_parts)

        sso_groups = claims.get("groups", [])
        is_staff = settings.SSO_STAFF_GROUP_NAME in sso_groups
        is_superuser = settings.SSO_SUPERUSER_GROUP_NAME in sso_groups

        user.email = claims.get("email")
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save()

        if is_staff:
            user.groups.add(self._get_staff_group())
        else:
            user.groups.clear()

        return user

    def _get_staff_group(self) -> Group:
        staff_group, _ = Group.objects.get_or_create(name="Wagtail Staff")
        permission = Permission.objects.get(name="Can access Wagtail admin")
        staff_group.permissions.add(permission)
        return staff_group
