import asyncio
from tenacity import retry, stop_after_attempt

from django.db.models import Q
from django.core.management.base import BaseCommand
from apiApp.managers import UserInquirySearchHistoryManager, StellarCreatorAccountLineageManager
from apiApp.helpers.sm_conn import AsyncStellarMapHTTPHelpers
from apiApp.helpers.env import EnvHelpers
from decouple import config
import sentry_sdk

class Command(BaseCommand):
    help = ('This management command is a scheduled task that retrieves creator account'
        'information from the Horizon API and persistently stores it in the database.')

    async def handle(self, *args, **options):
        @retry(reraise=True, stop=stop_after_attempt(17))
        async def make_child_lineage():
            # Create an instance of the manager
            inquiry_manager = UserInquirySearchHistoryManager()

            # Query 1 record with status PENDING or RE_INQUIRY
            queryset = inquiry_manager.get_queryset(
                Q(status='PENDING') | Q(status='RE_INQUIRY')
            )

            environ = config('ENV')
            # network
            net = EnvHelpers()
            if environ == 'production':
                net.set_public_network()
            else:
                net.set_testnet_network()

            # http request
            uri = f"{net.get_base_horizon_account}/{queryset.stellar_account}"
            req = AsyncStellarMapHTTPHelpers()
            req.add_url(uri)

            try:
                req_response = await req.get()

                # store records in StellarCreatorAccountLineage
                lineage_manager = StellarCreatorAccountLineageManager()

                lin_queryset = lineage_manager.get_queryset(
                    stellar_account=queryset.stellar_account,
                    network_name=queryset.network_name
                )

                
                if lin_queryset:
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
                        status='PENDING'
                    )

            except Exception as e:
                sentry_sdk.capture_exception(e)
                raise ValueError(f'Error: {e}')

        try:
            await make_child_lineage()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'Error: {e}')

        self.stdout.write(self.style.SUCCESS('Successfully ran the example command'))
