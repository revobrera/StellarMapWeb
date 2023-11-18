import re
import sentry_sdk

from apiApp.helpers.sm_cron import StellarMapCronHelpers

class StellarMapParsingUtilityHelpers:
    """
    A helpers class for parsing strings.
    
    This class contains methods for parsing the formatting of various types of
    strings, such as email addresses, URLs, and Stellar account addresses.
    """
    
    @staticmethod
    def get_documentid_from_url_address(url_address):

        # Compile the regular expression pattern
        pattern = r'[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}'
        
        # Match the documentid against the pattern
        result = re.findall(pattern, url_address, re.X)
        
        document_id = result[1]
        return document_id

class StellarMapUtilityHelpers:
    """
    A helpers class for utilities
    """

    def on_retry_failure(self, retry_state, cron_name):
        # This function will be called every time a retry fails
        # Log the exception using Sentry SDK
        sentry_sdk.capture_exception(retry_state.outcome.exception())
        # Call set_crons_unhealthy method of StellarMapCronHelpers class
        cron_helpers = StellarMapCronHelpers(cron_name=cron_name)
        cron_helpers.set_crons_unhealthy()