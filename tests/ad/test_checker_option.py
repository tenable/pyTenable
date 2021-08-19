from unittest import TestCase
from tenable.ad.checker_option import CheckerOptionApi as api
from tenable.ad import APIKeyApi as apikey


class TestCheckerOptionApi(TestCase):
    def test_api_profiles_profile_id_checkers_checker_id_checker_options_get(self):
        """
            Get all checker options related to a checker.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_profiles_profile_id_checkers_checker_id_checker_options_get(api, x_api_key,1,1)
        assert(thread != None)

    def test_api_profiles_profile_id_checkers_checker_id_checker_options_post(self):
        """
            Create checker options related to a checker.
        """
        x_api_key = apikey.get_api_key(self)
        body = [
            {
                "directoryId": 1,
                "codename": "test",
                "value": "1",
                "valueType": "regex"
            }
        ]

        thread = api.api_profiles_profile_id_checkers_checker_id_checker_options_post(api,body, x_api_key, 1, 1)
        assert (thread != None)
