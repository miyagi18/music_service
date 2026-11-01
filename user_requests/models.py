from django.db import models
from artists.models import Artist


class User(models.Model):
    name = models.CharField("Имя пользователя", max_length=255)
    email = models.EmailField("Email")
    city = models.CharField("Город", max_length=100, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name


class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Обработана'),
        ('cancelled', 'Отменена'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests")
    query = models.CharField("Запрос", max_length=255)
    genre = models.CharField("Жанр", max_length=100, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)
    status = models.CharField("Статус", max_length=20,
                              choices=STATUS_CHOICES, default='new')
    created_at = models.DateField("Дата создания", null=True, blank=True)
    found_artist = models.ForeignKey(
        Artist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matched_requests"
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка #{self.id}: {self.query}"
