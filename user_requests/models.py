from django.db import models
from artists.models import Artist

# Создаем кастомный QuerySet и Manager


class RequestQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status__in=[Request.Status.NEW, Request.Status.IN_PROGRESS])

    def done(self):
        return self.filter(status=Request.Status.DONE)


class RequestManager(models.Manager.from_queryset(RequestQuerySet)):
    pass


class User(models.Model):
    # ... (оставляем как было)
    name = models.CharField("Имя пользователя", max_length=255)
    email = models.EmailField("Email")
    city = models.CharField("Город", max_length=100, blank=True)

    def __str__(self):
        return self.name


class Request(models.Model):
    # TextChoices для статусов
    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        IN_PROGRESS = 'in_progress', 'В работе'
        DONE = 'done', 'Обработана'
        CANCELLED = 'cancelled', 'Отменена'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="requests")
    query = models.CharField("Запрос", max_length=255)
    genre = models.CharField("Жанр", max_length=100, blank=True)
    city = models.CharField("Город", max_length=100, blank=True)

    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )
    created_at = models.DateField("Дата создания", null=True, blank=True)
    found_artist = models.ForeignKey(
        Artist, on_delete=models.SET_NULL, null=True, blank=True, related_name="matched_requests"
    )

    objects = RequestManager()  # Подключаем менеджер

    def __str__(self):
        return f"Заявка #{self.id}: {self.query}"
