from django.urls import re_path
from apiApp import views
from django.views.generic import TemplateView


app_name = 'apiApp'
urlpatterns = [
    re_path('api/v1/docs/', views.documentation_view, name='swagger-ui'),
    re_path(
        'api/v1/check_url/<str:url>/',
        views.check_url,
        name='check_url'
    ),
    re_path(
        'api/v1/check_all_urls/',
        views.check_all_urls,
        name='check_all_urls'
    ),
    re_path('api/v1/set_network/<str:network>/', views.set_network, name='set_network'),
    re_path('api/v1/lineage/network/<str:network>/stellar_address/<str:stellar_account_address>/', views.lineage_stellar_account, name='lineage_stellar_account'),
]
