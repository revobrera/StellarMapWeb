import sentry_sdk
from apiApp.helpers.sm_horizon import StellarMapHorizonAPIParserHelpers
from apiApp.managers import StellarCreatorAccountLineageManager
from apiApp.services import AstraDocument
from django.http import HttpRequest


class StellarMapCreatorAccountLineageHelpers:

    def async_update_from_accounts_raw_data(self, client_session, lin_queryset, *args, **kwargs):

        try:

            # Create an instance of the manager
            lineage_manager = StellarCreatorAccountLineageManager()

            # update status to IN_PROGRESS
            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_UPDATING_FROM_RAW_DATA')

            # Create an instance of Astra Document
            astra_document = AstraDocument()
            astra_document.set_datastax_url(datastax_url=lin_queryset.horizon_accounts_doc_api_href)
            response_json = astra_document.get_document()

            # Create an instance of StellarMapHorizonAPIParserHelpers
            api_parser = StellarMapHorizonAPIParserHelpers()
            api_parser.set_datastax_response(datastax_response=response_json)
            native_balance = api_parser.parse_account_native_balance()
            home_domain = api_parser.parse_account_home_domain()

            # update lineage record
            request = HttpRequest()
            request.data = {
                'home_domain': home_domain,
                'xlm_balance': native_balance,
                'status': 'DONE_UPDATING_FROM_RAW_DATA'
            }

            lineage_manager.update_lineage(id=lin_queryset.id, request=request)
        except Exception as e:
            sentry_sdk.capture_exception(e)

    def async_update_from_operations_raw_data(self, client_session, lin_queryset, *args, **kwargs):

        try:

            # Create an instance of the manager
            lineage_manager = StellarCreatorAccountLineageManager()

            # update status to IN_PROGRESS
            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_UPDATING_FROM_OPERATIONS_RAW_DATA')

            # Create an instance of Astra Document
            astra_document = AstraDocument()
            astra_document.set_datastax_url(datastax_url=lin_queryset.horizon_accounts_operations_doc_api_href)
            response_json = astra_document.get_document()

            # Create an instance of StellarMapHorizonAPIParserHelpers
            api_parser = StellarMapHorizonAPIParserHelpers()
            api_parser.set_datastax_response(datastax_response=response_json)
            creator_dict = api_parser.parse_operations_creator_account(stellar_account=lin_queryset.stellar_account)

            # update lineage record
            request = HttpRequest()
            if creator_dict is not None and "funder" in creator_dict:
                request.data = {
                    'stellar_creator_account': creator_dict["funder"],
                    'stellar_account_created_at': creator_dict["created_at"],
                    'status': 'DONE_UPDATING_FROM_OPERATIONS_RAW_DATA'
                }
            else: 
                request.data = {
                    'stellar_creator_account': 'no_element_funder',
                    'status': 'DONE_COLLECTING_CREATOR_ACCOUNT'
                }

            lineage_manager.update_lineage(id=lin_queryset.id, request=request)
        except Exception as e:
            sentry_sdk.capture_exception(e)

    def async_make_grandparent_account(self, client_session, lin_queryset, *args, **kwargs):

        try:

            # Create an instance of the manager
            lineage_manager = StellarCreatorAccountLineageManager()

            # update status to IN_PROGRESS
            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_MAKE_GRANDPARENT_LINEAGE')

            # creator account queryset
            new_lin_manager = StellarCreatorAccountLineageManager()
            new_lin_queryset = new_lin_manager.get_queryset(
                stellar_account=lin_queryset.stellar_creator_account,
                network_name=lin_queryset.network_name
            )

            PENDING = 'PENDING_HORIZON_API_DATASETS'
            if new_lin_queryset:
                # update grandparent lineage record
                # TODO: update datetime only if 3 hours passed
                new_lin_manager.update_status(id=new_lin_queryset.id, status=PENDING)
            else:
                # create grandparent lineage record
                request = HttpRequest()
                request.data = {
                    'stellar_account': lin_queryset.stellar_creator_account,
                    'network_name': lin_queryset.network_name,
                    'status': PENDING
                }

                new_lin_manager.create_lineage(request)
            
            lineage_manager.update_status(id=lin_queryset.id, status='DONE_MAKE_GRANDPARENT_LINEAGE')
        except Exception as e:
            sentry_sdk.capture_exception(e)

    def get_account_genealogy(self, stellar_account, network_name):
        try:
            # loop until no records returned or stellar_creator_account is "no_element_funder"
            # init variables
            has_creator_account = True
            creator_account_in_loop = stellar_account
            network_in_loop = network_name
            
            # empty list
            queryset_list = []

            while (has_creator_account == True):
                # query account queryset
                lin_manager = StellarCreatorAccountLineageManager()
                lin_queryset = lin_manager.get_queryset(
                    stellar_account=creator_account_in_loop,
                    network_name=network_in_loop
                )

                # if query returns a record
                if (lin_queryset or lin_queryset.stellar_creator_account == 'no_element_funder'):

                    # set creator_account and network variable from query
                    creator_account_in_loop = lin_queryset.stellar_creator_account
                    network_in_loop = lin_queryset.network_name
                
                    # append row to list
                    queryset_list.append(lin_queryset)
                
                else:
                    # exits loop
                    has_creator_account = False
                    creator_account_in_loop = ''
                    network_in_loop = ''

            # if queryset_list is not empty:
                # convert queryset to list of dictionaries

                # convert list of dictionaries to pandas dataframe
                # return df
            
            # else
                # return empty dataframe
                    

        except Exception as e:
            sentry_sdk.capture_exception(e)
