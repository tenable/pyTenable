import os
from pprint import pprint
from unittest import TestCase
from tenable.ad.configuration import Configuration as config

class TestConfiguration(TestCase):


    def test_get_basic_auth_token(self):
        """
            Gets HTTP basic authentication header (string).
        """
        token = config.get_basic_auth_token(config)
        assert(token != None)

    def test_get_api_key_with_prefix(self):
        """
            Gets API key (with prefix if set).
        """
        identifier = os.environ.get("TenableADAPIKey")
        key = config.get_api_key_with_prefix(config, identifier)
        assert(key != None)

    def test__init__(self):
        """
            Constructor
        """
        config.__init__(self)
        assert(config.debug != None)


    def test_debug(self):
        assert(config.debug != True)


    def test_to_debug_report(self):
        debug_report = config.to_debug_report(self)
        pprint(debug_report)
        assert(debug_report != None)
