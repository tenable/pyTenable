from pprint import pprint
from unittest import TestCase
from tenable.ad.widget import WidgetApi as api
from tenable.ad import APIKeyApi as apikey


class TestWidgetApi(TestCase):
    def test_api_dashboards_dashboard_id_widgets_get(self):
        """
            Get all widgets by dashboard id
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_dashboards_dashboard_id_widgets_get(api, x_api_key, 1)
        if (len(thread) != 0):
            assert (thread[0] == 'error')
            assert (thread[1] == 'message')

    def test_api_widgets_get(self):
        """
            Retrieve all widget instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_widgets_get(api, x_api_key)
        if (len(thread) != 0) :
            assert (thread[0] == 'statusCode')
            assert (thread[1] == 'error')
            assert (thread[2] == 'message')

    def test_api_dashboards_dashboard_id_widgets_post(self):
        """
            Create a new widget in dashboard by dashboard id
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_dashboards_dashboard_id_widgets_post(api, x_api_key, 1)
        if (len(thread) != 0):
            assert (thread[0] == 'error')
            assert (thread[1] == 'message')


    def test_api_dashboards_dashboard_id_widgets_post(self):
        """
            Update widget instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "posX": 5,
            "posY": 6,
            "width": 5,
            "height": 6,
            "title": "DataPosted"
        }

        thread = api.api_dashboards_dashboard_id_widgets_id_patch(api, body,x_api_key, 1,1)
        if (len(thread) != 0):
            assert (thread[0] == 'error')
            assert (thread[1] == 'message')


    def test_api_dashboards_dashboard_id_widgets_patch(self):
        """
            Update widget instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "posX": 5,
            "posY": 6,
            "width": 5,
            "height": 6,
            "title": "DataPosted"
        }
        thread = api.api_dashboards_dashboard_id_widgets_id_patch(api, body, x_api_key, 1,1)
        if (len(thread) != 0):
            assert (thread[0] == 'error')
            assert (thread[1] == 'message')

    def test_api_dashboards_dashboard_id_widgets_id_options_put(self):
        """
            Define widget's options by id
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "posX": 5,
            "posY": 6,
            "width": 5,
            "height": 6,
            "title": "DataPosted"
        }
        thread = api.api_dashboards_dashboard_id_widgets_id_options_put(api, body,x_api_key, 1,1)
        if (len(thread) != 0):
            assert (thread[0] == 'error')
            assert (thread[1] == 'message')

