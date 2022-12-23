from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers.conn import SiteChecker
from .helpers.env import EnvHelpers


@api_view(['GET'])
def check_url(request, url):
    """
    Check the reachability of the given URL.

    Parameters:
        url (str): The URL to check.

    Returns:
        Response: A JSON response containing the reachability status of the URL.
    """
    checker = SiteChecker()
    result = checker.check_url(url)
    return Response({"reachable": result})

@api_view(['GET'])
def check_all_urls(request):
    """
    Check the reachability of all URLs in the sites_dict.

    Returns:
        Response: A JSON response containing the reachability status of each URL.
    """
    sites_dict = {
        "stellar_github": "https://github.com/stellar",
        "stellar_org": "https://www.stellar.org",
        "stellar_doc": "https://stellar-documentation.netlify.app/api/",
    }

    results = {}
    checker = SiteChecker()
    for site, url in sites_dict.items():
        results[site] = checker.check_url(url)

    return Response(results)


@api_view(['GET'])
def set_network(request):
    """Set the environment variables for the specified Stellar network.
    
    This API view function accepts a GET request with a `network` parameter in the query string,
    which specifies the Stellar network for which to set the environment variables. The function
    supports two values for the `network` parameter: 'testnet' and 'public'. If the `network`
    parameter is not one of these values, the function returns an error response. Otherwise, it
    sets the environment variables for the specified network and returns a success response.
    """
    env_helpers = EnvHelpers()
    network = request.GET.get('network')
    if network == 'testnet':
        env_helpers.set_testnet_network()
    elif network == 'public':
        env_helpers.set_public_network()
    else:
        return Response({"error": "Invalid network value"}, status=400)
    return Response({"success": "Network set successfully"})