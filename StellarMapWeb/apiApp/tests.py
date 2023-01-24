import unittest

from django.test import TestCase
from django.urls import reverse

from .helpers.env import EnvHelpers, StellarNetwork
from .helpers.sm_validator import StellarMapValidatorHelpers


class SwaggerUIViewTestCase(TestCase):

    def test_swagger_ui(self):
        # Issue a GET request to the swagger_ui view
        response = self.client.get(reverse('apiApp:swagger-ui'))

        # Check that the response is 200 (OK)
        self.assertEqual(response.status_code, 200)

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


class TestStellarNetwork(unittest.TestCase):

    def test_init(self):
        # Test the initialization of the StellarNetwork class with the 'testnet' network
        network = StellarNetwork('testnet')
        self.assertEqual(network.env_helpers.get_network(), 'testnet')
        self.assertEqual(network.env_helpers.get_debug(), 'True')
        self.assertEqual(network.env_helpers.get_base_horizon(), 'https://horizon-testnet.stellar.org')
        
        # Test the initialization of the StellarNetwork class with the 'public' network
        network = StellarNetwork('public')
        self.assertEqual(network.env_helpers.get_network(), 'public')
        self.assertEqual(network.env_helpers.get_debug(), 'False')
        self.assertEqual(network.env_helpers.get_base_horizon(), 'https://horizon.stellar.org')
        
        # Test the initialization of the StellarNetwork class with an invalid network
        with self.assertRaises(ValueError):
            network = StellarNetwork('invalid')


class TestEnvHelpers(unittest.TestCase):

    def test_set_testnet_network(self):
        env_helpers = EnvHelpers()
        env_helpers.set_testnet_network()
        self.assertEqual(env_helpers.get_network(), 'testnet')
        self.assertEqual(env_helpers.get_debug(), 'True')
        self.assertEqual(env_helpers.get_base_horizon(), 'https://horizon-testnet.stellar.org')
        self.assertEqual(env_helpers.get_base_site_network(), 'https://stellar.expert/explorer/testnet')
        self.assertEqual(env_helpers.get_base_site_network_account(), 'https://stellar.expert/explorer/testnet/account/')
        self.assertEqual(env_helpers.get_base_se_network(), 'https://api.stellar.expert/explorer/testnet')
        self.assertEqual(env_helpers.get_base_se_network_account(), 'https://api.stellar.expert/explorer/testnet/account/')
        self.assertEqual(env_helpers.get_base_se_network_dir(), 'https://api.stellar.expert/explorer/testnet/directory/')
        self.assertEqual(env_helpers.get_base_horizon_account(), 'https://horizon-testnet.stellar.org/accounts/')

    def test_set_public_network(self):
        env_helpers = EnvHelpers()
        env_helpers.set_public_network()
        self.assertEqual(env_helpers.get_network(), 'public')
        self.assertEqual(env_helpers.get_debug(), 'False')
        self.assertEqual(env_helpers.get_base_horizon(), 'https://horizon.stellar.org')
        self.assertEqual(env_helpers.get_base_site_network(), 'https://stellar.expert/explorer/public')
        self.assertEqual(env_helpers.get_base_site_network_account(), 'https://stellar.expert/explorer/public/account/')
        self.assertEqual(env_helpers.get_base_se_network(), 'https://api.stellar.expert/explorer/public')
        self.assertEqual(env_helpers.get_base_se_network_account(), 'https://api.stellar.expert/explorer/public/account/')
        self.assertEqual(env_helpers.get_base_se_network_dir(), 'https://api.stellar.expert/explorer/public/directory/')
        self.assertEqual(env_helpers.get_base_horizon_account(), 'https://horizon.stellar.org/accounts/')


class TestStellarMapValidatorHelpers(unittest.TestCase):

    def test_validate_stellar_account_address(self):
        # Test a valid Stellar account address
        self.assertTrue(StellarMapValidatorHelpers.validate_stellar_account_address('GA2C5RFPE6GCKMY3US5PAB6UZLKIGSPIUKSLRB6Q723BM2OARMDUYEJ5'))
        
        # Test an invalid Stellar account address with the wrong length
        self.assertFalse(StellarMapValidatorHelpers.validate_stellar_account_address('GA2C5RFPE6GCKMY3US5PAB6UZLKIGSPIUKSLRB6Q723BM2OARMDUYEJ56789'))
        
        # Test an invalid Stellar account address with the wrong starting character
        self.assertFalse(StellarMapValidatorHelpers.validate_stellar_account_address('HA2C5RFPE6GCKMY3US5PAB6UZLKIGSPIUKSLRB6Q723BM2OARMDUYEJ5'))
        
        # Test an invalid Stellar account address with invalid characters
        self.assertFalse(StellarMapValidatorHelpers.validate_stellar_account_address('GA2C5RFPE6GCKMY3US5PAB6UZLKIGSPIUKSLRB6Q723BM2OARMDUYEJ$'))
