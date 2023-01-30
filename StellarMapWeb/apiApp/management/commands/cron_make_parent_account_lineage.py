from django.http import HttpRequest
from django.core.management.base import BaseCommand
from apiApp.managers import StellarAccountInquiryHistoryManager, StellarAccountLineageManager
import sentry_sdk

class Command(BaseCommand):
    help = ('This management command is a scheduled task that creates the parent lineage '
        'information from the Horizon API and persistently stores it in the database.')

    def handle(self, *args, **options):
        try:
            # Create an instance of the manager
            inquiry_manager = StellarAccountInquiryHistoryManager()

            # Query 1 record with status PENDING or RE_INQUIRY
            queryset = inquiry_manager.get_queryset(
                status__in=['PENDING_MAKE_PARENT_LINEAGE', 'RE_INQUIRY']
            )
        
            # Create an instance of StellarAccountLineageManager
            lineage_manager = StellarAccountLineageManager()

            # Query 1 record from StellarAccountLineage
            lin_queryset = lineage_manager.get_queryset(
                stellar_account=queryset.stellar_account,
                network_name=queryset.network_name
            )
            
            if lin_queryset:
                # TODO: update datetime only if 3 hours passed
                lineage_manager.update_lineage(id=lin_queryset.id)
            else:
                request = HttpRequest()
                request.data = {
                    'stellar_account': queryset.stellar_account,
                    'network_name': queryset.network_name,
                    'status': 'PENDING_HORIZON_API_DATASETS'
                }

                lineage_manager.create_lineage(request)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'Error: {e}')


        self.stdout.write(self.style.SUCCESS('Successfully ran cron_make_parent_account_lineage'))
