from pprint import pprint
from unittest import TestCase
from tenable.ad.ldap_configuration import  LDAPConfigurationApi as api
from tenable.ad import APIKeyApi as apikey


class TestLDAPConfigurationApi(TestCase):
    def test_api_ldap_configuration_get(self):
        """
            Get ldap-configuration singleton.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_ldap_configuration_get(api,x_api_key)
        pprint(thread)
        assert(thread != None)
        #assert(thread.get("enabled") == False)
        #assert(thread.get("url") == None)
        #assert(thread.get("searchUserDN") == None)
        #assert(thread.get("userSearchBase") == None)
        #assert(thread.get("userSearchFilter") == None)
        #assert(thread.get("searchUserPassword") == None)
        #assert(thread.get("allowedGroups") == [])

    def test_api_ldap_configuration_patch(self):
        """
            Update ldap-configuration singleton.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "enabled": False,
            "url": 'pytenable.tenable.ad',
            "searchUserDN": 'pytenable.tenable.ad',
            "userSearchBase": 'tenable.ad',
            "userSearchFilter": '.ad',
            "searchUserPassword": "va",

            "allowedGroups": [
                {
                    "defaultRoleIds": [
                        2
                    ],
                    "name": "mva",
                    "defaultProfileId": 1
                }
            ]
        }
        thread = api.api_ldap_configuration_patch(api,body,x_api_key)
        pprint(thread)
        if (thread != None):
            print("ldap patch worked successfully")
