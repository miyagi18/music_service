from django.urls import path
from . import views

urlpatterns = [
    path("", views.songs, name="songs"),
    path("<int:song_id>/", views.song_detail, name="song_detail"),
]
