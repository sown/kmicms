from typing import Any

from django import http
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect


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
            return redirect("oidc_authentication_init")

        return super().dispatch(request, *args, **kwargs)
