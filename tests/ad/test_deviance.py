from unittest import TestCase
from tenable.ad.deviance import DevianceApi as api
from tenable.ad import APIKeyApi as apikey


class TestDevianceApi(TestCase):
    def test_api_infrastructure_id_directories_directory_id_deviances_get_with_http_info(self):
        """
            Get all deviances for a directory.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directory_id_deviances_get_with_http_info(api, x_api_key,1,1)
        assert (thread != None)

    def test_api_infrastructure_id_directory_id_deviances_get_with_http_info(self):
        """
            Get ad-object-deviance-history instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directory_id_deviances_get_with_http_info(api, x_api_key,1,1)
        assert (thread != None)

    def test_api_infrastructure_id_directory_id_deviances_id_get(self):
        """
            Get ad-object-deviance-history instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directory_id_deviances_id_get(api, x_api_key,1,1,1)
        assert (thread != None)

    def test_api_infrastructure_id_directory_id_deviances_id_patch(self):
        """
            Update ad-object-deviance-history instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "ignoreUntil": "19-01-2020 2:00PM"
        }
        thread = api.api_infrastructure_id_directory_id_deviances_id_patch(api,body, x_api_key,1,1,1)
        assert(thread != None)
