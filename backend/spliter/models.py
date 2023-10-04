from collections.abc import Iterable
import secrets

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Split(models.Model):
    debtor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("debtor"),
        related_name="splits_as_debtor",
        blank=False,
        null=True,
    )
    creditor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("creditor"),
        related_name="splits_as_creditor",
        blank=False,
        null=True,
    )
    is_closed = models.BooleanField(default="f")
    amount = models.PositiveBigIntegerField(
        verbose_name=_("amount"), blank=False, null=True
    )
    sku = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return (
            self.debtor.username
            + " --> "
            + self.creditor.username
            + " : "
            + str(self.amount)
        )

    def save(self, *args, **kwargs) -> None:
        if not self.sku:
            self.sku = secrets.token_urlsafe(nbytes=12)
        return super().save(*args, **kwargs)
