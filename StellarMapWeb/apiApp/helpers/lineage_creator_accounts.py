import os

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
    def stellar_account_url(self):
        """Get the URL for the Stellar account."""
        return self._stellar_account_url

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
            self._stellar_account_url = f"{os.getenv('BASE_SE_NETWORK_ACCOUNT')}{self.stellar_account_address}"
        elif api_name == 'horizon':
            self._stellar_account_url = f"{os.getenv('BASE_HORIZON_ACCOUNT')}{self.stellar_account_address}"
        else:
            raise ValueError(f"Invalid API name: {api_name}")


    def main(self):
        """
        Main method for the LineageHelpers class.
        
        This method calls all other methods in the class as needed.
        
        Returns:
            dict: A dictionary with the relevant information about the Stellar account's
            upstream lineage.
        """
        upstream_lineage = self.get_upstream_lineage()

        return {
            'network': self.network,
            'stellar_account_address': self.stellar_account_address,
            'upstream_lineage': upstream_lineage,
        }