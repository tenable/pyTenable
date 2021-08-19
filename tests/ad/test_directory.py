from unittest import TestCase
from tenable.ad.directory import DirectoryApi as api
from tenable.ad import APIKeyApi as apikey


class TestDirectoryApi(TestCase):
    def test_api_directories_get(self):
        """
            Retrieve all directory instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_directories_get(api, x_api_key)
        assert(thread != None)

    def test_api_directories_id_get(self):
        """
            Get directory instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_directories_id_get(api, x_api_key,1)
        assert(thread != None)

    def test_api_directories_post(self):
        """
            Create directory instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = [
            {
                "infrastructureId": 1,
                "name": "mvs",
                "ip": "10.10.10.10",
                "ldapPort": 1,
                "globalCatalogPort": 1,
                "smbPort": 1,
                "dns": "tenable"
            }
        ]
        thread = api.api_directories_post(api, body, x_api_key)
        assert(thread != None)

    def test_api_infrastructure_id_directories_get(self):
        """
            Get all directories for a given infrastructure
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directories_get(api, x_api_key, 1)
        assert(thread != None)

    def test_api_infrastructure_id_directories_id_delete(self):
        """
            Delete directory instance.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directories_id_delete(api, x_api_key, 1,1)
        assert(thread != None)

    def test_api_infrastructure_id_directories_id_get(self):
        """
            Get directory instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructure_id_directories_id_get(api, x_api_key, 1,1)
        assert(thread != None)

    def test_api_infrastructure_id_directories_id_patch(self):
        """
            Update directory instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "ignoreUntil": "19-01-2021 2:00PM"
        }
        thread = api.api_infrastructure_id_directories_id_patch(api,body, x_api_key, 1,1)
        assert(thread != None)

