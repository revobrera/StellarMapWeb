
class StellarNetwork:
    """A class for working with Stellar networks.
    
    This class allows users to set the network for a Stellar account and retrieve
    the network details.
    """

    def __init__(self, network: str):
        """Initialize the StellarNetwork class and set the network for the account.
        
        Args:
            network: The network to use for the Stellar account. Valid values are
                'testnet' and 'public'.
        """
        self.env_helpers = EnvHelpers()
        if network == 'testnet':
            self.env_helpers.set_testnet_network()
        elif network == 'public':
            self.env_helpers.set_public_network()
        else:
            raise ValueError(f"Invalid network name: {network}")


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
        self.base_se_blocked_domains = f"{self.base_se}/explorer/directory/blocked-domains/"
        self.base_se_network = f"{self.base_se}/explorer/{self.network}"
        self.base_se_network_account = f"{self.base_se_network}/account/"
        self.base_se_network_dir = f"{self.base_se_network}/directory/"
        self.base_horizon_account = f"{self.base_horizon}/accounts/"
        self.base_horizon_operations = f"{self.base_horizon}/operations/"
        self.base_horizon_effects = f"{self.base_horizon}/effects/"

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
    
    def get_base_se_blocked_domains(self):
        return self.base_se_blocked_domains
    
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

    def get_base_horizon_operations(self):
        return self.base_horizon_operations

    def get_base_horizon_effects(self):
        return self.base_horizon_effects
