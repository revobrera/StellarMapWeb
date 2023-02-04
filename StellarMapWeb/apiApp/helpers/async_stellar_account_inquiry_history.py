from apiApp.models import UserInquirySearchHistory
from django.db import transaction


class AsyncStellarInquiryCreator:
    """
    This class provides an async method for creating an inquiry
    for a Stellar account.

    The async keyword is used in the method definition to indicate
    that the method is an asynchronous method.

    In this case, you are using the Django ORM which is synchronous.
    And the async keyword is used to indicate that the method is asynchronous,
    but it doesn't mean that the method will run asynchronously. Async in this
    case means that the method is a coroutine, which means that it can be awaited
    by other coroutines, but the method itself is still executed synchronously.

    To run this method asynchronously, use asyncio library to call asyncio.run()
    or asyncio.create_task().

    """

    async def create_inquiry(self, stellar_account, network_name, status):
        """
        Creates a new inquiry for a Stellar account.
        
        Parameters:
            - stellar_account (str): The Stellar account address.
            - network_name (str): The network name the Stellar account belongs to.
        
        Returns:
            - inquiry (UserInquirySearchHistory): The newly created inquiry object.
        """
        try:
            async with transaction.atomic():
                # Start a database transaction
                # Using the transaction.atomic() context manager, you can run the database
                # operations in an atomic transaction, and in case of an exception,
                # the transaction will be rolled back and the database state will be preserved.

                inquiry = UserInquirySearchHistory(stellar_account=stellar_account, network_name=network_name, status=status)
                await inquiry.save()

            return inquiry
        except Exception as e:
            return e
