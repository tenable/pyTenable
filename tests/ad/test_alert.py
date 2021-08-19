
from unittest import TestCase
from tenable.ad import AlertApi as api
from tenable.ad import APIKeyApi as apikey


class TestAlertApi(TestCase):
    def test_api_alerts_id_get(self):
        """
            Get alert instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_alerts_id_get(api,x_api_key,1)
        assert(thread != None)

    def test_api_alerts_id_patch(self):
        """
            Update alert instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "archived": True,
            "read": True
        }
        thread = api.api_alerts_id_patch(api,body,x_api_key,1)
        assert(thread != None)

    def test_api_profiles_profile_id_alerts_get(self):
        """
            Retrieve all alert instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_profiles_profile_id_alerts_get(api,x_api_key,1)
        assert(thread != None)

    def test_api_profiles_profile_id_alerts_patch(self):
        """
            Update alerts for one profile
        """
        x_api_key = apikey.get_api_key(self)
        body = {
         "archived": True,
         "read": False
        }
        thread = api.api_profiles_profile_id_alerts_patch(api,x_api_key,1,1)
        assert(thread != None)

