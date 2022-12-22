from django.urls import re_path
from apiApp import views

app_name = 'apiApp'
urlpatterns = [
    re_path(
        'check_url/<str:url>/',
        views.check_url,
        name='check_url',
        docstring="""Check the reachability of the given URL.
        
        Parameters:
            url (str): The URL to check.
        
        Returns:
            Response: A JSON response containing the reachability status of the URL.
        """
    ),
    re_path(
        'check_all_urls/',
        views.check_all_urls,
        name='check_all_urls',
        docstring="""Check the reachability of all URLs in the sites_dict.
        
        Returns:
            Response: A JSON response containing the reachability status of each URL.
        """
    ),
]
