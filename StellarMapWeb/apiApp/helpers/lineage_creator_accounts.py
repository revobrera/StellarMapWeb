import os
import requests
import logging

from typing import Union
from typing import Dict
from stellar_sdk import Address


class LineageHelpers:
    def __init__(self, network, stellar_account_address):
        self.network = network
        self.stellar_account_address = stellar_account_address
        self.stellar_account_url = ''  # initialize empty attribute

    def get_upstream_lineage(self):
        """
        Retrieve the upstream lineage of a Stellar account.
        
        This method will recursively crawl the creator accounts of the Stellar account
        specified in the object's `stellar_account_address` attribute to build a list of
        its upstream lineage. The resulting list will be returned.
        
        Returns:
            list: A list of the upstream accounts in the lineage of the Stellar account,
            starting with the immediate creator and ending with the root account.
        """
        # Perform some action here to retrieve the upstream lineage of the Stellar account,
        # such as querying a database or making an API call

        return ['account1', 'account2', 'account3']  # example upstream lineage


    @property
    def get_stellar_account_url(self):
        """Get the URL for the Stellar account."""
        return self.stellar_account_url

    @stellar_account_url.setter
    def stellar_account_url(self, api_name):
        """
        Set the URL for the Stellar account based on the specified API.
        
        Parameters:
            - api_name (str): The name of the API to use. Valid options are 'stellar_expert'
              and 'horizon'.
        
        Returns:
            None
        """
        if api_name == 'stellar_expert':
            self.stellar_account_url = f"{os.getenv('BASE_SE_NETWORK_ACCOUNT')}{self.stellar_account_address}"
        elif api_name == 'horizon':
            self.stellar_account_url = f"{os.getenv('BASE_HORIZON_ACCOUNT')}{self.stellar_account_address}"
        else:
            raise ValueError(f"Invalid API name: {api_name}")


    def make_api_request(self, http_url: str) -> Union[Dict, None]:
        """
        Makes an API request to the specified URL and returns the JSON response.

        Parameters:
            http_url (str): The URL to make the API request to.

        Returns:
            Union[Dict, None]: The JSON response as a dictionary, or None if the request failed.
        """
        try:
            response = requests.get(http_url)
            if response.status_code == 200:
                return response.json()
            else:
                logging.warning("API request returned status code %d", response.status_code)
                return None
        except Exception as e:
            logging.error("Error fetching Stellar account information: %s", e)
            return None



    def main(self):
        """
        Main method for the LineageHelpers class.
        
        This method retrieves and returns information about the upstream lineage of a Stellar account.
        
        Returns:
            dict: A dictionary with the relevant information about the Stellar account's upstream lineage, including the network and the Stellar account address.
        """
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Retrieve the Stellar account address from the class attribute
        account_address = self.stellar_account_address

        # Check if the Stellar account address is valid using the Address class from the Stellar SDK
        try:
            address = Address(account_address)
        except:
            logger.warning("Invalid Stellar account address")
            return {"error": "Invalid Stellar account address"}

        # Set the Stellar account URL
        self.stellar_account_url("stellar_expert")

        # Make an API request
        account_response = self.make_api_request(self.get_stellar_account_url())

        # Get the upstream lineage
        upstream_lineage = self.get_upstream_lineage()

        # Return the relevant information as a dictionary
        return {
            "network": self.network,
            "stellar_account_address": account_address,
            "upstream_lineage": upstream_lineage,
        }

        