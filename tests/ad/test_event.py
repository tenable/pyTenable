from unittest import TestCase
from tenable.ad.event import EventApi as api
from tenable.ad import APIKeyApi as apikey


class TestEventApi(TestCase):
    def test_api_events_event_provider_id_last_events_get(self):
        """
            Get the last events for each AD object source and directory
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_events_event_provider_id_last_events_get(api, x_api_key,1)
        count = len(thread)
        #data is not there, need to create
        assert(len(thread) == 0)

    def test_api_events_last_get(self):
        """
            Get the last event
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_events_last_get(api, x_api_key)
        count = len(thread)
        #data is not there, need to create
        assert(len(thread) == 0)

    def test_api_events_search_post(self):
        """
            Search events instances
        """
        x_api_key = apikey.get_api_key(self)
        body = {
                "order": {
                    "column": "id",
                    "direction": "asc"
                },
                "directoryIds": [
                    1
                ],
                "profileId": 1,
                "dateStart": "29-01-2021",
                "dateEnd": "29-01-2029"
        }
        thread = api.api_events_search_post(api,body, x_api_key)
        count = len(thread)
        assert(thread != None)

    def test_api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get(self):
        """
            Get the last event related to an AD Object
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructures_infrastructure_id_directories_directory_id_ad_objects_ad_object_id_events_last_get(
            api,x_api_key,1,1,1)
        count = len(thread)
        assert(thread != None)

    def test_api_infrastructures_infrastructure_id_directories_directory_id_events_id_get(self):
        """
            Get event instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_infrastructures_infrastructure_id_directories_directory_id_events_id_get(api,x_api_key,1,1,1)
        count = len(thread)
        assert(thread != None)
