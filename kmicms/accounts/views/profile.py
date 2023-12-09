from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_profile.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(
            sso_user_settings_url=settings.SSO_USER_SETTINGS_URL,
            **kwargs,
        )
