from django.urls import include, re_path
# from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from apiApp import views
from apiApp.views import (UserInquirySearchHistoryListAPIView,
                          UserInquirySearchHistoryListCreateAPIView,
                          UserInquirySearchHistoryModelViewSet,
                          GetAccountGenealogy,
                          UserInquirySearchHistoryViewSet,
                          UserInquirySearchHistoryViewSet_OLDER)

# router = routers.SimpleRouter()
# router.register(r"inquiries-modelviewset", UserInquirySearchHistoryModelViewSet)

app_name = 'apiApp'
urlpatterns = [
    # re_path('api/v1/docs/', schema_view, name='swagger-ui'),
    re_path('api/v1/check_all_urls/', views.check_all_urls, name='check_all_urls'),
    re_path(r'^api/v1/set_network/(?P<network>[-\w]+)/$', views.set_network, name='set_network'),
    re_path(r'^lineage/network/(?P<network>[-\w]+)/stellar_address/(?P<stellar_account_address>[-\w]+)/$', views.lineage_stellar_account, name='lineage_stellar_account'),
    re_path(r'^inquiries/$', UserInquirySearchHistoryViewSet_OLDER.as_view(), name='UserInquirySearchHistoryViewSet_OLDER'),
    re_path(r'^stellar-inquiries/$', UserInquirySearchHistoryModelViewSet.as_view({'post': 'create'}), name='stellar-inquiries'),
    re_path(r'^account-genealogy/network/(?P<network>[-\w]+)/stellar_address/(?P<stellar_account_address>[-\w]+)/$', GetAccountGenealogy.as_view(), name='account-genealogy'),
    re_path(
        r"^inquiries-viewset/$",
        UserInquirySearchHistoryViewSet.as_view({"get": "list"}),
        name="inquiries_viewset_api",
    ),
    re_path(
        r"^inquiries-listcreate/$",
        UserInquirySearchHistoryListCreateAPIView.as_view(),
        name="inquiries_listcreate_api",
    ),
    re_path(
        r"^inquiries-listview/$",
        UserInquirySearchHistoryListAPIView.as_view(),
        name="inquiries_listview_api",
    ),
]

# urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
