from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from labels.models import Label
from unidecode import unidecode


class Artist(models.Model):
    name = models.CharField("Имя артиста", max_length=255)
    country = models.CharField("Страна", max_length=100, blank=True)
    label = models.ForeignKey(
        Label, on_delete=models.SET_NULL, null=True, blank=True, related_name="artists")

    # Добавляем slug
    slug = models.SlugField(max_length=255, unique=True,
                            blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            # unidecode переводит кириллицу в латиницу (Эндшпиль -> Endshpil)
            transliterated_name = unidecode(self.name)
            # slugify убирает пробелы и спецсимволы
            self.slug = f"{slugify(transliterated_name)}-{self.id or ''}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("artists:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
