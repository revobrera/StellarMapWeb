import sentry_sdk
from django.http import HttpRequest
from django.core.management.base import BaseCommand
from apiApp.managers import StellarAccountInquiryHistoryManager, StellarAccountLineageManager
from apiApp.helpers.sm_cron import StellarMapCronHelpers

class Command(BaseCommand):
    help = ('This management command is a scheduled task that creates the parent lineage '
        'information from the Horizon API and persistently stores it in the database.')

    def handle(self, *args, **options):
        try:
            # create an instance of cron helpers to check for cron health
            cron_helpers = StellarMapCronHelpers(cron_name='cron_make_parent_account_lineage')
            if cron_helpers.check_cron_health is True:

                # Create an instance of the manager
                inquiry_manager = StellarAccountInquiryHistoryManager()

                # Query 1 record with status PENDING or RE_INQUIRY
                inq_queryset = inquiry_manager.get_queryset(
                    status__in=['PENDING_MAKE_PARENT_LINEAGE', 'RE_INQUIRY']
                )

                # updated status in StellarAccountInquiryHistory
                inquiry_manager.update_inquiry(id=inq_queryset.id, status='IN_PROGRESS_MAKE_PARENT_LINEAGE')
            
                # Create an instance of StellarAccountLineageManager
                lineage_manager = StellarAccountLineageManager()

                # Query 1 record from StellarAccountLineage
                lin_queryset = lineage_manager.get_queryset(
                    stellar_account=inq_queryset.stellar_account,
                    network_name=inq_queryset.network_name
                )

                try:
                    PENDING = 'PENDING_HORIZON_API_DATASETS'
                    if lin_queryset:
                        # TODO: update datetime only if 3 hours passed
                        lineage_manager.update_lineage(id=lin_queryset.id, status=PENDING)
                    else:
                        request = HttpRequest()
                        request.data = {
                            'stellar_account': inq_queryset.stellar_account,
                            'network_name': inq_queryset.network_name,
                            'status': PENDING
                        }

                        lineage_manager.create_lineage(request)

                    # updated status in StellarAccountInquiryHistory
                    inquiry_manager.update_inquiry(id=inq_queryset.id, status='DONE_MAKE_PARENT_LINEAGE')

                except Exception as e:
                    sentry_sdk.capture_exception(e)
                    raise ValueError(f'Error: {e}. Attempting to enter parent account in StellarAccountLineage')

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'cron_make_parent_account_lineage Error: {e}')


        self.stdout.write(self.style.SUCCESS('Successfully ran cron_make_parent_account_lineage'))
