from django.urls import path
from . import views

urlpatterns = [
    path("", views.labels, name="labels"),
    path("<int:label_id>/", views.label_detail, name="label_detail"),
]
