from unittest import TestCase
from tenable.ad.topology import  TopologyApi as api
from tenable.ad import APIKeyApi as apikey


class TestTopologyApi(TestCase):
    def test_api_profiles_profile_id_topology_get(self):
        """
            Get a representation of the AD topology.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_profiles_profile_id_topology_get(api,x_api_key,1)
        assert(thread != None)
