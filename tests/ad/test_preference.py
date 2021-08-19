from unittest import TestCase
from tenable.ad.preference import PreferenceApi as api
from tenable.ad import APIKeyApi as apikey



class TestPreferenceApi(TestCase):

    def test_api_categories_get(self):
        """
            Get a user's preferences
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_preferences_get(api, x_api_key)
        assert(thread != None)
        #assert(thread["language"] == "en")
        #assert(thread["preferredProfileId"] == 1)

    def test_api_preferences_patch(self):
        """
            Update a user's preferences
        """
        x_api_key = apikey.get_api_key(self)
        payload = {'language': 'dutch', 'preferredProfileId': '2'}
        thread = api.api_preferences_patch(api,payload, x_api_key)
        assert(thread != None)
