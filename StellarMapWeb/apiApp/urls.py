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
    re_path('set_network/<str:network>/', views.set_network, name='set_network'),
]
