from django.urls import re_path
from apiApp import views
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='StellarMap API')

app_name = 'apiApp'
urlpatterns = [
    re_path('api/v1/docs/', schema_view, name='swagger-ui'),
    re_path('api/v1/check_all_urls/', views.check_all_urls, name='check_all_urls'),
    re_path(r'^api/v1/set_network/(?P<network>[-\w]+)/$', views.set_network, name='set_network'),
    re_path(r'^lineage/network/(?P<network>[-\w]+)/stellar_address/(?P<stellar_account_address>[-\w]+)/$', views.lineage_stellar_account, name='lineage_stellar_account'),
]
