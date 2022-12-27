import re

class StellarMapValidatorHelpers:
    """
    A helpers class for validating strings.
    
    This class contains methods for validating the formatting of various types of
    strings, such as email addresses, URLs, and Stellar account addresses.
    """
    
    @staticmethod
    def validate_stellar_account_address(address):
        """
        Validate the formatting of a Stellar account address.
        
        This method uses a regular expression to verify that the address has the correct
        format, which is a string of 56 characters starting with "G".
        
        Parameters:
            - address (str): The Stellar account address to validate.
        
        Returns:
            bool: True if the address is valid, False otherwise.
        """
        # Compile the regular expression pattern
        pattern = re.compile(r'^G[A-Za-z0-9]{55}$')
        # Match the address against the pattern
        match = pattern.match(address)
        # Return True if the address is valid, False otherwise
        return bool(match)
