from django.urls import path

urlpatterns = [
    path(
        'v1/check_url/<str:url>/',
        check_url,
        name='check_url',
        docstring="""Check the reachability of the given URL.
        
        Parameters:
            url (str): The URL to check.
        
        Returns:
            Response: A JSON response containing the reachability status of the URL.
        """
    ),
    path(
        'v1/check_all_urls/',
        check_all_urls,
        name='check_all_urls',
        docstring="""Check the reachability of all URLs in the sites_dict.
        
        Returns:
            Response: A JSON response containing the reachability status of each URL.
        """
    ),
]
