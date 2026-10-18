from django.urls import path
from . import views

app_name = "labels"

urlpatterns = [
    path("", views.labels, name="list"),
    path("<int:label_id>/", views.label_detail, name="detail"),
]