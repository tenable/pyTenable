from pprint import pprint
from unittest import TestCase
from tenable.ad.about import AboutApi
from tenable.ad import APIKeyApi as apikey

class TestAboutApi(TestCase):

    def test_api_about_get(api):
        """
            This is AboutAPI to get general information on Eridanis
        """
        x_api_key = apikey.get_api_key(apikey)
        response = AboutApi.__init__(api)
        response = AboutApi.api_about_get_with_http_info(api, x_api_key)
        pprint(response[0])
        assert(response[0] != None)

