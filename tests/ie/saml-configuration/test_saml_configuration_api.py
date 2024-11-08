'''tests for saml_configuration API endpoints'''
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_saml_configuration_singleton(api):
    '''tests the saml_configuration_singleton API response with
    actual saml_configuration_singleton response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/saml-configuration',
                  json={
                      'activateCreatedUsers': True,
                      'allowedGroups': [{
                          'defaultProfileId': 1,
                          'defaultRoleIds': [1, 2],
                          'name': 'test'
                      }],
                      'assertEndpoint':
                          'assert_endpoint_url',
                      'enabled': True,
                      'encryptionCertificate': 'certificate',
                      'providerLoginUrl': 'url',
                      'serviceProviderUrl': 'https://pytenable.tenable.ad',
                      'signatureCertificate': 'certificate'
                  }
                  )
    resp = api.saml_configuration.details()
    assert isinstance(resp, dict)
    assert resp['allowed_groups'][0]['name'] == 'test'


@responses.activate
def test_saml_configuration_update(api):
    '''tests the update API response with actual update response'''
    responses.add(responses.PATCH,
                  f'{RE_BASE}/saml-configuration',
                  json={
                      'activateCreatedUsers': True,
                      'allowedGroups': [{
                          'defaultProfileId': 1,
                          'defaultRoleIds': [1, 2],
                          'name': 'updated_name'
                      }],
                      'assertEndpoint': 'assert_endpoint_url',
                      'enabled': True,
                      'encryptionCertificate': 'certificate',
                      'providerLoginUrl': 'url',
                      'serviceProviderUrl': 'https://pytenable.tenable.ad',
                      'signatureCertificate': 'certificate'
                  }
                  )
    resp = api.saml_configuration.update(allowed_groups=[{
        'name': 'updated_name',
        'default_profile_id': 1,
        'default_role_ids': [1, 2]
    }]
    )

    assert isinstance(resp, dict)
    assert resp['allowed_groups'][0]['name'] == 'updated_name'


@responses.activate
def test_saml_configuration_generate_saml_certificate(api):
    '''tests the generate saml certificate API response with actual
    saml certificate response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/saml-configuration/generate-certificate',
                  json={
                      'encryptionCertificate': 'generated_certificate',
                  }
                  )
    resp = api.saml_configuration.generate_saml_certificate()

    assert isinstance(resp, dict)
    assert resp['encryption_certificate'] == 'generated_certificate'
