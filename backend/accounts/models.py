import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    sku = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(nbytes=12)
        return super().save(*args, **kwargs)
