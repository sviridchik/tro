from django.urls import re_path
from rest_framework.routers import DefaultRouter

from custom_auth import views

router = DefaultRouter()
router.register("users", views.UserViewSet)


urlpatterns = [
    re_path(r"^token/login/?$", views.TokenCreateView.as_view(), name="login"),
] + router.urls