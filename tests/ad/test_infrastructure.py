from unittest import TestCase
from tenable.ad.infrastructure import InfrastructureApi as api
from tenable.ad import APIKeyApi as apikey

class TestInfrastructureApi(TestCase):
    def test_api_infrastructures_get(self):
        """
            Retrieve all infrastructure instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructures_get(api, x_api_key)
        count = len(thread)
        assert(len(thread) == 0)

    def test_api_infrastructures_id_delete(self):
        """
            Delete infrastructure instance.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructures_id_delete(api, x_api_key,1)
        count = len(thread)
        assert(thread != None)

    def test_api_infrastructures_id_get(self):
        """
            Get infrastructure instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructures_id_get(api, x_api_key,1)
        count = len(thread)
        assert(thread != None)

    def test_api_infrastructures_id_patch(self):
        """
            Update infrastructure instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {}
        thread = api.api_infrastructures_id_patch(api, body,x_api_key,1)
        count = len(thread)
        assert(thread != None)

    def test_api_infrastructures_post(self):
        """
            Create infrastructure instance.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructures_post(api, x_api_key,1)
        count = len(thread)
        assert(thread != None)
