from unittest import TestCase
from tenable.ad.email_notifier import EmailNotifierApi as api
from tenable.ad import APIKeyApi as apikey


class TestEmailNotifierApi(TestCase):
    def test_api_email_notifiers_get(self):
        """
            Retrieve all email-notifier instances.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_email_notifiers_get(api, x_api_key)
        count = len(thread)
        #data is not there, need to create
        assert(thread != None)

    def test_api_email_notifiers_id_delete(self):
        """
            Delete email-notifier instance.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_email_notifiers_id_delete(api, x_api_key,1)
        assert(thread != 200)




