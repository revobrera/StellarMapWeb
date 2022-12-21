import requests

class SiteChecker:
    """A class for checking the reachability of URLs."""

    def check_url(self, url: str) -> bool:
        """
        Check if the given URL is reachable.

        Parameters:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is reachable, False otherwise.
        """
        try:
            response = requests.get(url)
            return response.status_code == 200
        except requests.RequestException:
            return False

def check_all_urls(request):
    """
    Check the reachability of all URLs in the sites_dict.

    Returns:
        JsonResponse: A JSON response containing the reachability status of each URL.
    """
    sites_dict = {
        "stellar_github": "https://github.com/stellar",
        "stellar_org": "https://www.stellar.org",
        "stellar_doc": "https://stellar-documentation.netlify.app/api/",
    }

    results = {}
    checker = SiteChecker()
    for site, url in sites_dict.items():
        results[site] = checker.check_url(url)

    return JsonResponse(results)
