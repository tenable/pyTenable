from unittest import TestCase
from tenable.ad.license import  LicenseApi as api
from tenable.ad import APIKeyApi as apikey

class TestLicenseApi(TestCase):

    def test_api_license_get(self):
        """
            Get license singleton.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_license_get(api, x_api_key)
        #assert(thread.get("customerName") == "pytenable")
        #assert(thread.get("maxActiveUserCount") == 101)
        #assert(thread.get("expirationDateUTC") == "2022-07-26T00:00:00.000Z")
        #assert(thread.get("inAppEula") == False)
        #assert(thread.get("type") == "INTERNAL")
        #assert(thread.get("currentActiveUserCount") == None)
        #assert(thread.get("features") != None)

    def test_api_license_post(self):
        """
            Create new license singleton
        """
        x_api_key = apikey.get_api_key(self)
        body = {"currentActiveUserCount":5,"features":"active directory vulnerabilities"}
        thread = api.api_license_post(api,body, x_api_key)
        assert(thread != None)
        #if (thread.get("error") == None):
        #    assert(thread.status == 200)
        #    print ("license posted successfully")