from unittest import TestCase
from tenable.ad.checker import CheckerApi as api
from tenable.ad import APIKeyApi as apikey


class TestCheckerApi(TestCase):

    def test_api_checkers_get(self):
        """
            Retrieve all checker instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_checkers_get(api, x_api_key)
        count = len(thread)
        if (count != 0):
            assert(len(thread) != 0)
            for i in range(count):
                assert(thread[i]["id"] != 0)
                assert(thread[i]["name"] != None)
                assert(thread[i]["categoryId"] != None)

    def test_api_checkers_id_get(self):
        """
            Get checker instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_checkers_id_get(api, x_api_key, 1)
        if (thread != ''):
            if (thread.get("error") == None):
                assert(thread[0]["id"] != 0)
                assert(thread[0]["name"] != None)
                assert(thread[0]["categoryId"] != None)
