import sentry_sdk
from apiApp.helpers.sm_async import StellarMapAsyncHelpers
from apiApp.helpers.sm_creatoraccountlineage import \
    StellarMapCreatorAccountLineageHelpers
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from apiApp.managers import StellarCreatorAccountLineageManager
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('This management command is a scheduled task that creates grandparent accounts.')

    def handle(self, *args, **options):
        try:
            # create an instance of cron helpers to check for cron health
            cron_helpers = StellarMapCronHelpers(cron_name='cron_make_grandparent_account_lineage')
            if cron_helpers.check_cron_health() is True:

                # Create an instance of async
                async_helpers = StellarMapAsyncHelpers()
                
                # Create an instance of StellarCreatorAccountLineageManager
                lineage_manager = StellarCreatorAccountLineageManager()

                # Query all records matching status from StellarCreatorAccountLineage
                lin_queryset = lineage_manager.get_all_queryset(
                    status__in=['DONE_UPDATING_FROM_OPERATIONS_RAW_DATA']
                )
                
                # Create an instance of StellarMapCreatorAccountLineageHelpers
                lineage_helpers = StellarMapCreatorAccountLineageHelpers()

                # Run the async tasks with the custom function
                async_helpers.execute_async(lin_queryset, lineage_helpers.async_make_grandparent_account)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'cron_make_grandparent_account_lineage Error: {e}')



