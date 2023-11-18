import json

import sentry_sdk
from apiApp.helpers.sm_datetime import StellarMapDateTimeHelpers
from apiApp.helpers.sm_utils import StellarMapUtilityHelpers
from apiApp.services import AstraDocument
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
        sm_util = StellarMapUtilityHelpers()
        sm_util.on_retry_failure(retry_state, self.cron_name)

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
        
    def parse_account_assets(self):
        """
        Gets the account asset balances for the specified Stellar account.

        Not needed to make a request to the Horizon API.
        The JSON was stored already in horizon_accounts_doc_api_href
        Parse to get asset balances

        :return: Dictionary of asset balances
        :rtype: dict
        """
        try:
            response_dict = self.datastax_response

            # building child nodes of an issuer's account balances for the radial tidy tree 
            balances = []
            for ab in response_dict['data']['raw_data']['balances']:
                if 'asset_code' in ab:
                    # The get() method returns None if the attribute doesn't exist in the dictionary, instead of raising a KeyError.
                    # This allows the code to continue executing and append the account_balance dictionary to the balances list,
                    # even if any of the attributes are missing.
                    account_balance = {
                        'node_type': 'ASSET',
                        'asset_type': ab.get('asset_type'),
                        'asset_code': ab.get('asset_code'),
                        'asset_issuer': ab.get('asset_issuer'),
                        'balance': ab.get('balance'),
                        'limit': ab.get('limit'),
                        'is_authorized': ab.get('is_authorized'),
                        'is_authorized_to_maintain_liabilities': ab.get('is_authorized_to_maintain_liabilities'),
                        'is_clawback_enabled': ab.get('is_clawback_enabled')
                    }
                    balances.append(account_balance)

            return balances

        except Exception as e:
            sentry_sdk.capture_exception(e)

    def parse_account_flags(self):
        """
        Gets the account flags for the specified Stellar account.

        Not needed to make a request to the Horizon API.
        The JSON was stored already in horizon_accounts_doc_api_href
        Parse to get account flags

        :return: Dictionary of flags
        :rtype: dict
        """
        try:
            response_dict = self.datastax_response

            # building child nodes of an issuer's flags for the radial tidy tree 
            flags = []
            if 'flags' in response_dict['data']['raw_data']:
                account_flag = response_dict['data']['raw_data']['flags']  # Assign the flags dictionary to account_flag
                """
                "flags": {
                    "auth_required": false,
                    "auth_revocable": false,
                    "auth_immutable": false,
                    "auth_clawback_enabled": false
                },
                """
                flags.append(account_flag)

            return flags

        except Exception as e:
            sentry_sdk.capture_exception(e)
