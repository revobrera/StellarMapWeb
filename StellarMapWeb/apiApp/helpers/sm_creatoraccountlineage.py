import json

import pandas as pd
import sentry_sdk
from apiApp.helpers.sm_horizon import StellarMapHorizonAPIParserHelpers
from apiApp.helpers.sm_stellarexpert import (
    StellarMapStellarExpertAPIHelpers, StellarMapStellarExpertAPIParserHelpers)
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

    def async_horizon_accounts_assets_doc_api_href_from_accounts_raw_data(self, client_session, lin_queryset, *args, **kwargs):

        try:

            # Create an instance of the manager
            lineage_manager = StellarCreatorAccountLineageManager()

            # update status to IN_PROGRESS
            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_UPDATING_HORIZON_ACCOUNTS_ASSETS_DOC_API_HREF')

            # Create an instance of Astra Document
            astra_document = AstraDocument()
            astra_document.set_datastax_url(datastax_url=lin_queryset.horizon_accounts_doc_api_href)
            response_dict = astra_document.get_document()

            # Create an instance of StellarMapHorizonAPIParserHelpers
            api_parser = StellarMapHorizonAPIParserHelpers()
            api_parser.set_datastax_response(datastax_response=response_dict)
            account_assets_dict = api_parser.parse_account_assets()

            # Converting dictionary to JSON string
            json_string = json.dumps(account_assets_dict)

            # update lineage record
            request = HttpRequest()
            request.data = {
                'horizon_accounts_assets_doc_api_href': json_string,
                'status': 'DONE_UPDATING_HORIZON_ACCOUNTS_ASSETS_DOC_API_HREF'
            }

            lineage_manager.update_lineage(id=lin_queryset.id, request=request)
        except Exception as e:
            sentry_sdk.capture_exception(e)

    def async_horizon_accounts_flags_doc_api_href_from_accounts_raw_data(self, client_session, lin_queryset, *args, **kwargs):

        try:

            # Create an instance of the manager
            lineage_manager = StellarCreatorAccountLineageManager()

            # update status to IN_PROGRESS
            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_UPDATING_HORIZON_ACCOUNTS_FLAGS_DOC_API_HREF')

            # Create an instance of Astra Document
            astra_document = AstraDocument()
            astra_document.set_datastax_url(datastax_url=lin_queryset.horizon_accounts_doc_api_href)
            response_dict = astra_document.get_document()

            # Create an instance of StellarMapHorizonAPIParserHelpers
            api_parser = StellarMapHorizonAPIParserHelpers()
            api_parser.set_datastax_response(datastax_response=response_dict)
            account_flags_dict = api_parser.parse_account_flags()

            # Converting dictionary to JSON string
            json_string = json.dumps(account_flags_dict)

            # update lineage record
            request = HttpRequest()
            request.data = {
                'horizon_accounts_flags_doc_api_href': json_string,
                'status': 'DONE_UPDATING_HORIZON_ACCOUNTS_FLAGS_DOC_API_HREF'
            }

            lineage_manager.update_lineage(id=lin_queryset.id, request=request)
        except Exception as e:
            sentry_sdk.capture_exception(e)

    def async_stellar_expert_explorer_directory_doc_api_href_from_accounts_raw_data(self, client_session, lin_queryset, *args, **kwargs):

        try:

            # Create an instance of the manager
            lineage_manager = StellarCreatorAccountLineageManager()

            # update status to IN_PROGRESS
            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_UPDATING_HORIZON_ACCOUNTS_SE_DIRECTORY')

            # Request SE to GET directory for account
            comprehensive_se_responses = {}
            se_helpers = StellarMapStellarExpertAPIHelpers(lin_queryset=lin_queryset)

            # Collecting stellar_account code, issuer and type
            se_parser = StellarMapStellarExpertAPIParserHelpers(lin_queryset=lin_queryset)
            asset_dict = se_parser.parse_asset_code_issuer_type()

            # Collect all SE api responses
            comprehensive_se_responses['se_asset_list'] = se_helpers.get_se_asset_list()
            comprehensive_se_responses['se_asset_rating'] = se_helpers.get_se_asset_rating(asset_code=asset_dict['asset_code'], asset_type=asset_dict['asset_type'])
            comprehensive_se_responses['se_blocked_domain'] = se_helpers.get_se_blocked_domain(asset_domain=lin_queryset.home_domain)
            comprehensive_se_responses['se_account_directory'] = se_helpers.get_se_account_directory()

            # Converting dictionary to JSON string
            json_string = json.dumps(comprehensive_se_responses)

            # update lineage record
            request = HttpRequest()
            request.data = {
                'stellar_expert_explorer_directory_doc_api_href': json_string,
                'status': 'DONE_UPDATING_HORIZON_ACCOUNTS_SE_DIRECTORY'
            }

            lineage_manager.update_lineage(id=lin_queryset.id, request=request)
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
            row_dict = {}

            while (has_creator_account == True):
                # query account queryset
                lin_manager = StellarCreatorAccountLineageManager()
                lin_queryset = lin_manager.get_queryset(
                    stellar_account=creator_account_in_loop,
                    network_name=network_in_loop
                )

                # if query returns a record
                if (lin_queryset is not None):

                    # set creator_account and network variable from query
                    creator_account_in_loop = lin_queryset.stellar_creator_account
                    network_in_loop = lin_queryset.network_name

                    # queryset to dict
                    '''
                    {
                        'id': UUID('51db8d0b-76a6-4961-9b3d-243f4f5479bb'), 
                        'account_active': None, 
                        'stellar_creator_account': 'GCGNWKCJ3KHRLPM3TM6N7D3W5YKDJFL6A2YCXFXNMRTZ4Q66MEMZ6FI2', 
                        'stellar_account': 'GCF7F72LNF3ODSJIIWPJWEVWX33VT2SVZSUQ5NMDKDLK3N2NFCUAUHPT',
                        'stellar_account_created_at': datetime.datetime(2019, 4, 16, 19, 51, 54),
                        'network_name': 'public',
                        'home_domain': 'no_element_home_domain',
                        'xlm_balance': 0.0,
                        'horizon_accounts_doc_api_href': '...horizon_accounts/a7a3affd-95d6-4de9-88d4-254acc9e3d8f',
                        'horizon_accounts_operations_doc_api_href': '...horizon_operations/1419f099-ef61-4112-861b-1f94552fab53',
                        'horizon_accounts_effects_doc_api_href': '...horizon_effects/3b993958-8d3b-4d59-9146-e41cda66054f',
                        'stellar_expert_explorer_account_doc_api_href': None,
                        'status': 'DONE_MAKE_GRANDPARENT_LINEAGE',
                        'created_at': datetime.datetime(2023, 3, 14, 0, 31, 36),
                        'updated_at': datetime.datetime(2023, 3, 14, 0, 36, 37),
                        'stellar_expert_explorer_directory_doc_api_href': None
                    }
                    '''
                    row_dict = {field_name: getattr(lin_queryset, field_name) for field_name in lin_queryset._values.keys()}
                
                    # append row to list
                    queryset_list.append(row_dict)
                
                else:
                    # exits loop
                    has_creator_account = False

            if queryset_list:
                # list is not empty
                # convert list of dictionaries to pandas dataframe with index
                df = pd.DataFrame(queryset_list)
                return df
            
            else:
                return pd.DataFrame()

        except Exception as e:
            sentry_sdk.capture_exception(e)


    def generate_tidy_radial_tree_genealogy(self, genealogy_df):
        # takes in dataframe from get_account_genealogy()
        
        if not genealogy_df.empty:
            for index, row in genealogy_df.iterrows():
                # query account queryset
                lin_manager = StellarCreatorAccountLineageManager()
                lin_queryset = lin_manager.get_queryset(
                    stellar_account=row['stellar_account'],
                    network_name=row['network_name']
                )

                # Create an instance of Astra Document
                astra_document = AstraDocument()
                astra_document.set_datastax_url(datastax_url=lin_queryset.horizon_accounts_doc_api_href)
                response_json = astra_document.get_document()

                # Create an instance of StellarMapHorizonAPIParserHelpers
                api_parser = StellarMapHorizonAPIParserHelpers()
                api_parser.set_datastax_response(datastax_response=response_json)
                creator_dict = api_parser.parse_operations_creator_account(stellar_account=lin_queryset.stellar_account)
                
                tidy_radial_tree_genealogy_dict = api_parser.parse_operations_creator_account(stellar_account=lin_queryset.stellar_account)
