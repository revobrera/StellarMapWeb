import json
import logging
from datetime import datetime
import pytz

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import viewsets

from .helpers.async_stellar_account_inquiry_history import \
    AsyncStellarInquiryCreator
from .helpers.conn import SiteChecker
from .helpers.env import EnvHelpers
from .helpers.lineage_creator_accounts import LineageHelpers
from .models import StellarAccountInquiryHistory
from .serializers import (BaseModelSerializer,
                          StellarAccountInquiryHistorySerializer,
                          StellarAccountLineageSerializer)

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


class StellarAccountInquiryHistoryViewSet_OLDER(APIView):
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
        import pdb; pdb.set_trace()
        # create inquiry
        try:
            # inquire account
            queryset = StellarAccountInquiryHistory.objects.filter(
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
                inquiry_qs = StellarAccountInquiryHistory(
                    stellar_account=request.data['stellar_account'],
                    network_name=request.data['network_name'],
                    status=request.data['status']
                )

                inquiry_qs.save()
                context['message']='Stellar Account Address sucessfully stored in DB.'

            return Response(context)

        except Exception as e:
            logger.error("Error with executing POST request on StellarAccountInquiryHistoryViewSet_OLDER")
            logger.error(e)


class StellarAccountInquiryHistoryViewSet(ViewSet):
    def list(self, request):
        queryset = StellarAccountInquiryHistory.objects.all()
        serializer = StellarAccountInquiryHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class StellarAccountInquiryHistoryListCreateAPIView(ListCreateAPIView):
    queryset = StellarAccountInquiryHistory.objects.all()
    serializer_class = StellarAccountInquiryHistorySerializer
    permission_classes = ()


class StellarAccountInquiryHistoryListAPIView(ListAPIView):
    queryset = StellarAccountInquiryHistory.objects.all()
    serializer_class = StellarAccountInquiryHistorySerializer
    permission_classes = ()

class StellarAccountInquiryHistoryModelViewSet(viewsets.ModelViewSet):
    queryset = StellarAccountInquiryHistory.objects.all()
    serializer_class = StellarAccountInquiryHistorySerializer

    def create(self, request, *args, **kwargs):
        # config NY time
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)

        # create datetime string
        date_str = datetime_NY.strftime("%Y-%m-%d %H:%M:%S")

        # create datetime object and NOT string
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")


        queryset = self.get_queryset().filter(
            stellar_account=request.data['stellar_account'],
            network_name=request.data['network_name']
        ).first()

        if queryset:
            payload = {
                "status":"RE_INQUIRY",
                "updated_at":date_obj
            }
            self.get_queryset().filter(id=queryset.id).update(**payload)
            return Response({'message': 'Stellar Account Address found and updated status: RE_INQUIRY'})
        else:
            request.data.update({'created_at':date_obj})
            return super().create(request, *args, **kwargs)

