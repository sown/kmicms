from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class DiscordAccount(models.Model):
    discord_id = models.PositiveBigIntegerField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"@{self.username}"


class DiscordConnection(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="discord_connection", related_query_name="discord_connection"
    )
    discord_account = models.OneToOneField(
        DiscordAccount,
        on_delete=models.CASCADE,
        related_name="discord_connection",
        related_query_name="discord_connection",
    )
    access_token = models.CharField(max_length=30)
    refresh_token = models.CharField(max_length=30)
    access_token_expires_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"Discord Connection for {self.user} to {self.discord_account}"
