from django.urls import re_path
from apiApp import views


app_name = 'apiApp'
urlpatterns = [
    re_path(
        'check_url/<str:url>/',
        views.check_url,
        name='check_url'
    ),
    re_path(
        'check_all_urls/',
        views.check_all_urls,
        name='check_all_urls'
    ),
]
