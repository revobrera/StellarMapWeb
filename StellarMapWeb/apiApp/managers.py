import sentry_sdk
from .helpers.sm_datetime import StellarMapDateTimeHelpers
from .models import StellarAccountInquiryHistory

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
            return StellarAccountInquiryHistory.objects.filter(**kwargs).limit(0)
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

            # add the created_at field to the kwargs
            kwargs['created_at'] = date_obj

            return StellarAccountInquiryHistory.objects.create(**kwargs)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def update_inquiry(self, id):
        """
        Updates an inquiry with the given id.

        :param id: the id of the inquiry to update
        :return: the updated inquiry
        """
        try:
            # get datetime object
            dt_helpers = StellarMapDateTimeHelpers()
            dt_helpers.set_datetime_obj()
            date_obj = dt_helpers.get_datetime_obj()

            # get the inquiry instance
            inquiry = StellarAccountInquiryHistory.objects.filter(id=id).limit(1)
            if inquiry:
                inquiry.status = "RE_INQUIRY"
                inquiry.updated_at = date_obj
                inquiry.save()
                return inquiry
            else:
                return None
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e



    