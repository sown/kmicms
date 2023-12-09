from django.http import HttpRequest
from django.urls import reverse
from wagtail import hooks


@hooks.register("register_account_menu_item")
def register_account_profile(request: HttpRequest) -> dict[str, str]:
    return {"url": reverse("accounts:profile"), "label": "View profile", "help_text": "View your SUWS / SOWN profile."}
