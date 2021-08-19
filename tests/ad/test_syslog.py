from unittest import TestCase
from tenable.ad.syslog import SyslogApi as api
from tenable.ad import APIKeyApi as apikey


class TestSyslogApi(TestCase):
    def test_api_syslogs_get_with_http_info(self):
        """
            Retrieve all syslog instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_syslogs_get(api,x_api_key)
        assert (thread != None)

    def test_api_syslogs_id_delete(self):
        """
            Delete syslog instance.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_syslogs_id_delete(api,x_api_key,1)
        assert (thread != None)

    def test_api_syslogs_id_get(self):
        """
            Get syslog instance by id.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_syslogs_id_get(api,x_api_key,1)
        assert (thread != None)

    def test_api_syslogs_id_patch(self):
        """
            Update syslog instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "directories": [2],
            "checkers": [2],
            "profiles": [1],
            "attackTypes": [1],
            "ip": "191.23.21.34",
            "port": 86,
            "protocol": "TCP",
            "tls": True,
            "criticityThreshold": 1,
            "description": "Hello",
            "inputType": "deviances"
        }
        thread = api.api_syslogs_id_patch(api,body,x_api_key,1)
        assert (thread != None)

    def test_api_syslogs_post(self):
        """
            Create syslog instance.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "directories": [2],
            "checkers": [2],
            "profiles": [1],
            "attackTypes": [1],
            "ip": "191.23.21.34",
            "port": 86,
            "protocol": "TCP",
            "tls": True,
            "criticityThreshold": 1,
            "description": "Hello",
            "inputType": "deviances"
        }
        thread = api.api_syslogs_post(api,body,x_api_key)
        assert (thread != None)

    def test_api_syslogs_test_message_id_get(self):
        """
            Send a test syslog notification by id
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_syslogs_test_message_id_get(api,x_api_key,1)
        assert (thread != None)

    def test_api_syslogs_test_message_post(self):
        """
            Send a test syslog notification
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            "directories": [2],
            "checkers": [2],
            "profiles": [1],
            "attackTypes": [1],
            "ip": "191.23.21.34",
            "port": 86,
            "protocol": "TCP",
            "tls": True,
            "criticityThreshold": 1,
            "description": "Hello",
            "inputType": "deviances"
        }
        thread = api.api_syslogs_test_message_post(api,body,x_api_key)
        assert (thread != None)




