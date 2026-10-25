from django.urls import path
from . import views

app_name = "songs"

urlpatterns = [
    path("", views.songs, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:song_id>/", views.song_detail, name="detail"),
]
