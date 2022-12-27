

class EnvHelpers:
    """A class for setting environment variables for different Stellar networks.
    
    This class allows users to set environment variables for either the public Stellar
    network or the testnet network.
    """

    def __init__(self):
        """Initialize the EnvHelpers class and set the environment variables for the testnet network."""
        self.debug = 'True'
        self.network = 'testnet'
        self.base_horizon = 'https://horizon-testnet.stellar.org'
        self.base_site = 'https://stellar.expert'
        self.base_se = 'https://api.stellar.expert'
        self._set_base_network()

    def set_testnet_network(self):
        """Set the environment variables for the testnet network."""
        self.debug = 'True'
        self.network = 'testnet'
        self.base_horizon = 'https://horizon-testnet.stellar.org'
        self._set_base_network()

    def set_public_network(self):
        """Set the environment variables for the public Stellar network."""
        self.debug = 'False'
        self.network = 'public'
        self.base_horizon = 'https://horizon.stellar.org'
        self._set_base_network()

    def _set_base_network(self):
        """Set the base environment variables for the current Stellar network."""
        self.base_site_network = f"{self.base_site}/explorer/{self.network}"
        self.base_site_network_account = f"{self.base_site_network}/account/"
        self.base_se_network = f"{self.base_se}/explorer/{self.network}"
        self.base_se_network_account = f"{self.base_se_network}/account/"
        self.base_se_network_dir = f"{self.base_se_network}/directory/"
        self.base_horizon_account = f"{self.base_horizon}/accounts/"

    def get_debug(self):
        return self.debug
    
    def get_network(self):
        return self.network
    
    def get_base_horizon(self):
        return self.base_horizon

    def get_base_site(self):
        return self.base_site

    def get_base_se(self):
        return self.base_se
    
    def get_base_site_network(self):
        return self.base_site_network
    
    def get_base_site_network_account(self):
        return self.base_site_network_account

    def get_base_se_network(self):
        return self.base_se_network

    def get_base_se_network_account(self):
        return self.base_se_network_account

    def get_base_se_network_dir(self):
        return self.base_se_network_dir

    def get_base_horizon_account(self):
        return self.base_horizon_account
