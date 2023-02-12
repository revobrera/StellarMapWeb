import sentry_sdk
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from stellar_sdk import Server
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_error_callback


class StellarMapHorizonAPIHelpers:
    """
    This class provides helper functions to interact with the Horizon API provided by the Stellar network.

    Note: 
        All exponential retries are set the following:
            `wait=wait_random_exponential(multiplier=1, max=71)` specifies the wait time between retries. 
            It uses an exponential backoff algorithm with a random multiplier between 1 and
            max (71 in this case), meaning the wait time between retries will increase exponentially
            with each retry and also be randomized.

            `stop=stop_after_attempt(7)` specifies that the retries should stop after 7 attempts.

            `retry_error_callback=on_retry_failure` specifies a callback function that will be 
            called every time a retry fails. In this case, it is the function on_retry_failure, 
            which is expected to handle the error, such as logging the exception to Sentry, and 
            performing any necessary cleanup, reporting and then sets the cron jobs as 'UNHEALTHY_'

            `cron_health_check` will set the crons to 'HEALTHY_' after 1.7 hours of buffer.
    """

    def __init__(self, horizon_url, account_id):
        """
        Initializes the class with the Horizon API URL and the account ID.

        :param horizon_url: Horizon API URL
        :type horizon_url: str
        :param account_id: Account ID
        :type account_id: str
        """
        self.server = Server(horizon_url=horizon_url) # Create a server instance with the given horizon API URL
        self.account_id = account_id

    def set_cron_name(self, cron_name):
        """
        Set the name of the cron job for reporting purposes.

        This method should be called before making any calls to the
        `StellarMapHorizonAPIHelpers` class from a cron job. This will allow the
        `on_retry_failure` callback to include the name of the cron job when
        reporting errors.

        Args:
            cron_name (str): The name of the cron job.
        """
        self.cron_name = cron_name

    def get_cron_name(self):
        return self.cron_name

    def on_retry_failure(self, retry_state):
        # This function will be called every time a retry fails
        # Log the exception using Sentry SDK
        sentry_sdk.capture_exception(retry_state.outcome.exception())
        # Call set_crons_unhealthy method of StellarMapCronHelpers class
        cron_helpers = StellarMapCronHelpers(cron_name=self.get_cron_name())
        cron_helpers.set_crons_unhealthy()

    @retry(wait=wait_random_exponential(multiplier=1, max=71),
       stop=stop_after_attempt(7),
       retry_error_callback=on_retry_failure)
    def get_base_accounts(self):
        """
        Gets base account info.

        :return: List of base account
        :rtype: list
        """
        try:
            # Fetch base account
            base_account = self.server.accounts().call()
            return base_account
        except Exception as e:
            sentry_sdk.capture_exception(e)
    
    @retry(wait=wait_random_exponential(multiplier=1, max=71),
       stop=stop_after_attempt(7),
       retry_error_callback=on_retry_failure)
    def get_account_operations(self):
        """
        Gets all operations for the account specified.

        :return: List of operations
        :rtype: list
        """
        try:
            # Fetch operations for the specified account
            ops = self.server.operations().for_account(account_id=self.account_id).call()
            return ops
        except Exception as e:
            sentry_sdk.capture_exception(e)

    @retry(wait=wait_random_exponential(multiplier=1, max=71),
       stop=stop_after_attempt(7),
       retry_error_callback=on_retry_failure)
    def get_account_effects(self):
        """
        Gets all effects for the account specified.

        :return: List of effects
        :rtype: list
        """
        try:
            # Fetch effects for the specified account
            efxs = self.server.effects().for_account(account_id=self.account_id).call()
            return efxs
        except Exception as e:
            sentry_sdk.capture_exception(e)
    
    @retry(wait=wait_random_exponential(multiplier=1, max=71),
       stop=stop_after_attempt(7),
       retry_error_callback=on_retry_failure)
    def get_account_transactions(self):
        """
        Gets all transactions for the account specified.

        :return: List of transactions
        :rtype: list
        """
        try:
            # Fetch transactions for the specified account
            txns = self.server.transactions().for_account(account_id=self.account_id).call()
            return txns
        except Exception as e:
            sentry_sdk.capture_exception(e)
