import sentry_sdk
from django.core.management.base import BaseCommand
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from apiApp.helpers.sm_datetime import StellarMapDateTimeHelpers

class Command(BaseCommand):
    help = 'Checks the health status of crons and updates their status accordingly'

    def handle(self, *args, **options):
        try:
            # Create an instance of StellarMapCronHelpers and StellarMapDateTimeHelpers
            cron_helpers = StellarMapCronHelpers(cron_name='cron_health_check')
            
            # Do not use .check_cron_health() in cron_health_check 
            # as it will never enter the logic to re-initiate the crons
            # if cron_helpers.check_cron_health() is True:

            date_helpers = StellarMapDateTimeHelpers()

            # Get the health status of all crons
            cron_status = cron_helpers.check_all_crons_health()

            # Set the current datetime
            date_helpers.set_datetime_obj()

            # get the current datetime obj
            the_current_date_time_obj = date_helpers.get_datetime_obj()

            if cron_status is not None:
                
                # loop through all latest cron jobs and check if 
                
                for cron_name, status in cron_status:
                    # Get the created_at time of the latest record of the cron
                    created_at = cron_status[cron_name]['created_at']
                    time_difference = the_current_date_time_obj - created_at

                    # The cron job that encounters rate limiting should be the 
                    # one to set all crons as "UNHEALTHY_"

                    # This condition assumes that enough time has elapsed to provide 
                    # a buffer between the last recorded "UNHEALTHY_" status. 

                    # Check if ANY cron's status contains the string "UNHEALTHY_" AND
                    # Check if the difference between the current time 
                    # and the created_at time is greater than 1.7 hours.
                    # Set all crons to "HEALTHY" to re-initiate them. 
                    if 'UNHEALTHY_' in status and time_difference.total_seconds() >= (1.7 * 60 * 60):
                        cron_helpers.set_crons_healthy()

        except Exception as e:
            sentry_sdk.capture_exception(e)

