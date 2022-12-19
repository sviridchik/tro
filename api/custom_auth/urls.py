from django.urls import re_path
from rest_framework.routers import DefaultRouter

from custom_auth import views


urlpatterns = [
    re_path(r"^token/login/?$", views.TokenCreateView.as_view()),
    re_path(r"^users/?$", views.CreateUserView.as_view()),
]
