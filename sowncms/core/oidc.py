from django.contrib.auth.models import Group, Permission, User
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class SOWNOIDCAuthenticationBackend(OIDCAuthenticationBackend):

    def get_username(self, claims: dict[str, bool | str | list[str]]) -> str:
        return claims.get('sub')  # corresponds to username

    def create_user(self, claims: dict[str, bool | str | list[str]]) -> User :
        user = super().create_user(claims)
        return self.update_user(user, claims)

    def update_user(self, user: User, claims: dict[str, bool | str | list[str]]) -> User:
        full_name = claims.get('given_name', '')

        name_parts = full_name.split(' ')

        if len(name_parts) == 0:
            return user
        elif len(name_parts) == 1:
            user.first_name = name_parts[0]
            user.last_name = ''
        else:
            user.first_name = name_parts.pop(0)
            user.last_name = ' '.join(name_parts)

        user.email = claims.get('email')

        user.save()

        if 'Wagtail Staff' in claims.get('groups', []):
            user.groups.add(self._get_staff_group())
        else:
            user.groups.clear()

        return user

    def _get_staff_group(self) -> Group:
        staff_group, _ = Group.objects.get_or_create(name='Wagtail Staff')
        permission = Permission.objects.get(name='Can access Wagtail admin')
        staff_group.permissions.add(permission)
        return staff_group
