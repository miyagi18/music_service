from django.db import models
from artists.models import Artist


class Song(models.Model):
    title = models.CharField("Название песни", max_length=255)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="songs",
        verbose_name="Артист"
    )
    genre = models.CharField("Жанр", max_length=100, blank=True)
    release_year = models.IntegerField("Год выпуска", null=True, blank=True)
    duration_sec = models.IntegerField(
        "Длительность (сек)", null=True, blank=True)
    has_lyrics = models.BooleanField("Есть текст", default=False)

    class Meta:
        verbose_name = "Песня"
        verbose_name_plural = "Песни"

    def __str__(self):
        return self.title
