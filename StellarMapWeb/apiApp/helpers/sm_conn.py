import asyncio
import json

import aiohttp
import pandas as pd
import requests
import sentry_sdk
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from decouple import config
from django.conf import settings
from django.http import HttpResponse

APP_PATH = config('APP_PATH')
CASSANDRA_DB_NAME = config('CASSANDRA_DB_NAME')
CASSANDRA_HOST = config('CASSANDRA_HOST')
CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')


class SiteChecker:
    """A class for checking the reachability of URLs."""

    def check_url(self, url: str) -> bool:
        """
        Check if the given URL is reachable.

        Parameters:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is reachable, False otherwise.
        """
        try:
            response = requests.get(url)
            return True
        except requests.RequestException:
            return False

    def check_all_urls(self):
        """
        Check the reachability of all URLs in the sites_dict.

        Returns:
            HttpResponse: An HTTP response containing the reachability status of each URL in JSON format.
        """
        sites_dict = {
            "stellar_github": "https://github.com/stellar",
            "stellar_org": "https://www.stellar.org",
            "stellar_doc": "https://stellar-documentation.netlify.app/api/",
            "stellarmap": "http://revobrera.pythonanywhere.com/search/",
        }

        results = {}
        checker = SiteChecker()
        for site, url in sites_dict.items():
            results[site] = checker.check_url(url)


        # Convert the data dictionary to a JSON response
        data_json = json.dumps(results)

        # Return the data as a JSON response
        return HttpResponse(data_json, content_type='application/json')


class StellarMapHTTPHelpers:
    """
    A class to handle external HTTP requests for the StellarMap application.
    """

    def __init__(self):
        self.url = None

    def add_url(self, url):
        """
        Add the full URL for the API endpoint.
        :param url: str
        """
        self.url = url

    def handle_response(self, response):
        """
        Handle the response from the API.
        :param response: requests.Response
        :return: dict
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise ValueError(f'HTTP Error: {e}')
        except ValueError as e:
            raise ValueError(f'Invalid JSON: {e}')

    def get(self):
        """
        Perform a GET request.
        :return: dict
        """
        url = f"{self.url}"
        try:
            response = requests.get(url)
            return self.handle_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Error: {e}')

    
class AsyncStellarMapHTTPHelpers:
    """
    A class to handle external HTTP requests for the StellarMap application using asyncio.
    """

    def __init__(self):
        self.url = None

    async def add_url(self, url: str) -> None:
        """
        Add the full URL for the API endpoint.
        :param url: str
        """
        self.url = url

    async def handle_response(self, response) -> dict:
        """
        Handle the response from the API.
        :param response: aiohttp.ClientResponse
        :return: dict
        """
        try:
            response.raise_for_status()
            json_response = await response.json()
            return json_response
        except aiohttp.ClientError as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'HTTP Error: {e}')

    async def get(self) -> dict:
        """
        Perform a GET request.
        :return: dict
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    return await self.handle_response(response)
        except asyncio.TimeoutError as e:
            sentry_sdk.capture_exception(e)
            raise ValueError(f'Error: {e}')
            

class CassandraConnectionsHelpers:
    def __init__(self):
        self.cloud_config = {
            'secure_connect_bundle': f"{APP_PATH}/secure-connect-stellarmapdb.zip"
        }

        self.auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
        self.cluster = Cluster(cloud=self.cloud_config, auth_provider=self.auth_provider, protocol_version=4)
        self.session = self.cluster.connect(CASSANDRA_DB_NAME)
        self.cql_query = None

    def set_cql_query(self, cql):
        self.cql_query = cql

    def execute_cql(self):
        try:
            rows = self.session.execute(self.cql_query)
            return rows
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise e

    def close_connection(self):
        self.session.cluster.shutdown()
        self.session.shutdown()