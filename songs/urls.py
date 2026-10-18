from django.urls import path
from . import views

app_name = "songs"

urlpatterns = [
    path("", views.songs, name="list"),
    path("<int:song_id>/", views.song_detail, name="detail"),
]