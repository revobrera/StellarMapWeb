from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .helpers import SiteChecker


@api_view(['GET'])
def check_url(request, url):
    checker = SiteChecker()
    result = checker.check_url(url)
    return Response({"reachable": result})

@api_view(['GET'])
def check_all_urls(request):
    sites_dict = {
        "stellar_github": "https://github.com/stellar",
        "stellar_org": "https://www.stellar.org",
        "stellar_doc": "https://stellar-documentation.netlify.app/api/",
    }

    results = {}
    checker = SiteChecker()
    for site, url in sites_dict.items():
        results[site] = checker.check_url(url)

    return Response(results)

