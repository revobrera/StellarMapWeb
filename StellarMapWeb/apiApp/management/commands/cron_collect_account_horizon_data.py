import json
import re
import uuid

import sentry_sdk
from apiApp.helpers.env import EnvHelpers
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from apiApp.helpers.sm_horizon import StellarMapHorizonAPIHelpers
from apiApp.helpers.sm_utils import StellarMapParsingUtilityHelpers
from apiApp.managers import (StellarCreatorAccountLineageManager,
                             UserInquirySearchHistoryManager)
from apiApp.services import AstraDocument
from django.core.management.base import BaseCommand
from django.http import HttpRequest


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
                        
                        # set environment
                        env_helpers = EnvHelpers()
                        network_name = lin_queryset.network_name
                        if network_name == 'public':
                            env_helpers.set_public_network()
                        else:
                            env_helpers.set_testnet_network()

                        account_id = lin_queryset.stellar_account
                        if lin_queryset.status == 'PENDING_HORIZON_API_DATASETS':
                            horizon_url = env_helpers.get_base_horizon()

                            # update status to IN_PROGRESS
                            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS')

                            # call horizon accounts
                            sm_horizon_helpers = StellarMapHorizonAPIHelpers(horizon_url=horizon_url, account_id=account_id)
                            sm_horizon_helpers.set_cron_name(cron_name=cron_name)
                            accounts_dict = sm_horizon_helpers.get_base_accounts()

                            # build external horizon url
                            ext_horiz_acc = f"{horizon_url}/accounts/{account_id}"

                            # set documentid 
                            doc_id = ''
                            if lin_queryset.horizon_accounts_doc_api_href is not None:
                                util_helpers = StellarMapParsingUtilityHelpers()
                                doc_id = util_helpers.get_documentid_from_url_address(url_address=lin_queryset.horizon_accounts_doc_api_href)
                            else:
                                doc_id = str(uuid.uuid4())

                            # Failed to PATCH document. Response: b'{"description":"Array paths contained in 
                            # square brackets, periods, single quotes, and backslash are not allowed in
                            # field names, invalid field config.memo_required","code":400}'
                            for key in accounts_dict['data'].keys():
                                new_key = re.sub(r'[^\w]+', '_', key)
                                if key != new_key:
                                    accounts_dict['data'][new_key] = accounts_dict['data'].pop(key)

                            # store and patch in cassandra document api
                            astra_doc = AstraDocument()
                            astra_doc.set_document_id(document_id=doc_id)
                            astra_doc.set_collections_name(collections_name='horizon_accounts')
                            res_dict = astra_doc.patch_document(
                                stellar_account=account_id,
                                network_name=network_name,
                                external_url=ext_horiz_acc,
                                raw_data=accounts_dict,
                                cron_name=cron_name
                            )

                            # store document href on db
                            request = HttpRequest()
                            request.data = {
                                'horizon_accounts_doc_api_href': res_dict.get("href"),
                                'status': 'DONE_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS'
                            }

                            # update lineage
                            lineage_manager.update_lineage(id=lin_queryset.id, request=request)

                        elif lin_queryset.status == 'DONE_COLLECTING_HORIZON_API_DATASETS_ACCOUNTS':
                            horizon_url = env_helpers.get_base_horizon()

                            # update status to IN_PROGRESS
                            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_OPERATIONS')

                            # call horizon operations
                            sm_horizon_helpers = StellarMapHorizonAPIHelpers(horizon_url=horizon_url, account_id=account_id)
                            sm_horizon_helpers.set_cron_name(cron_name=cron_name)
                            operations_dict = sm_horizon_helpers.get_account_operations()

                            # converts dictionary to json
                            # operations_json = json.dumps(operations_list)

                            # build external horizon url
                            ext_horiz_ops = f"{horizon_url}/accounts/{account_id}/operations"

                            # set documentid
                            doc_id = ''
                            if lin_queryset.horizon_accounts_operations_doc_api_href is not None:
                                util_helpers = StellarMapParsingUtilityHelpers()
                                doc_id = util_helpers.get_documentid_from_url_address(url_address=lin_queryset.horizon_accounts_operations_doc_api_href)
                            else:
                                doc_id = str(uuid.uuid4())

                            # store and patch in cassandra document api
                            astra_doc = AstraDocument()
                            astra_doc.set_document_id(document_id=doc_id)
                            astra_doc.set_collections_name(collections_name='horizon_operations')
                            res_dict = astra_doc.patch_document(
                                stellar_account=account_id,
                                network_name=network_name,
                                external_url=ext_horiz_ops,
                                raw_data=operations_dict,
                                cron_name=cron_name
                            )

                            # store document href on db
                            request = HttpRequest()
                            request.data = {
                                'horizon_accounts_operations_doc_api_href': res_dict.get("href"),
                                'status': 'DONE_COLLECTING_HORIZON_API_DATASETS_OPERATIONS'
                            }

                            # update lineage
                            lineage_manager.update_lineage(id=lin_queryset.id, request=request)

                        elif lin_queryset.status == 'DONE_COLLECTING_HORIZON_API_DATASETS_OPERATIONS':
                            horizon_url = env_helpers.get_base_horizon()

                            # update status to IN_PROGRESS
                            lineage_manager.update_status(id=lin_queryset.id, status='IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS_EFFECTS')

                            # call horizon effects
                            sm_horizon_helpers = StellarMapHorizonAPIHelpers(horizon_url=horizon_url, account_id=account_id)
                            sm_horizon_helpers.set_cron_name(cron_name=cron_name)
                            effects_dict = sm_horizon_helpers.get_account_effects()

                            # converts dictionary to json
                            # effects_json = json.dumps(effects_list)

                            # build external horizon url
                            ext_horiz_eff = f"{horizon_url}/accounts/{account_id}/effects"

                            # set documentid 
                            doc_id = ''
                            if lin_queryset.horizon_accounts_effects_doc_api_href is not None:
                                util_helpers = StellarMapParsingUtilityHelpers()
                                doc_id = util_helpers.get_documentid_from_url_address(url_address=lin_queryset.horizon_accounts_effects_doc_api_href)
                            else:
                                doc_id = str(uuid.uuid4())

                            # store and patch in cassandra document api
                            astra_doc = AstraDocument()
                            astra_doc.set_document_id(document_id=doc_id)
                            astra_doc.set_collections_name(collections_name='horizon_effects')
                            res_dict = astra_doc.patch_document(
                                stellar_account=account_id,
                                network_name=network_name,
                                external_url=ext_horiz_eff,
                                raw_data=effects_dict,
                                cron_name=cron_name
                            )

                            # store document href on db
                            request = HttpRequest()
                            request.data = {
                                'horizon_accounts_effects_doc_api_href': res_dict.get("href"),
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
