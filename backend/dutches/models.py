import secrets

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Dutch(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dutches", blank=False, null=True
    )
    stuff_name = models.CharField(
        verbose_name=_("stuff name"),
        max_length=255,
        blank=False,
        null=True,
    )
    price = models.PositiveBigIntegerField(
        verbose_name=_("price"), blank=False, null=True
    )
    sku = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.get_username() + "'s " + self.stuff_name

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = secrets.token_urlsafe(nbytes=12)
        return super().save(*args, **kwargs)
