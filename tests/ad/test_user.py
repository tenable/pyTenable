from pprint import pprint
from unittest import TestCase
from tenable.ad.user import  UserApi as api
from tenable.ad import APIKeyApi as apikey


class TestUserApi(TestCase):

    def test_api_login_post_with_http_info(self):
        """
            Logs in a user
        """
        x_api_key = apikey.get_api_key(self)
        body = {"authToken": x_api_key}
        thread = api.api_login_post(api,body)
        if (thread["error"] != None):
            print("User data can not be modified")
        else:
            print("User data had been modified")

    def test_api_users_whoami_get(self):
        """
            Get a user's information
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_users_whoami_get(api,x_api_key)
        if (len(thread) != 0):
            assert (thread['id'] == 18)
            assert (thread['name'] == 'Muthu')
            assert (thread['email'] == 'ms.valliammal@delixus.com')
            assert (thread['internal'] == False)
            assert (thread['provider'] == 'tenable')
            assert (thread['department'] == 'TenableAD')

    def test_api_users_retrieve_password_post_with_http_info(self):
        """
            Retrieves a user's password
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "token": x_api_key,
            "newPassword": 'abcd*'
        }
        thread = api.api_users_retrieve_password_post_with_http_info(api,body)
        if (len(thread) != 0):
            if (thread[0]["error"] != None):
                print("User data can not be modified")
            else:
                print("User data had been modified")
        assert(thread != None)


    def test_api_users_password_patch_with_http_info(self):
        """
            Update a user's password
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "token": x_api_key,
            "newPassword": 'valliammal123*'
        }
        thread = api.api_users_password_patch_with_http_info(api,body,x_api_key)
        if (len(thread) != 0) and (thread[0] != ''):
            if (thread[0]["error"] != None):
                print("User data can not be modified")
            else:
                print("User data had been modified")
        assert(thread != None)


    def test_api_users_id_roles_put(self):
        """
            Replace role list for a user
        """
        x_api_key = apikey.get_api_key(self)
        body = {
           "picture": [1],
            "surname": "Muthu",
            "name": "Valliammal",
            "department": "ITSecurity",
            "biography": "Architect",
            "active": True
        }
        thread = api.api_users_id_roles_put(api,body, x_api_key,18)
        if (len(thread) != 0):
            if (thread["error"] != None):
                print("User data can not be modified")
            else:
                print("User data had been modified")
        assert(thread != None)

    def test_api_users_id_patch(self):
        """
            Update user instance
        """
        x_api_key = apikey.get_api_key(self)
        body = {
           "picture": [1],
            "surname": "Muthu",
            "name": "Valliammal",
            "department": "ITSecurity",
            "biography": "Architect",
            "active": True
        }
        thread = api.api_users_id_patch(api, body, x_api_key,1)
        if (len(thread) != 0):
            if (thread["error"] != None):
                print("User data can not be modified")
            else:
                print("User data had been modified")
        assert(thread != None)

    def test_api_users_id_get_with_http_info(self):
        """
            Get user instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
           "picture": [1],
            "surname": "Muthu",
            "name": "Valliammal",
            "department": "ITSecurity",
            "biography": "Architect",
            "active": True
        }
        thread = api.api_users_id_get_with_http_info(api, x_api_key,1)
        if (len(thread) != 0) and (thread[0] != ''):
            if (thread[0]['id'] == 1):
                assert (thread[0]["name"] == 'Admin')
                assert (thread[0]["email"] == 'hello@tenable.ad')
                assert (thread[0]['active'] == True)
                assert (thread[0]['department'] == None)
                assert (thread[0]['biography'] == None)
                assert (thread[0]['picture'] == None)
                assert (thread[0]['roles'] == [1])
        assert(thread != None)

    def test_api_users_id_delete(self):
        """
            Get all users
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_users_get(api, x_api_key)
        count = len(thread)
        if (count > 0) :
            thread = api.api_users_id_delete(api, x_api_key,20)
            thread = api.api_users_get(api, x_api_key)
            count_after_delete = len(thread)
            assert(count == (count_after_delete + 1))
        assert(thread != None)

    def test_api_users_get(self):
        """
            Get all users
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_users_get(api, x_api_key)
        count = len(thread)
        if (len(thread) != 0):
            for i in range(count):
                assert(thread[i]["id"] != 0)
                if (thread[i]['id'] == 1):
                    assert(thread[i]["name"] == 'Admin')
                    assert(thread[i]["email"] == 'hello@tenable.ad')
                    assert(thread[i]['active'] == True)
                    assert(thread[i]['department'] == None)
                    assert(thread[i]['biography'] == None)
                    assert(thread[i]['picture'] == None)
                    assert(thread[i]['provider'] == 'tenable')
                    assert(thread[i]['identifier'] == 'hello@tenable.ad')
                    assert(thread[i]['eulaVersion'] == -1)
                    assert(thread[i]['roles'] == [1])
        assert(thread != None)


    def test_api_users_forgotten_password_post(self):
        """
            Sends an email to create a new password
        """
        x_api_key = apikey.get_api_key(self)
        body = {
           "picture": [1],
            "surname": "Muthu",
            "name": "Valliammal",
            "department": "ITSecurity",
            "biography": "Architect",
            "active": True
        }
        thread = api.api_users_forgotten_password_post(api, body)
        assert(thread != None)

    def test_api_logout_post(self):
        """
            Logs out a user
        """
        x_api_key = apikey.get_api_key(self)
        body = {
           "picture": [1],
            "surname": "Muthu",
            "name": "Valliammal",
            "department": "ITSecurity",
            "biography": "Architect",
            "active": True
        }
        thread = api.api_logout_post_with_http_info(api, x_api_key)
        assert(thread != None)

    def test_api_login_post(self):
        """
            Logs in a user
        """
        x_api_key = apikey.get_api_key(self)
        body = {
           "picture": [1],
            "surname": "Muthu",
            "name": "Valliammal",
            "department": "ITSecurity",
            "biography": "Architect",
            "active": True
        }
        thread = api.api_login_post(api, body)
        assert(thread != None)

