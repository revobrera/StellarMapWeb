import logging
import os
import time
from typing import Dict, Union

import requests

from .env import StellarNetwork
from .sm_validator import StellarMapValidatorHelpers


# Set up logging for module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LineageHelpers:
    def __init__(self, network, stellar_account_address):
        self.network = network
        self.stellar_account_address = stellar_account_address
        self.stellar_account_url = ''  # initialize empty attribute
        self.base_se_network_account_responses = [] # Set an empty list to store the issuer and JSON responses as tuples

        self.stellar_net = StellarNetwork(network)


    @property
    def get_stellar_account_url(self):
        """Get the URL for the Stellar account."""
        return self.stellar_account_url

    def set_stellar_account_url(self, api_name):
        """
        Set the URL for the Stellar account based on the specified API.
        
        Parameters:
            - api_name (str): The name of the API to use. Valid options are 'stellar_expert'
              and 'horizon'.
        
        Returns:
            None
        """

        if api_name == 'stellar_expert':
            self.stellar_account_url = f"{self.stellar_net.env_helpers.get_base_se_network_account()}{self.stellar_account_address}"
        elif api_name == 'horizon':
            self.stellar_account_url = f"{self.stellar_net.env_helpers.get_base_horizon_account()}{self.stellar_account_address}"
        else:
            raise ValueError(f"Invalid API name: {api_name}")


    def collect_account_issuers(self, initial_url):
        """
        Collects the issuers of an account from a series of URLs.
        
        Args:
            initial_url (str): The initial URL to be queried.
        
        Returns:
            list: A list of issuers for the account.
        """

        # Set the initial URL
        url = initial_url

        # Set a flag to indicate whether there are more URLs to be queried
        more_urls = True

        while more_urls:
            # Make a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the issuers from the JSON data
                issuer = response.json()["creator"]

                # Append the issuer and JSON response to the list as a tuple
                self.base_se_network_account_responses.append((issuer, response.json()))

                # Check if the "creator" data property exists and is not null
                if "creator" in response.json() and response.json()["creator"] is not None:
                    # Set the URL to the next URL
                    url = f"{self.stellar_net.env_helpers.get_base_se_network_account()}{response.json()['creator']}"
                else:
                    # There are no more URLs to be queried, so set the flag to False
                    more_urls = False

            else:
                logger.warning(f"Error: request to {url} returned status code {response.status_code}")
                # There was an error, so set the flag to False
                more_urls = False

            # Wait for a specified amount of time before making the next request for servers that rate limit requests
            time.sleep(1)

        # Return the collected issuers
        return self.base_se_network_account_responses


    def main(self):
        """
        Main method for the LineageHelpers class.
        
        This method retrieves and returns information about the upstream lineage of a Stellar account.
        
        Returns:
            dict: A dictionary with the relevant information about the Stellar account's upstream lineage, including the network and the Stellar account address.
        """

        # Retrieve the Stellar account address from the class attribute
        account_address = self.stellar_account_address

        # Check if the Stellar account address is valid using the Address class from the Stellar SDK
        try:
            sm_val = StellarMapValidatorHelpers()
            sm_val.validate_stellar_account_address(account_address)
        except:
            logger.warning("Invalid Stellar account address")
            return {"error": "Invalid Stellar account address"}

        # Set the Stellar account URL
        self.set_stellar_account_url("stellar_expert")

        # Collect issuers upstream
        self.collect_account_issuers(self.stellar_account_url)

        # Return the relevant information as a dictionary
        return {
            "network": self.network,
            "stellar_account_address": account_address,
            "upstream_lineage": self.base_se_network_account_responses,
        }

        