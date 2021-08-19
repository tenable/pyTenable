from unittest import TestCase
from tenable.ad.attack_alert import AttackAlertApi as api
from tenable.ad import APIKeyApi as apikey

class TestAttackApi(TestCase):

    def test_api_attack_types_get_with_http_info(self, **kwargs):
        """
            Get attack types
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_alerts_ioa_count_get(api, x_api_key)
        count = len(thread)
        assert(thread.get('statusCode') == 404)
        assert(thread.get('error') == 'Not Found')
        assert(thread.get('message') == 'Not Found')
        assert(len(thread) == 3)


    def test_api_alerts_ioa_get(self, **kwargs):
        x_api_key = apikey.get_api_key(self)
        thread = api.api_alerts_ioa_get(api, x_api_key)
        count = len(thread)
        assert(thread[0] == 'statusCode')
        assert(thread[1] == 'error')
        assert(thread[2] == 'message')
        assert(len(thread) == 3)

    def test_api_alerts_ioa_id_patch(self, **kwargs):
        x_api_key = apikey.get_api_key(self)
        thread = api.api_alerts_ioa_id_patch(api, x_api_key)
        count = len(thread)
        assert(len(thread) == 3)
        assert(len(thread) == 3)
        assert(thread.get('statusCode') == 404)
        assert(thread.get('error') == 'Not Found')
        assert(thread.get('message') == 'Not Found')
        assert(len(thread) == 3)

    def test_api_alerts_ioa_id_patch(self, **kwargs):
        x_api_key = apikey.get_api_key(self)
        body = {}
        thread = api.api_alerts_ioa_patch(api,body, x_api_key)
        count = len(thread)
        assert(len(thread) == 3)
        assert(thread.get('statusCode') == 404)
        assert(thread.get('error') == 'Not Found')
        assert(thread.get('message') == 'Not Found')
        assert(len(thread) == 3)



