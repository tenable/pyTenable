from pprint import pprint
from unittest import TestCase
from tenable.ad.profile import  ProfileApi as api
from tenable.ad import APIKeyApi as apikey


class TestProfileApi(TestCase):
    def test_api_profiles_get(self):
        """
            Retrieve all profile instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_profiles_get(api,x_api_key)
        assert(thread != None)
        #count = len(thread)
        #assert(len(thread) != 0)
        #for i in range(count):
        #    pprint(thread[i])
        #    assert (thread[i]["id"] != 0)
        #    assert (thread[i]["name"] != None)
        #    assert (thread[i]["deleted"] == False)
        #    assert (thread[i]["dirty"] == False)
        #    assert (thread[i]["hasEverBeenCommitted"] != None)
        #    assert (thread[i]["directories"] == [])


    def test_api_profiles_post(self):
        """
            Creates a new profile from another one
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "directories": [1],
            "name": "Muthu"
        }
        thread = api.api_profiles_from_from_id_post(api,body,x_api_key,1)
        assert(thread != None)
        #if (thread.get("error") == None) :
        #    count = len(thread)
        #    assert(len(thread) != 0)
        #    for i in range(count):
        #        pprint(thread[i])
        #        assert (thread[i]["id"] != 0)
        #        assert (thread[i]["name"] != None)
        #        assert (thread[i]["deleted"] == False)
        #        assert (thread[i]["dirty"] == False)
        #        assert (thread[i]["hasEverBeenCommitted"] != None)
        #        assert (thread[i]["directories"] == [])

    def test_api_profiles_id_commit_post(self):
        """
            Commits change of the related profile
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_profiles_id_commit_post(api,x_api_key,1)
        assert (thread != None)
        #if (thread.get("error") == None) :
        #    count = len(thread)
        #    assert(len(thread) != 0)
        #    for i in range(count):
        #        pprint(thread[i])
        #        assert (thread[i]["id"] != 0)
        #       assert (thread[i]["name"] != None)
        #       assert (thread[i]["deleted"] == False)
        #       assert (thread[i]["dirty"] == False)
        #       assert (thread[i]["hasEverBeenCommitted"] != None)
        #       assert (thread[i]["directories"] == [])

