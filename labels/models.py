from django.db import models


class Label(models.Model):
    name = models.CharField("Название", max_length=255)
    founded_year = models.IntegerField("Год основания", null=True, blank=True)
    country = models.CharField("Страна", max_length=100, blank=True)

    class Meta:
        verbose_name = "Лейбл"
        verbose_name_plural = "Лейблы"

    def __str__(self):
        return self.name
