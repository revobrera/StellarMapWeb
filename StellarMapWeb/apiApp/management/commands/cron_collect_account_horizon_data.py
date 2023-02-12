import json

import sentry_sdk
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from apiApp.helpers.sm_horizon import StellarMapHorizonAPIHelpers
from apiApp.managers import (StellarCreatorAccountLineageManager,
                             UserInquirySearchHistoryManager)
from apiApp.services import AstraDocument
from django.core.management.base import BaseCommand
from django.http import HttpRequest
from apiApp.helpers.env import EnvHelpers


class Command(BaseCommand):
    help = ('This management command is a scheduled task that creates the parent lineage '
        'information from the Horizon API and persistently stores it in the database.')

    def handle(self, *args, **options):
        cron_name = 'cron_collect_account_horizon_data'
        try:
            # create an instance of cron helpers to check for cron health
            cron_helpers = StellarMapCronHelpers(cron_name=cron_name)
            if cron_helpers.check_cron_health() is True:

                # Create an instance of the manager
                lineage_manager = StellarCreatorAccountLineageManager()

                # Query 1 record with one of the status'
                lin_queryset = lineage_manager.get_queryset(
                    status__in=[
                        'PENDING_HORIZON_API_DATASETS',
                        'DONE_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS',
                        'DONE_COLLECTING_HORIZON_API_DATASETS_OPERATIONS',
                        'DONE_COLLECTING_HORIZON_API_DATASETS_EFFECTS'
                        ]
                )

                # Query 1 record with status starting with IN_PROGRESS_COLLECTING if in progress
                lin_in_progress_qs = lineage_manager.get_queryset(
                    status__in=[
                        'IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS',
                        'IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_OPERATIONS',
                        'IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_EFFECTS'
                        ]
                )

                # Due to rate limiting from the API server, we will only work on 1 pull at a time
                # Continue Horizon collection if found a PENDING_ record and no other records IN_PROGRESS
                if lin_queryset and not lin_in_progress_qs:

                    try:
                        # StellarMapWeb will not be collecting API datasets from Stellar.Expert 
                        # due to incomplete data when compared with Horizon API
                        # No specific use case at the moment to retrieve data from Stellar.Expert. 
                        # If a use case arises, the request call can be added to the if condition below.
                        
                        sm_horizon_helpers = StellarMapHorizonAPIHelpers()
                        sm_horizon_helpers.set_cron_name(cron_name=cron_name)

                        # set environment
                        env_helpers = EnvHelpers()
                        if lin_queryset.network_name == 'public':
                            env_helpers.set_public_network()
                        else:
                            env_helpers.set_testnet_network()

                        if lin_queryset.status == 'PENDING_HORIZON_API_DATASETS':

                            # update status to IN_PROGRESS
                            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS')

                            # call horizon accounts
                            accounts_list = sm_horizon_helpers.get_base_accounts()

                            # converts dictionary to json
                            accounts_json = json.dumps(accounts_list)

                            # get env horizon url
                            base_horiz_acc = f"{env_helpers.get_base_horizon_account()}{lin_queryset.stellar_account}" 

                            # store and patch in cassandra document api
                            astra_doc = AstraDocument()
                            astra_doc.set_collections_name(collections_name='horizon_accounts')
                            document_href = astra_doc.patch_document(stellar_account=lin_queryset.stellar_account, network_name=lin_queryset.network_name, external_url=base_horiz_acc, raw_data=accounts_json)

                            # store document href on db
                            request = HttpRequest()
                            request.data = {
                                'horizon_accounts_doc_api_href': document_href,
                                'status': 'DONE_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS'
                            }

                            # update lineage
                            lineage_manager.update_lineage(id=lin_queryset.id, request=request)

                        elif lin_queryset.status == 'DONE_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS':

                            # update status to IN_PROGRESS
                            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_OPERATIONS')

                            # call horizon operations
                            operations_list = sm_horizon_helpers.get_account_operations()

                            # converts dictionary to json
                            operations_json = json.dumps(operations_list)

                            # get env horizon url
                            base_horiz_ops = f"{env_helpers.get_base_horizon_operations()}{lin_queryset.stellar_account}" 

                            # store and patch in cassandra document api
                            astra_doc = AstraDocument()
                            astra_doc.set_collections_name(collections_name='horizon_operations')
                            document_href = astra_doc.patch_document(stellar_account=lin_queryset.stellar_account, network_name=lin_queryset.network_name, external_url=base_horiz_ops, raw_data=operations_json)

                            # store document href on db
                            request = HttpRequest()
                            request.data = {
                                'horizon_accounts_operations_doc_api_href': document_href,
                                'status': 'DONE_COLLECTING_HORIZON_API_DATASETS_OPERATIONS'
                            }

                            # update lineage
                            lineage_manager.update_lineage(id=lin_queryset.id, request=request)

                        elif lin_queryset.status == 'DONE_COLLECTING_HORIZON_API_DATASETS_OPERATIONS':

                            # update status to IN_PROGRESS
                            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_EFFECTS')

                            # call horizon effects
                            effects_list = sm_horizon_helpers.get_account_effects()

                            # converts dictionary to json
                            effects_json = json.dumps(effects_list)

                            # get env horizon url
                            base_horiz_eff = f"{env_helpers.get_base_horizon_effects()}{lin_queryset.stellar_account}" 

                            # store and patch in cassandra document api
                            astra_doc = AstraDocument()
                            astra_doc.set_collections_name(collections_name='horizon_effects')
                            document_href = astra_doc.patch_document(stellar_account=lin_queryset.stellar_account, network_name=lin_queryset.network_name, external_url=base_horiz_eff, raw_data=effects_json)

                            # store document href on db
                            request = HttpRequest()
                            request.data = {
                                'horizon_accounts_effects_doc_api_href': document_href,
                                'status': 'DONE_HORIZON_API_DATASETS'
                            }

                            # update lineage
                            lineage_manager.update_lineage(id=lin_queryset.id, request=request)

                    except Exception as e:
                        sentry_sdk.capture_exception(e)
                        raise ValueError(f'Error: {e}. Attempting to retrieve Horizon datasets, store in document DB and save href in StellarCreatorAccountLineage')

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'{cron_name}: {e}')


        self.stdout.write(self.style.SUCCESS(f'Successfully ran {cron_name}'))
