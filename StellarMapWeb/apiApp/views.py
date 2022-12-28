import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers.conn import SiteChecker
from .helpers.env import EnvHelpers
from .helpers.lineage_creator_accounts import LineageHelpers


@api_view(['GET'])
def check_all_urls(request):
    """
    Check the reachability of all URLs in the sites_dict.

    Returns:
        HttpResponse: An HTTP response containing the reachability status of each URL in JSON format.
    """

    results = {}
    checker = SiteChecker()
    results_json = checker.check_all_urls()

    return HttpResponse(results_json, content_type='application/json')


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


@api_view(['GET'])
def lineage_stellar_account(request, network, stellar_account_address):
    """
    Retrieve the upstream lineage of a Stellar account.
    
    This function will recursively crawl the creator accounts of the given Stellar account
    to build a list of its upstream lineage. The resulting list will be returned as a JSON
    response.
    
    Parameters:
        - network (str): The network on which the Stellar account is located.
        - stellar_account_address (str): The address of the Stellar account.
    
    Returns:
        JSON response with the following fields:
        - network (str): The network on which the Stellar account is located.
        - stellar_account_address (str): The address of the Stellar account.
        - upstream_lineage (list): A list of the upstream accounts in the lineage of the
          given Stellar account, starting with the immediate creator and ending with the
          root account.
    """

    # Instantiate the LineageHelpers class with the network and stellar_account_address
    lineage_helpers = LineageHelpers(network, stellar_account_address)
    
    # Create a dictionary with the relevant information
    data_dict = lineage_helpers.main()

    # Convert the data dictionary to a JSON response
    data_json = json.dumps(data_dict)

    # Return the data as a JSON response
    return Response(data_json)
