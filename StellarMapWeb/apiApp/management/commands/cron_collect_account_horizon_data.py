import sentry_sdk
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from apiApp.managers import (StellarCreatorAccountLineageManager,
                             UserInquirySearchHistoryManager)
from django.core.management.base import BaseCommand
from django.http import HttpRequest


class Command(BaseCommand):
    help = ('This management command is a scheduled task that creates the parent lineage '
        'information from the Horizon API and persistently stores it in the database.')

    def handle(self, *args, **options):
        try:
            # create an instance of cron helpers to check for cron health
            cron_helpers = StellarMapCronHelpers(cron_name='cron_make_parent_account_lineage')
            if cron_helpers.check_cron_health() is True:

                # Create an instance of the manager
                lineage_manager = StellarCreatorAccountLineageManager()

                # Query 1 record with status PENDING_HORIZON_API_DATASETS
                lin_queryset = lineage_manager.get_queryset(
                    status__in=['PENDING_HORIZON_API_DATASETS']
                )

                # Query 1 record with status starting with IN_PROGRESS_COLLECTING if in progress
                lin_in_progress_qs = lineage_manager.get_queryset(
                    status__startswith='IN_PROGRESS_COLLECTING'
                )

                # Due to rate limiting from the API server, we will only work on 1 pull at a time
                # Continue Horizon collection if found a PENDING_ record and no other records IN_PROGRESS
                if lin_queryset and not lin_in_progress_qs:
                    # updated status in UserInquirySearchHistory
                    lineage_manager.update_inquiry(id=lin_queryset.id, status='IN_PROGRESS_COLLECTING_HORIZON_API_DATASETS')

                    try:
                        # TODO: call horizon account ops, effects, or transactions
                        PENDING = 'PENDING_HORIZON_API_DATASETS_'
                        if lin_queryset:
                            # TODO: update datetime only if 3 hours passed
                            
                            
                            lineage_manager.update_lineage(id=lin_queryset.id, status=PENDING)
                        # else:

                            # request = HttpRequest()
                            # request.data = {
                            #     'stellar_account': lin_queryset.stellar_account,
                            #     'network_name': lin_queryset.network_name,
                            #     'status': PENDING
                            # }

                            # lineage_manager.create_lineage(request)

                        # updated status in UserInquirySearchHistory
                        lineage_manager.update_inquiry(id=lin_queryset.id, status='DONE_MAKE_PARENT_LINEAGE')

                    except Exception as e:
                        sentry_sdk.capture_exception(e)
                        raise ValueError(f'Error: {e}. Attempting to enter parent account in StellarCreatorAccountLineage')

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'cron_make_parent_account_lineage Error: {e}')


        self.stdout.write(self.style.SUCCESS('Successfully ran cron_make_parent_account_lineage'))
