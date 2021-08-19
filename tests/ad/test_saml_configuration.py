from unittest import TestCase
from tenable.ad.saml_configuration import SAMLConfigurationApi as api
from tenable.ad import APIKeyApi as apikey


class TestSAMLConfigurationApi(TestCase):
    def test_saml_configuration_generate_certificate_get(self):
        """
            Generates SAML certificate
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_saml_configuration_generate_certificate_get(api, x_api_key)
        if (len(thread) != 0):
            if (thread.get("encryptionCertificate") != None):
                print ('encrypted certificate generated')
            else:
                print ('encrypted certificate is not generated')

    def test_api_saml_configuration_get(self):
        """
            Get saml-configuration singleton.
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_saml_configuration_get(api, x_api_key)
        if (len(thread) != 0):
            if (thread.get("encryptionCertificate") != None):
                assert(thread.get('enabled') == False)
                assert(thread.get('activateCreatedUsers') == False)
                assert(thread.get('providerLoginUrl') == None)
                assert(thread.get('signatureCertificate') == None)
                assert(thread.get('assertEndpoint') == "https://pytenable.tenable.ad/auth-service/providers/saml/assert")
                assert(thread.get('serviceProviderUrl') == "https://pytenable.tenable.ad")
            else:
                print ('encrypted certificate is not printed')

    def test_api_saml_configuration_patch(self):
        """
            Update saml-configuration singleton.
        """
        x_api_key = apikey.get_api_key(self)
        body = {
            'providerLoginUrl':'pytenable.tenable.ad'
        }
        thread = api.api_saml_configuration_patch(api, body,x_api_key)
        assert(thread != None)
        #if thread.get('error') != None:
        #    print (' the patch is done for the parameters in the tenable.ad')
