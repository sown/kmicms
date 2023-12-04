from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from accounts.models import User


class SOWNOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def get_username(self, claims: dict[str, bool | str | list[str]]) -> str:
        return claims.get("sub")  # corresponds to username

    def create_user(self, claims: dict[str, bool | str | list[str]]) -> User:
        user = super().create_user(claims)
        return self.update_user(user, claims)

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
