from datetime import datetime

import pandas as pd
import pytz
import sentry_sdk
from apiApp.helpers.sm_conn import CassandraConnectionsHelpers
from apiApp.helpers.sm_datetime import StellarMapDateTimeHelpers
from apiApp.models import (ManagementCronHealth, StellarCreatorAccountLineage,
                           UserInquirySearchHistory)


class UserInquirySearchHistoryManager():
    """
    Manager class for the UserInquirySearchHistory model.
    
    Usage:
    ```
    # create an instance of the manager
    inquiry_manager = UserInquirySearchHistoryManager()
    
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
            return UserInquirySearchHistory.objects.filter(**kwargs).first()
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

            return UserInquirySearchHistory.objects.create(**request.data)
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


class StellarCreatorAccountLineageManager():

    def get_queryset(self, **kwargs):
        """
        Returns a queryset filtered by the given keyword arguments.
        
        :param kwargs: keyword arguments to filter the queryset by
        :return: a filtered queryset
        
        """
        
        try:
            return StellarCreatorAccountLineage.objects.filter(**kwargs).first()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def get_all_queryset(self, **kwargs):
        """
        Returns a queryset filtered by the given keyword arguments.
        
        :param kwargs: keyword arguments to filter the queryset by
        :return: a filtered queryset
        
        """
        
        try:
            return StellarCreatorAccountLineage.objects.filter(**kwargs)
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

            return StellarCreatorAccountLineage.objects.create(**request.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def update_lineage(self, id, request, *args, **kwargs):
        """
        Updates an lineage with the given id.

        :param id: the id of the lineage to update
        :param request: the request object
        :param args: additional positional arguments
        :param kwargs: additional key-value arguments
        :return: the updated lineage
        """
        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # get the lineage instance
            lineage = self.get_queryset(id=id)

            # add the updated_at field to the request
            request.data['updated_at'] = date_obj

            return lineage.update(**request.data)
            
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def update_status(self, id, status):
        """
        Updates an lineage's status with the given id.

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


class ManagementCronHealthManager():

    def get_queryset(self, **kwargs):
        """
        Returns a queryset filtered by the given keyword arguments.
        
        :param kwargs: keyword arguments to filter the queryset by
        :return: a filtered queryset
        
        """
        
        try:
            return ManagementCronHealth.objects.filter(**kwargs).first()
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

            return ManagementCronHealth.objects.create(**request.data)
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
        Returns the most recent record today for the given cron_name.

        :param cron_name: the name of the cron job
        :return: the most recent record for the cron_name
        """
        try:
            # return ManagementCronHealth.objects.filter(cron_name=cron_name).order_by('-created_at').first()
            # The 'created_at' attribute is part of the composite primary key.
            # Since the model was defined with a clustering order of "DESC",
            # the first record retrieved for a specific 'cron_name' will be the
            # most recent one.
            # return ManagementCronHealth.objects.filter(cron_name=cron_name).first()

            date_helpers = StellarMapDateTimeHelpers()
            date_helpers.set_datetime_obj()
            the_current_date_str = date_helpers.get_date_str()

            conn_helpers = CassandraConnectionsHelpers()
            cql_query = f"SELECT * FROM management_cron_health WHERE cron_name='{cron_name}' AND created_at >= '{the_current_date_str} 00:00:00' AND created_at <= '{the_current_date_str} 23:59:59' LIMIT 17 ALLOW FILTERING;"

            conn_helpers.set_cql_query(cql_query)
            rows = conn_helpers.execute_cql()

            data_df = pd.DataFrame(rows)

            if not data_df.empty:
                # sort created_at descending
                data_df_sorted = data_df.sort_values('created_at', ascending=False)

                # row 1
                row_1_df = data_df_sorted.iloc[0]

                # returns a dataframe
                return row_1_df

            # returns an empty dataframe
            return pd.DataFrame()
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def get_distinct_cron_names(self):
        try:
            # query all latest distinct cron names
            conn_helpers = CassandraConnectionsHelpers()
            cql_query = "SELECT cron_name FROM management_cron_health limit 171;"

            conn_helpers.set_cql_query(cql_query)
            rows = conn_helpers.execute_cql()

            cron_names = []
            # iterate through all the rows and append element to list
            for row in rows:
                cron_names.append(row.cron_name)
            
            # set() stores only unique cron names 
            unique_cron_names = set(cron_names)

            # convert set back to list []
            unique_cron_names_list = list(unique_cron_names)

            conn_helpers.close_connection()

            return unique_cron_names_list
        except Exception as e:
            # log the error to Sentry
            sentry_sdk.capture_exception(e)
            raise e