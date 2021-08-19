from unittest import TestCase
from tenable.ad.reason import  ReasonApi as api
from tenable.ad import APIKeyApi as apikey


class TestReasonApi(TestCase):
    def test_api_reasons_get(self):
        """
            Retrieve all reason instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_reasons_get(api,x_api_key)
        count = len(thread)
        if (len(thread) != 0):
            assert(len(thread) != 0)
            for i in range(count):
                assert(thread[i]["id"] != 0)
                assert(thread[i]["codename"] != "")
                assert(thread[i]["name"] != "")
                assert(thread[i]["description"] != "")

    def test_api_reasons_id_get(self):
        """
            Get reason instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_reasons_id_get(api,x_api_key,51)
        count = len(thread)
        if (count != 0):
            assert(len(thread) != 0)
            assert(thread['id'] == 51)
            assert(thread['codename'] == 'R-AAD-SSO-PASSWORD')
            assert(thread['name'] == 'Old AAD SSO account password')
            assert(thread["description"] == 'This account could be used to impersonate users for Azure resources and should be protected accordingly.')