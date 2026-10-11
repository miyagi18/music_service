"""Корневая конфигурация URL проекта Music Service."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("labels/", include("labels.urls")),
    path("artists/", include("artists.urls")),
    path("songs/", include("songs.urls")),
    path("requests/", include("user_requests.urls")),
]
