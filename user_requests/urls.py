from django.urls import path
from . import views

urlpatterns = [
    path("", views.requests_list, name="requests"),
    path("<int:request_id>/",
         views.request_detail,
         name="request_detail"),
]