from unittest import TestCase
from tenable.ad.role import  RoleApi as api
from tenable.ad import APIKeyApi as apikey


class TestReasonApi(TestCase):
    def test_api_reasons_get(self):
        """
            Retrieve all role instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_roles_get(api,x_api_key)
        count = len(thread)
        if (count != 0):
            assert(len(thread) != 0)
            for i in range(count):
                assert(thread[i]["id"] != 0)
                assert((thread[i]["name"] == "User") or (thread[i]["name"] == "Global Administrator"))
                assert(thread[i]["description"] != "")


    def test_api_roles_id_get(self):
        """
            Get role instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_roles_id_get(api, x_api_key,1)
        count = len(thread)
        if (count == 1):
            assert(thread['id'] == 1)
            assert(thread['name'] == 'Global Administrator')
            assert(thread['description'] != "")
        thread = api.api_roles_id_get(api, x_api_key,2)
        count = len(thread)
        if (count == 1):
            assert(thread['id'] == 2)
            assert(thread['name'] == 'User')
            assert(thread['description'] != "")

    def test_api_roles_from_from_id_post(self):
        """
            Creates a new role from another one
        """
        x_api_key = apikey.get_api_key(self)
        body = [
            {
                "name": "guest",
                "description": "guest users of tenable.ad will work in this"
            }
        ]
        thread = api.api_roles_from_from_id_post(api,body, x_api_key, 1)
        assert(thread != None)
        #if (thread.get("error") == None):
        #    print('role created successfully')
        #else:
        #    print('role is not created')

    def test_api_roles_id_patch(self):
        """
            Update role instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "name": "User",
            "description": "Read only permissions given"
        }
        thread = api.api_roles_id_patch(api,body, x_api_key, 2)
        assert (thread != None)
        #if (thread.get("error") == None):
        #    print('Role Patch done successfully')
        #else:
        #    print('Role Patch not done')
