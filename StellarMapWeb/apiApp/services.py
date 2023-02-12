import json

import requests
import sentry_sdk
from apiApp.managers import ManagementCronHealthManager
from decouple import config
from django.conf import settings
from django.http import HttpRequest
from tenacity import retry, stop_after_attempt, wait_exponential

ASTRA_DB_ID = config('ASTRA_DB_ID')
ASTRA_DB_REGION = config('ASTRA_DB_REGION')
ASTRA_DB_KEYSPACE = config('ASTRA_DB_KEYSPACE')


class AstraDocument:
    def init(self):
        self.url = ''
        self.headers = {
            "X-Cassandra-Token": settings.ASTRA_DB_APPLICATION_TOKEN,
            "Content-Type": "application/json"
        }
        self.collections_name = "default"

    def set_collections_name(self, collections_name):
        """
        The name of the collections mapped to the attributes:

        horizon_accounts --> horizon_accounts_doc_api_href
        horizon_accounts_operations --> horizon_accounts_operations_doc_api_href
        horizon_accounts_effects --> horizon_accounts_effects_doc_api_href
        stellar_expert_explorer_account --> stellar_expert_explorer_account_doc_api_href

        The attributes name is mapped to the attributes found in StellarCreatorAccountLineage which is linked to the API endpoint

        horizon_accounts_doc_api_href --> "https://horizon.stellar.org/accounts/{stellar_account}"
        horizon_accounts_operations_doc_api_href --> "https://horizon.stellar.org/operations/{stellar_account}"
        horizon_accounts_effects_doc_api_href --> https://horizon.stellar.org/accounts/{stellar_account}/effects
        stellar_expert_explorer_account_doc_api_href --> https://api.stellar.expert/explorer/{network_name}/account/{stellar_account}
        
        """
        self.collections_name = collections_name
        self.url = f"https://{ASTRA_DB_ID}-{ASTRA_DB_REGION}.apps.astra.datastax.com/api/rest/v2/namespaces/{ASTRA_DB_KEYSPACE}/collections/{collections_name}"

    @retry(wait=wait_exponential(multiplier=1, max=7), stop=stop_after_attempt(7))
    def patch_document(self, stellar_account, network_name, external_url, raw_data, cron_name):
        data = {
            "stellar_account": stellar_account,
            "network_name": network_name,
            "external_url": external_url,
            "raw_data": raw_data
        }
        try:
            response = requests.patch(f"{self.url}/{self}", headers=self.headers, json=data)
            if response.status_code == 200:
                response_dict = json.loads(response)
                document_id = response_dict['documentId']
                document_href = f"{self.url}/{document_id}"
                return document_href
            else:
                raise Exception(f"Failed to patch document. Response: {response.content}")
        except Exception as e:
            sentry_sdk.capture_exception(e)

            request = HttpRequest()
            request.data = {
                'cron_name': f"{cron_name}",
                'status': f"UNHEALTHY_RATE_LIMITED_BY_CASSANDRA_DOCUMENT_API",
                'reason': f"{e}"
            }

            ManagementCronHealthManager.objects.create_cron_health(request)


