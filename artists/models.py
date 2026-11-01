from django.db import models
from labels.models import Label


class Artist(models.Model):
    name = models.CharField("Имя артиста", max_length=255)
    country = models.CharField("Страна", max_length=100, blank=True)
    label = models.ForeignKey(
        Label,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artists",
        verbose_name="Лейбл"
    )

    class Meta:
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"

    def __str__(self):
        return self.name
