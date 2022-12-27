from django.urls import re_path
from apiApp import views
from django.views.generic import TemplateView


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
    re_path('docs/', TemplateView.as_view(
        template_name='documentation.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    re_path('lineage/network/<str:network>/stellar_address/<str:stellar_account_address>/', views.lineage_stellar_account, name='lineage_stellar_account'),
]
