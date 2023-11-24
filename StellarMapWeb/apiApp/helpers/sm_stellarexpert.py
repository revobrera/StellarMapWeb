import json

import requests
import sentry_sdk
from apiApp.helpers.env import EnvHelpers
from apiApp.helpers.sm_horizon import StellarMapHorizonAPIHelpers
from apiApp.helpers.sm_utils import StellarMapUtilityHelpers
from tenacity import retry, stop_after_attempt, wait_random_exponential


class StellarMapStellarExpertAPIHelpers(StellarMapHorizonAPIHelpers):
    """
    This class provides helper functions to interact with the Stellar Expert API provided by Stellar Expert.

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

    def __init__(self, lin_queryset):
        self.headers = {
            "Content-Type": "application/json"
        }
        self.lin_queryset = lin_queryset # creator account lineage record

        # set environment
        self.env_helpers = EnvHelpers()
        network_name = lin_queryset.network_name
        if network_name == 'public':
            self.env_helpers.set_public_network()
        else:
            self.env_helpers.set_testnet_network()

    def on_retry_failure(self, retry_state):
        sm_util = StellarMapUtilityHelpers()
        sm_util.on_retry_failure(retry_state, self.cron_name)

    @retry(wait=wait_random_exponential(multiplier=1, max=71),
       stop=stop_after_attempt(7),
       retry_error_callback=on_retry_failure)
    def get_se_asset_list(self):
        """
        Retrieves the asset list from the Stellar Expert API for a specific account.

        Returns:
            The asset list in JSON format.

        Raises:
            Exception: If the GET request to the API fails.

        Example URI: 
        >>> https://api.stellar.expert/explorer/public/asset?search=GDZZEJPAY2M4BU5EZ3H2V3HPNYHQUQLUUHKR4OQAM2RM453FRDZUOZJF

        Example JSON:
        >>> {
            "_links": {
                "self": "/explorer/public/asset?order=desc&limit=50&cursor=0",
                "prev": "/explorer/public/asset?order=asc&limit=50&cursor=1",
                "next": "/explorer/public/asset?order=desc&limit=50&cursor=50"
            },
            "_embedded": {
                "records": [
                {
                    "asset": "ZBZ-GDZZEJPAY2M4BU5EZ3H2V3HPNYHQUQLUUHKR4OQAM2RM453FRDZUOZJF-1",
                    "supply": 404553067174374000000,
                    "traded_amount": 630946799020173800000,
                    "payments_amount": 1.6454491800032636e+21,
                    "created": 1633466666,
                    "trustlines": [2865, 2865, 2720],
                    "payments": 576,
                    "domain": "gov.stellarbonds.exchange",
                    "rating": {
                    "age": 0,
                    "trades": 0,
                    "payments": 0,
                    "trustlines": 0,
                    "volume7d": 0,
                    "interop": 0,
                    "liquidity": 0,
                    "average": 0
                    },
                    "price7d": [[1699401600, 3.55133e-11], [1699488000, 4.7751942999999994e-11], [1699574400, 4.088812875e-11], [1699660800, 5.157111333333333e-11], [1699747200, 3.884246e-11], [1699833600, 4.0516755e-11], [1699920000, 4.273100777777778e-11], [1700006400, 4.660724e-11]],
                    "volume7d": 202902378,
                    "tomlInfo": {
                    "code": "ZBZ",
                    "issuer": "GDZZEJPAY2M4BU5EZ3H2V3HPNYHQUQLUUHKR4OQAM2RM453FRDZUOZJF",
                    "name": "U.S. Treasury Bond 0.75%",
                    "image": "https://ipfs.io/ipfs/bafkreihj5xo3ypmh6k5wa5ahmfoq7udjupgwmrxaxcsrtyenavgxwx5ijq",
                    "status": "live",
                    "anchorAssetType": "bond",
                    "anchorAsset": "US Treasury"
                    },
                    "paging_token": 1
                },
                ...
                ]
            }
        }
        """

        try:
            base_se_network = self.env_helpers.get_base_se_network()

            # Make a GET request to the API to retrieve the asset list
            response = requests.get(f"{base_se_network}/asset?search={self.lin_queryset.stellar_account}", headers=self.headers)
            
            if response.status_code == 200:
                # If the response is successful (status code 200), return the response data in JSON format
                return response.json()
            else:
                # If the response is not successful, raise an exception with a descriptive error message
                raise Exception(f"Failed to GET SE asset list. Response: {response.content}")
        except Exception as e:
            # Capture any exception that occurs during the execution of the function and send it to Sentry for error tracking
            sentry_sdk.capture_exception(e)

    @retry(wait=wait_random_exponential(multiplier=1, max=71),
           stop=stop_after_attempt(7),
           retry_error_callback=on_retry_failure)
    def get_se_asset_rating(self, asset_code, asset_type):
        """
        Example URI:
        >>> https://api.stellar.expert/explorer/{network}/asset/{asset_code}-{asset_issuer}-{asset_type}/rating

        Example JSON: 
        >>> {
            "asset": "ZBM-GDZZEJPAY2M4BU5EZ3H2V3HPNYHQUQLUUHKR4OQAM2RM453FRDZUOZJF-1",
            "rating": {
                "age": 0,
                "trades": 0,
                "payments": 0,
                "trustlines": 0,
                "volume7d": 0,
                "interop": 0,
                "liquidity": 0,
                "average": 0
            }
        }
        """ 

        try:
            base_se_network = self.env_helpers.get_base_se_network()
            # Make a GET request to the API to retrieve the asset rating
            response = requests.get(f"{base_se_network}/asset/{asset_code}-{self.lin_queryset.stellar_account}-{asset_type}/rating", headers=self.headers)
            
            if response.status_code == 200:
                # If the response is successful (status code 200), return the response data in JSON format
                return response.json()
            else:
                # If the response is not successful, raise an exception with a descriptive error message
                raise Exception(f"Failed to GET SE asset rating. Response: {response.content}")
        except Exception as e:
            # Capture any exception that occurs during the execution of the function and send it to Sentry for error tracking
            sentry_sdk.capture_exception(e)

    @retry(wait=wait_random_exponential(multiplier=1, max=71),
           stop=stop_after_attempt(7),
           retry_error_callback=on_retry_failure)
    def get_se_blocked_domain(self, asset_domain):
        """
        Example URI:
        >>> https://api.stellar.expert/explorer/directory/blocked-domains/{domain}

        Example JSON (domain specific):
        >>> {
            "domain": "stellar.org.am",
            "blocked": true
        }

        Example URI:
        >>> https://api.stellar.expert/explorer/directory/blocked-domains/

        Example JSON:
        >>> {
            "_links": {
                "self": {
                "href": "/explorer/directory/blocked-domains/?order=asc&limit=1000"
                },
                "prev": {
                "href": "/explorer/directory/blocked-domains/?order=desc&limit=1000&cursor=afreum.co"
                },
                "next": {
                "href": "/explorer/directory/blocked-domains/?order=asc&limit=1000&cursor=xlmstar.net"
                }
            },
            "_embedded": {
                "records": [
                {
                    "domain": "afreum.co",
                    "paging_token": "afreum.co"
                },
                {
                    "domain": "agrogenesis.in",
                    "paging_token": "agrogenesis.in"
                },
                {
                    "domain": "airdrop-info.vwv.pw",
                    "paging_token": "airdrop-info.vwv.pw"
                },
                {
                    "domain": "airdrop-stellar.org",
                    "paging_token": "airdrop-stellar.org"
                },
                {
                    "domain": "amm.xmint.io",
                    "paging_token": "amm.xmint.io"
                },
                {
                    "domain": "app.xmint.io",
                    "paging_token": "app.xmint.io"
                },
                ...
                ]
            }
        }
        """

        try:
            base_se_blocked_domains = self.env_helpers.base_se_blocked_domains()
            
            # Make a GET request to the API to retrieve blocked domains
            if asset_domain is None:
                # Get list of all blocked domains
                response = requests.get(f"{base_se_blocked_domains}", headers=self.headers)
            else:
                # Get domain specific blocked domain
                response = requests.get(f"{base_se_blocked_domains}{asset_domain}", headers=self.headers)
            
            if response.status_code == 200:
                # If the response is successful (status code 200), return the response data in JSON format
                return response.json()
            else:
                # If the response is not successful, raise an exception with a descriptive error message
                raise Exception(f"Failed to GET SE asset rating. Response: {response.content}")
        except Exception as e:
            # Capture any exception that occurs during the execution of the function and send it to Sentry for error tracking
            sentry_sdk.capture_exception(e)

    @retry(wait=wait_random_exponential(multiplier=1, max=71),
           stop=stop_after_attempt(7),
           retry_error_callback=on_retry_failure)
    def get_se_account_directory(self):
        """
        Example URI:
        >>> https://api.stellar.expert/explorer/public/directory/{asset_issuer}

        Example JSON: 
        >>> {
            "address": "GDUKMGUGDZQK6YHYA5Z6AY2G4XDSZPSZ3SW5UN3ARVMO6QSRDWP5YLEX",
            "name": "AnchorUSD",
            "domain": "www.anchorusd.com",
            "tags": [
                "anchor",
                "issuer"
            ]
        }
        """ 

        try:
            base_se_network_dir = self.env_helpers.get_base_se_network_dir()
            # Make a GET request to the API to retrieve the SE account directory
            response = requests.get(f"{base_se_network_dir}/{self.lin_queryset.stellar_account}", headers=self.headers)
            
            if response.status_code == 200:
                # If the response is successful (status code 200), return the response data in JSON format
                return response.json()
            else:
                # If the response is not successful, raise an exception with a descriptive error message
                raise Exception(f"Failed to GET SE account directory. Response: {response.content}")
        except Exception as e:
            # Capture any exception that occurs during the execution of the function and send it to Sentry for error tracking
            sentry_sdk.capture_exception(e)


class StellarMapStellarExpertAPIParserHelpers:
    """ 
    Note: This class parses the Stellar Expert JSON dataset that is embedded into a custom
          StellarMap JSON formatted.
    """
    def __init__(self, lin_queryset):
        self.lin_queryset = lin_queryset

    def parse_asset_code_issuer_type(self):

        # parse the json data
        parsed_data = json.loads(self.lin_queryset.horizon_accounts_assets_doc_api_href)

        asset_dict = {}
        # iterate over each item data
        for item in parsed_data:
            if item["asset_issuer"] == self.lin_queryset.stellar_account:
                asset_dict['asset_code'] = item["asset_code"]
                asset_dict["asset_issuer"] = item["asset_issuer"]
                asset_dict["asset_type"] = item["asset_type"]

        return asset_dict