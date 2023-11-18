import sentry_sdk
from apiApp.helpers.sm_async import StellarMapAsyncHelpers
from apiApp.helpers.sm_creatoraccountlineage import \
    StellarMapCreatorAccountLineageHelpers
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from apiApp.managers import StellarCreatorAccountLineageManager
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('This management command is a scheduled task that populates the '
        'horizon_accounts_assets_doc_api_href and persistently stores it in the database.')

    def handle(self, *args, **options):
        try:
            # create an instance of cron helpers to check for cron health
            cron_helpers = StellarMapCronHelpers(cron_name='cron_collect_account_lineage_assets')
            if cron_helpers.check_cron_health() is True:

                # Create an instance of async
                async_helpers = StellarMapAsyncHelpers()
                
                # Create an instance of StellarCreatorAccountLineageManager
                lineage_manager = StellarCreatorAccountLineageManager()

                # Query all records matching status from StellarCreatorAccountLineage
                lin_queryset = lineage_manager.get_all_queryset(
                    status__in=['DONE_UPDATING_FROM_RAW_DATA']
                )
                
                # Create an instance of StellarMapCreatorAccountLineageHelpers
                lineage_helpers = StellarMapCreatorAccountLineageHelpers()

                # Run the async tasks with the custom function
                async_helpers.execute_async(lin_queryset, lineage_helpers.async_horizon_accounts_assets_doc_api_href_from_accounts_raw_data)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'cron_collect_account_lineage_assets Error: {e}')
