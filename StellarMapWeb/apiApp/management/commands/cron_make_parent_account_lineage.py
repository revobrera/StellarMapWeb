from tenacity import retry, stop_after_attempt

from django.db.models import Q
from django.core.management.base import BaseCommand
from apiApp.managers import StellarAccountInquiryHistoryManager, StellarAccountLineageManager
import sentry_sdk

class Command(BaseCommand):
    help = ('This management command is a scheduled task that creates the parent lineage '
        'information from the Horizon API and persistently stores it in the database.')

    async def handle(self, *args, **options):
        @retry(reraise=True, stop=stop_after_attempt(17))
        async def make_parent_lineage():
            # Create an instance of the manager
            inquiry_manager = StellarAccountInquiryHistoryManager()

            # Query 1 record with status PENDING or RE_INQUIRY
            queryset = inquiry_manager.get_queryset(
                Q(status='PENDING_MAKE_PARENT_LINEAGE') | Q(status='RE_INQUIRY')
            )

            try:
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
                    lineage_manager.create_lineage(
                        # account_active=req_response.data[''],
                        # stellar_creator_account=req_response.data[''],
                        stellar_account=queryset.stellar_account,
                        # stellar_account_created_at=req_response.data[''],
                        network_name=queryset.network_name,
                        # home_domain=req_response.data[''],
                        # xlm_balance=req_response.data[''],
                        status='PENDING_HORIZON_API_DATASETS'
                    )

            except Exception as e:
                sentry_sdk.capture_exception(e)
                raise ValueError(f'Error: {e}')

        try:
            await make_parent_lineage()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'Error: {e}')

        self.stdout.write(self.style.SUCCESS('Successfully ran the make_parent_lineage command'))
