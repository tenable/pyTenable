from unittest import TestCase
from tenable.ad import ADObjectApi as api
from tenable.ad import APIKeyApi as apikey

class TestADObjectApi(TestCase):

    def test_api_infrastructure_id_directory_id_ad_objects_id_get(self):
        """
            Get the AD Object instance by id
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directory_id_ad_objects_id_get(api, x_api_key,1,1,1)
        assert(thread != None)

    def test_api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get(self):
        """
            Retrieve an AD object by id that have deviances for a specific profile and checker
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directory_id_event_id_ad_objects_id_changes_get(api,x_api_key,1,1,1,1)
        assert(thread != None)

    def test_api_infrastructure_id_directory_id_event_id_ad_objects_id_get(self):
        """
            Get ad-object instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directory_id_event_id_ad_objects_id_get(api, x_api_key, 1, 1, 1, 1)
        assert (thread != None)

    def test_api_profiles_profile_id_checker_id_ad_objects_id_get(self):
        """
            Get one ad-object changes between a given event and the event which precedes it
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_profile_id_checker_id_ad_objects_id_get(api, x_api_key, 1, 1, 1)
        assert (thread != None)

    def test_api_profiles_profile_id_checker_id_ad_objects_search_post(self):
        """
            Search all AD objects having deviances by profile by checker
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "expression": {
                "testKey": "testValue"
            },
            "directories": [1],
            "dateStart": "17/8/2021",
            "dateEnd": "17/8/2021",
            "showIgnored": True
        }

        thread = api.api_profile_id_checker_id_ad_objects_search_post(api,body, x_api_key, 1, 1)
        assert (thread != None)
