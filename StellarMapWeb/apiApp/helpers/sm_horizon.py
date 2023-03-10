import json

import sentry_sdk
from apiApp.helpers.sm_cron import StellarMapCronHelpers
from apiApp.helpers.sm_datetime import StellarMapDateTimeHelpers
from stellar_sdk import Server
from tenacity import retry, stop_after_attempt, wait_random_exponential


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
        :rtype: json
        """
        try:
            # Fetch base account
            base_account = self.server.accounts().account_id(account_id=self.account_id).call()
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


class StellarMapHorizonAPIParserHelpers:
    """ 
    Note: This class parses the Horizon JSON dataset that is embedded into a custom
          StellarMap JSON formatted for Datastax Document API.
    """
    def set_datastax_response(self, datastax_response):
        self.datastax_response = datastax_response

    def parse_account_native_balance(self):
        response_dict = self.datastax_response

        # check if 'balances' data property is present
        if 'balances' in response_dict['data']['raw_data']:
            # iterate and check if balance data property is present
            for trnx in response_dict['data']['raw_data']['balances']:
                if (trnx['asset_type'] == 'native') and (float(trnx['balance']) > 0):
                    return float(trnx['balance'])
                else:
                    # No matching XLM asset_type or asset_code
                    return 0.00
        else:
            # No XLM balance
            return 0.0
            
    def parse_account_home_domain(self):
        response_dict = self.datastax_response

        # check if 'home_domain' data property is present
        if 'home_domain' in response_dict['data']['raw_data']:
            # get the home_domain value
            return response_dict['data']['raw_data']['home_domain']
        else:
            return "no_element_home_domain"
        
    def parse_operations_creator_account(self, stellar_account):
        response_dict = self.datastax_response

        for record in response_dict['data']['raw_data']["_embedded"]["records"]:
            if record["type"] == "create_account" and record["account"] == stellar_account:
                funder = record["funder"]
                created_at = record["created_at"]

                # convert horizon datetime str to cassandra datetime obj
                datetime_helpers = StellarMapDateTimeHelpers()
                datetime_helpers.set_horizon_datetime_str(horizon_datetime_str=created_at)
                created_at_obj = datetime_helpers.convert_horizon_datetime_str_to_obj()

                creator_dict = {
                    "funder": funder,
                    "created_at": created_at_obj
                }
                return creator_dict
