from unittest import TestCase
from tenable.ad.dashboard import DashboardApi as api
from tenable.ad import APIKeyApi as apikey


class TestDashboardApi(TestCase):

    def test_api_dashboards_get(self):
        """
            Retrieve all dashboard instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_dashboards_get(api, x_api_key)
        assert (thread != None)

    def test_api_dashboards_id_delete(self):
        """
           Delete dashboard instance with it's associated widgets
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_dashboards_id_delete(api, x_api_key,1)
        assert(thread != None)

    def test_api_dashboards_id_get(self):
        """
            Get dashboard instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_dashboards_id_get(api, x_api_key,1)
        assert(thread != None)

    def test_api_dashboards_id_patch(self):
        """
            Update dashboard instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "name": "Active Users",
            "order": 1
        }

        thread = api.api_dashboards_id_patch(api, body, x_api_key,1)
        assert (thread != None)


    def test_api_dashboards_post(self):
        """
            Create dashboard instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "name": "Active Events",
            "order": 1
        }
        thread = api.api_dashboards_post(api,body, x_api_key)
        assert(thread != None)


