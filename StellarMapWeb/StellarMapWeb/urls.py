"""StellarMapWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

django.conf.urls.url() was deprecated in Django 3.0, and is removed in Django 4.0+.
user re_path with regex
"""
from django.urls import include, re_path
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='StellarMap API')

urlpatterns = [
    re_path('chief/', admin.site.urls),
    re_path('api/v1/', include('apiApp.urls')),
    re_path('docs/', schema_view),
]
