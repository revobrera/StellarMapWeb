import json
import logging

from apiApp.helpers.sm_creatoraccountlineage import \
    StellarMapCreatorAccountLineageHelpers
from apiApp.helpers.sm_datetime import StellarMapDateTimeHelpers
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .helpers.env import EnvHelpers
from .helpers.lineage_creator_accounts import LineageHelpers
from .helpers.sm_conn import SiteChecker
from .managers import UserInquirySearchHistoryManager
from .models import UserInquirySearchHistory
from .serializers import (UserInquirySearchHistorySerializer)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


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
def set_network(request, network):
    """Set the environment variables for the specified Stellar network.
    
    This API view function accepts a GET request with a `network` parameter in the query string,
    which specifies the Stellar network for which to set the environment variables. The function
    supports two values for the `network` parameter: 'testnet' and 'public'. If the `network`
    parameter is not one of these values, the function returns an error response. Otherwise, it
    sets the environment variables for the specified network and returns a success response.
    """
    env_helpers = EnvHelpers()
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


class UserInquirySearchHistoryViewSet_OLDER(APIView):
    """
    A viewset for handling the creation of inquiries for Stellar accounts.
    """

    # DRF documentation states that without explicit declaration of authentication_classes, 
    # default SessionAuthentication is enforced thus requires CSRF token
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        """
        Handles the creation of a new inquiry for a Stellar account.
        
        Parameters:
            - request (HttpRequest): The request object containing the data for the new inquiry.
        
        Returns:
            - 201 (created): If the inquiry is created successfully.
            - 400 (bad request): If the request data is invalid.

        Notes:
            Regarding the use of async in views, Django views are synchronous by default.
            This means that views are executed one after the other, and the next view is
            executed only after the previous one has finished. Asynchronous views are not
            supported in Django because of the way the framework is designed.

            However, it's possible to use async in service layer or in the models. Async
            can be used to optimize the performance of the application by allowing the
            execution of multiple tasks at the same time, without waiting for one task
            to finish before starting another one. For example, if you are making
            multiple HTTP requests or performing a time-consuming computation, you can 
            use async to perform those tasks concurrently and avoid blocking the execution
            of other parts of the application.
        """

        # create inquiry
        try:
            # inquire account
            queryset = UserInquirySearchHistory.objects.filter(
                stellar_account=request.data['stellar_account'],
                network_name=request.data['network_name']
            ).first()

            context = {}
            context['stellar_account']=request.data['stellar_account']
            context['network_name']=request.data['network_name']

            if queryset.exists():
                payload = {
                    "status":"RE_INQUIRY"
                }

                queryset.update(**payload)
                context['message']='Stellar Account Address found and updated status: RE_INQUIRY'
            else:
                inquiry_qs = UserInquirySearchHistory(
                    stellar_account=request.data['stellar_account'],
                    network_name=request.data['network_name'],
                    status=request.data['status']
                )

                inquiry_qs.save()
                context['message']='Stellar Account Address sucessfully stored in DB.'

            return Response(context)

        except Exception as e:
            logger.error("Error with executing POST request on UserInquirySearchHistoryViewSet_OLDER")
            logger.error(e)


class UserInquirySearchHistoryViewSet(ViewSet):
    def list(self, request):
        queryset = UserInquirySearchHistory.objects.all()
        serializer = UserInquirySearchHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class UserInquirySearchHistoryListCreateAPIView(ListCreateAPIView):
    queryset = UserInquirySearchHistory.objects.all()
    serializer_class = UserInquirySearchHistorySerializer
    permission_classes = ()


class UserInquirySearchHistoryListAPIView(ListAPIView):
    queryset = UserInquirySearchHistory.objects.all()
    serializer_class = UserInquirySearchHistorySerializer
    permission_classes = ()

class UserInquirySearchHistoryModelViewSet(viewsets.ModelViewSet):
    queryset = UserInquirySearchHistory.objects.all()
    serializer_class = UserInquirySearchHistorySerializer

    def create(self, request, *args, **kwargs):
        # query stellar account in db
        inquiry_manager = UserInquirySearchHistoryManager()

        queryset = inquiry_manager.get_queryset(
            stellar_account=request.data['stellar_account'],
            network_name=request.data['network_name']
        )

        # if stellar account found, update status
        if queryset:
            inquiry_manager.update_inquiry(id=queryset.id, status='RE_INQUIRY')
            return Response({'message': 'Stellar Account Address found and updated status: RE_INQUIRY'})
        else:
            inquiry_manager.create_inquiry(request)
            return Response({'message': f'Stellar Account Address {request.data["stellar_account"]} saved successfully'})


class GetAccountGenealogy(APIView):

    def get(self, request, network, stellar_account_address):

        sm_lineage_helpers = StellarMapCreatorAccountLineageHelpers()
        genealogy_df = sm_lineage_helpers.get_account_genealogy(stellar_account=stellar_account_address, network_name=network)

        # format df as records
        genealogy_records = genealogy_df.to_dict(orient='records')

        sm_dt_helpers = StellarMapDateTimeHelpers()
        # use `format_timestamp` function to handle Cassandra Timestamp objects

        # iterate through the df records and match it with the account_genealogy_fields
        account_genealogy_items = []
        for idx, record in enumerate(genealogy_records):
            account_genealogy_item = {
                'index': idx,
                'stellar_creator_account': record['stellar_creator_account'],
                'stellar_account_created_at': sm_dt_helpers.format_timestamp(record['stellar_account_created_at']),
                'stellar_account': record['stellar_account'],
                'network_name': record['network_name'],
                'home_domain': record['home_domain'],
                'xlm_balance': record['xlm_balance'],
                'stellar_expert': 'https://stellar.expert/explorer/'+ record['network_name'] + '/account/' + record['stellar_account'],
                'status': record['status']
            }
            account_genealogy_items.append(account_genealogy_item)

        # frontend vue account_genealogy_items
        # Convert the dictionary to a JSON format
        account_genealogy_items_json = json.dumps(account_genealogy_items)

        return account_genealogy_items_json
