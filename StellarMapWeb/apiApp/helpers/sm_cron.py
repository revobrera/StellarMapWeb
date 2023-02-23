import sentry_sdk
from apiApp.managers import ManagementCronHealthManager
from django.http import HttpRequest


class StellarMapCronHelpers:
    def __init__(self, cron_name, status='HEALTHY'):
        """ Initializes the class with cron_name and status

        Args:
            cron_name (str): name of the cron
            status (str): status of the cron, defaults to 'HEALTHY'
        """
        self.cron_name = cron_name
        self.status = status

    def check_cron_health(self):
        """
        This method is called ONLY from a cron to check the health of the cron.
        It retrieves the most recent record of the cron based on name.
        If the record exists and the status is 'HEALTHY', returns True.
        If the record exists and the status is not 'HEALTHY', returns False.
        If the record does not exist, creates an initial record with the given cron_name and status, and returns True.
        
        Returns:
            bool: returns True if the cron is healthy or initial record is created, False otherwise
        
        """
        try:

            # check most recent record of the cron based on name
            cron_health = ManagementCronHealthManager()
            cron_health_df = cron_health.get_latest_record(cron_name=self.cron_name)

            # check if the df is empty
            if not cron_health_df.empty:
                # df is not empty; iterate through the rows of the DataFrame
                for idx, row in cron_health_df.iterrows():
                    # if cron health exists and HEALTHY
                    if row['status'] == 'HEALTHY':
                        return True
                    else:
                        # stop cron from executing
                        return False

            else:
                # df is empty; create initial cron record
                request = HttpRequest()
                request.data = {
                    'cron_name': self.cron_name,
                    'status': self.status
                }
                ManagementCronHealthManager().create_cron_health(request=request)
                return True
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return False

    def set_crons_unhealthy(self):
        try:
            # query all latest distinct cron names
            cron_names_list = ManagementCronHealthManager().get_distinct_cron_names()

            # set all these cron status' to UNHEALTHY due to exponential algorithm failing
            for elmnt in cron_names_list:
                # exclude cron_health_check
                if elmnt != 'cron_health_check':
                    request = HttpRequest()
                    request.data = {
                        'cron_name': elmnt,
                        'status': 'UNHEALTHY_DUE_TO_RATE_LIMITING_FROM_EXTERNAL_API_SERVER'
                    }
                    ManagementCronHealthManager().create_cron_health(request=request)

        except Exception as e:
            # Log the error to Sentry
            sentry_sdk.capture_exception(e)


    def set_crons_healthy(self):
        try:
            cron_names_list = ManagementCronHealthManager().get_distinct_cron_names()

            for elmnt in cron_names_list:
                request = HttpRequest()
                request.data = {
                    'cron_name': elmnt,
                    'status': 'HEALTHY'
                }
                ManagementCronHealthManager().create_cron_health(request=request)
        except Exception as e:
            sentry_sdk.capture_exception(e)


    def check_all_crons_health(self):
        try:
            cron_names_list = ManagementCronHealthManager().get_distinct_cron_names()
            cron_health = {}

            if cron_names_list:
                for elmnt in cron_names_list:
                    cron_name = elmnt
                    latest_record_df = ManagementCronHealthManager().get_latest_record(cron_name=cron_name)

                    # check if the df is empty
                    if not latest_record_df.empty:
                        # df is not empty; iterate through the rows of the DataFrame
                        for idx, row in latest_record_df.iterrows():
                            cron_health[row['cron_name']] = {'status': row['status'], 'created_at': row['created_at']}

            return cron_health
        except Exception as e:
            sentry_sdk.capture_exception(e)





