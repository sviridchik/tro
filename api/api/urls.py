"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_swagger.views import get_swagger_view
# from django.conf.urls import url

schema_view = get_swagger_view(title='Pastebin API')

# urlpatterns = [
#     url(r'^$', schema_view)
# ]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('managment/', include('managment.urls')),
    path('medicine/', include('medicine.urls')),
    path('statistic/', include('statistic.urls')),
    path('api/v1/auth/',include('djoser.urls')),
    path('api/v1/auth-token/',include('djoser.urls.authtoken')),
    path('main/', include('medicine.urls')),
    re_path(r'^$', schema_view),
]
