from pprint import pprint
from unittest import TestCase
from tenable.ad.category import CategoryApi as api
from tenable.ad import APIKeyApi as apikey

class TestCategoryApi(TestCase):

    def test_api_categories_get(self):
        """
            Retrieve all category instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_categories_get(api, x_api_key)
        count = len(thread)
        if (count != 0):
            assert(len(thread) != 0)
            for i in range(count):
                assert(thread[i]["id"] != 0)
                assert(thread[i]["name"] != None)

    def test_api_categories_id_get(self):
        """
            Get category instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_categories_id_get(api, x_api_key,1)
        pprint(thread)
        if (thread != ''):
            if (thread.get("error") == None):
                print(thread.data)
                print(thread.status)
                assert(thread.get("id") != 0)
                assert(thread.get("name") != None)
