from unittest import TestCase
from tenable.ad.attack import AttackApi as api
from tenable.ad import APIKeyApi as apikey

class TestAttackApi(TestCase):

    def test_api_attack_types_get_with_http_info(self, **kwargs):
        """
            Get all attacks
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_attack_types_get(api, x_api_key)
        count = len(thread)
        if (len(thread) != 0):
            assert(len(thread) != 0)
            for i in range(count):
                assert(thread[0]["id"] != 0)
                assert(thread[0]["yaraRules"] != None)
                assert(thread[0]["workloadQuota"] != None)
                assert(thread[0]["vectorTemplateReplacements"] != None)
                assert(thread[0]["mitreAttackDescription"] != None)

