import sentry_sdk
from apiApp.helpers.sm_horizon import StellarMapHorizonAPIParserHelpers
from apiApp.managers import StellarCreatorAccountLineageManager
from apiApp.services import AstraDocument
from django.http import HttpRequest


class StellarMapCreatorAccountLineageHelpers:

    def async_update_from_raw_data(self, client_session, lin_queryset, *args, **kwargs):

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




