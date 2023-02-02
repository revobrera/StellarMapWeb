import pandas as pd
import sentry_sdk
from decouple import config
from django.db import connections

from .helpers.sm_datetime import StellarMapDateTimeHelpers
from .models import (ManagementCronHealthHistory, StellarAccountInquiryHistory,
                     StellarAccountLineage)


class StellarAccountInquiryHistoryManager():
    """
    Manager class for the StellarAccountInquiryHistory model.
    
    Usage:
    ```
    # create an instance of the manager
    inquiry_manager = StellarAccountInquiryHistoryManager()
    
    # create an inquiry
    inquiry = inquiry_manager.create_inquiry(
        id='unique_id',
        stellar_account='GBY4C4B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B',
        network_name='testnet',
        status='success'
    )
    
    # update an inquiry
    inquiry_manager.update_inquiry(
        id='unique_id',
        stellar_account='GBY4C4B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B4Y3B',
        network_name='mainnet',
        status='failed'
    )
    ```
    """

    def get_queryset(self, **kwargs):
        """
        Returns a queryset filtered by the given keyword arguments.
        
        :param kwargs: keyword arguments to filter the queryset by
        :return: a filtered queryset
        
        """
        
        try:
            return StellarAccountInquiryHistory.objects.filter(**kwargs).first()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def create_inquiry(self, request, *args, **kwargs):
        """
        Creates an inquiry with the given information
        
        :param request: the request object
        :param args: additional positional arguments
        :param kwargs: additional key-value arguments
        :return: the created inquiry
        """

        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # add the created_at field to the request
            request.data['created_at'] = date_obj

            return StellarAccountInquiryHistory.objects.create(**request.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def update_inquiry(self, id, status):
        """
        Updates an inquiry with the given id.

        :param id: the id of the inquiry to update
        :param status: the status of the inquiry to update
        :return: the updated inquiry
        """
        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # get the inquiry instance
            inquiry = self.get_queryset(id=id)
            
            return inquiry.update(
                status = status,
                updated_at = date_obj
            )
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e


class StellarAccountLineageManager():

    def get_queryset(self, **kwargs):
        """
        Returns a queryset filtered by the given keyword arguments.
        
        :param kwargs: keyword arguments to filter the queryset by
        :return: a filtered queryset
        
        """
        
        try:
            return StellarAccountLineage.objects.filter(**kwargs).first()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def create_lineage(self, request, *args, **kwargs):
        """
        Creates an lineage with the given information
        
        :param request: the request object
        :param args: additional positional arguments
        :param kwargs: additional key-value arguments
        :return: the created lineage
        """

        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # add the created_at field to the request
            request.data['created_at'] = date_obj

            return StellarAccountLineage.objects.create(**request.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def update_lineage(self, id, status):
        """
        Updates an lineage with the given id.

        :param id: the id of the lineage to update
        :param status: the status of the lineage to update
        :return: the updated lineage
        """
        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # get the lineage instance
            lineage = self.get_queryset(id=id)
            
            return lineage.update(
                status = status,
                updated_at = date_obj
            )
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e


class ManagementCronHealthHistoryManager():

    def get_queryset(self, **kwargs):
        """
        Returns a queryset filtered by the given keyword arguments.
        
        :param kwargs: keyword arguments to filter the queryset by
        :return: a filtered queryset
        
        """
        
        try:
            return ManagementCronHealthHistory.objects.filter(**kwargs).first()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def create_cron_health(self, request, *args, **kwargs):
        """
        Creates a cron_health with the given information
        
        :param request: the request object
        :param args: additional positional arguments
        :param kwargs: additional key-value arguments
        :return: the created cron_health
        """

        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # add the created_at field to the request
            request.data['created_at'] = date_obj

            return ManagementCronHealthHistory.objects.create(**request.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def update_cron_health(self, id, status):
        """
        Updates an cron_health with the given id.

        :param id: the id of the cron_health to update
        :param status: the status of the cron_health to update
        :return: the updated cron_health
        """
        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # get the cron_health instance
            cron_health = self.get_queryset(id=id)
            
            return cron_health.update(
                status = status,
                updated_at = date_obj
            )
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def get_latest_record(self, cron_name):
        """
        Returns the most recent record for the given cron_name.

        :param cron_name: the name of the cron job
        :return: the most recent record for the cron_name
        """
        try:
            return ManagementCronHealthHistory.objects.filter(cron_name=cron_name).order_by('-created_at')[:1]
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def get_distinct_cron_names(self):
        try:
            # query all latest distinct cron names
            # cron_names = ManagementCronHealthHistory.objects.values("cron_name").distinct()
            
            CASSANDRA_DB_NAME = config('CASSANDRA_DB_NAME')
            connection = connections["cassandra"]
            session = connection.connection.session
            session.set_keyspace(CASSANDRA_DB_NAME)

            cql_query = "SELECT cron_name FROM management_cron_health_history limit 171;"
            result_df = pd.DataFrame(session.execute(cql_query))

            # using pandas to drop duplicates
            result_df = result_df.drop_duplicates()

            # convert to dictionary and orient as records
            cron_names_dict = result_df.to_dict('records')

            return cron_names_dict
        except Exception as e:
            # log the error to Sentry
            sentry_sdk.capture_exception(e)
            raise e
