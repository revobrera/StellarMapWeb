import os

class EnvHelpers:
    """A class for setting environment variables for different Stellar networks.
    
    This class allows users to set environment variables for either the public Stellar
    network or the testnet network.
    """

    def __init__(self):
        """Initialize the EnvHelpers class and set the environment variables for the testnet network."""
        self.set_testnet_network()

    def set_testnet_network(self):
        """Set the environment variables for the testnet network."""
        os.environ['DEBUG'] = 'True'
        os.environ['NETWORK'] = 'testnet'
        os.environ['BASE_HORIZON'] = 'https://horizon-testnet.stellar.org'
        self._set_base_network()

    def set_public_network(self):
        """Set the environment variables for the public Stellar network."""
        os.environ['DEBUG'] = 'False'
        os.environ['NETWORK'] = 'public'
        os.environ['BASE_HORIZON'] = 'https://horizon.stellar.org'
        self._set_base_network()

    def _set_base_network(self):
        """Set the base environment variables for the current Stellar network."""
        # stellar.expert site
        os.environ['BASE_SITE'] = 'https://stellar.expert'
        os.environ['BASE_SITE_NETWORK'] = f"{os.getenv('BASE_SITE')}/explorer/{os.getenv('NETWORK')}"
        os.environ['BASE_SITE_NETWORK_ACCOUNT'] = f"{os.getenv('BASE_SITE_NETWORK')}/account/"

        # stellar.expert api
        os.environ['BASE_SE'] = 'https://api.stellar.expert'
        os.environ['BASE_SE_NETWORK'] = f"{os.getenv('BASE_SE')}/explorer/{os.getenv('NETWORK')}"
        os.environ['BASE_SE_NETWORK_ACCOUNT'] = f"{os.getenv('BASE_SE_NETWORK')}/account/"
        os.environ['BASE_SE_NETWORK_DIR'] = f"{os.getenv('BASE_SE_NETWORK')}/directory/"

        # horizon
        os.environ['BASE_HORIZON_ACCOUNT'] = f"{os.getenv('BASE_HORIZON')}/accounts/"
