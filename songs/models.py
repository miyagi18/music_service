from django.db import models
from django.db.models import Case, When, Value
from artists.models import Artist


class Song(models.Model):
    # ... ваши поля ...
    title = models.CharField("Название песни", max_length=255)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="songs")
    genre = models.CharField("Жанр", max_length=100, blank=True)
    release_year = models.IntegerField("Год выпуска", null=True, blank=True)
    duration_sec = models.IntegerField(
        "Длительность (сек)", null=True, blank=True)
    has_lyrics = models.BooleanField("Есть текст", default=False)

    # Вычисляемое поле: true, если песня длится 240 секунд и больше
    is_long = models.GeneratedField(
        expression=Case(
            When(duration_sec__gte=240, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField()
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Длинная песня"
    )

    def __str__(self):
        return self.title
