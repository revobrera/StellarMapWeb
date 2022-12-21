from django.urls import path

urlpatterns = [
    path('check_url/<str:url>/', check_url, name='check_url'),
    path('check_all_urls/', check_all_urls, name='check_all_urls'),
]
