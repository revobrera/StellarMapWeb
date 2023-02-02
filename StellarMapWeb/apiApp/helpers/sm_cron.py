import sentry_sdk
from apiApp.managers import ManagementCronHealthHistoryManager

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
            cron_health = ManagementCronHealthHistoryManager()
            cron_health_qs = cron_health.get_latest_record(cron_name=self.cron_name)

            for latest_cron_record in cron_health_qs:
                if latest_cron_record:
                    # if cron health exists and HEALTHY
                    if latest_cron_record.status == 'HEALTHY':
                        return True
                    else:
                        # stop cron from executing
                        return False

                else:
                    # create initial cron record
                    request_data = {
                        'cron_name': self.cron_name,
                        'status': self.status
                    }
                    ManagementCronHealthHistoryManager().create_cron_health(request=request_data)
                    return True
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return False

    def set_crons_unhealthy(self):
        try:
            # query all latest distinct cron names
            cron_names_df_dict = ManagementCronHealthHistoryManager().get_distinct_cron_names()

            # set all these cron status' to UNHEALTHY due to exponential algorithm failing
            for row in cron_names_df_dict:
                # exclude cron_health_check
                if row['cron_name'] != 'cron_health_check':
                    request_data = {
                        'cron_name': row['cron_name'],
                        'status': 'UNHEALTHY_DUE_TO_RATE_LIMITING_FROM_EXTERNAL_API_SERVER'
                    }
                    ManagementCronHealthHistoryManager().create_cron_health(request=request_data)
        except Exception as e:
            # Log the error to Sentry
            sentry_sdk.capture_exception(e)


    def set_crons_healthy(self):
        try:
            cron_names_df_dict = ManagementCronHealthHistoryManager().get_distinct_cron_names()

            for row in cron_names_df_dict:
                request_data = {
                    'cron_name': row['cron_name'],
                    'status': 'HEALTHY'
                }
                ManagementCronHealthHistoryManager().create_cron_health(request=request_data)
        except Exception as e:
            sentry_sdk.capture_exception(e)


    def check_all_crons_health(self):
        try:
            cron_names_df_dict = ManagementCronHealthHistoryManager().get_distinct_cron_names()
            cron_health = {}

            for row in cron_names_df_dict:
                cron_name = row['cron_name']
                latest_record = ManagementCronHealthHistoryManager().get_latest_record(cron_name=cron_name)
                cron_health[cron_name] = {'status': latest_record.status, 'created_at': latest_record.created_at}

            return cron_health
        except Exception as e:
            sentry_sdk.capture_exception(e)





