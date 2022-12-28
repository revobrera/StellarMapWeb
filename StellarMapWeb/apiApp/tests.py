from django.test import TestCase
from django.urls import reverse

class SwaggerUIViewTestCase(TestCase):
    def test_swagger_ui(self):
        # Issue a GET request to the swagger_ui view
        response = self.client.get(reverse('apiApp:swagger-ui'))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)

class CheckUrlViewTestCase(TestCase):
    def test_check_url(self):
        # Issue a GET request to the check_url view
        response = self.client.get(reverse('apiApp:check_url', kwargs={'url': 'http://revobrera.pythonanywhere.com/search/'}))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected data
        self.assertEqual(response.data, {'url': 'http://revobrera.pythonanywhere.com/search/', 'status': 'OK'})

class CheckAllUrlsViewTestCase(TestCase):
    def test_check_all_urls(self):
        # Issue a GET request to the check_all_urls view
        response = self.client.get(reverse('apiApp:check_all_urls'))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)

class SetNetworkViewTestCase(TestCase):
    def test_set_network(self):
        # Issue a GET request to the set_network view
        response = self.client.get(reverse('apiApp:set_network', kwargs={'network': 'testnet'}))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)

class LineageStellarAccountViewTestCase(TestCase):
    def test_lineage_stellar_account(self):
        # Issue a GET request to the lineage_stellar_account view
        response = self.client.get(reverse('apiApp:lineage_stellar_account', kwargs={'network': 'testnet', 'stellar_account_address': 'GBRPYHIL2CI3FNQ4BXLFMNDLFJUNPU2HY3ZMFSHONUCEOASW7QC7OX2H'}))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)
