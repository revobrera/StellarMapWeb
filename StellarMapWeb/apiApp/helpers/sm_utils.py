import re

class StellarMapParsingUtilityHelpers:
    """
    A helpers class for parsing strings.
    
    This class contains methods for parsing the formatting of various types of
    strings, such as email addresses, URLs, and Stellar account addresses.
    """
    
    @staticmethod
    def get_documentid_from_url_address(url_address):

        # Compile the regular expression pattern
        pattern = re.compile(r'[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}')
        
        # Match the documentid against the pattern
        res = pattern.match(url_address)
        
        document_id = res.group(1)
        return document_id
