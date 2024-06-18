'''tests for saml_configuration schema'''
import pytest
from marshmallow.exceptions import ValidationError
from tenable.ie.saml_configuration.schema import SAMLConfigurationSchema


@pytest.fixture
def saml_configuration_schema():
    return {
        'activateCreatedUsers': True,
        'allowedGroups': [{
                'defaultProfileId': 1,
                'defaultRoleIds': [1, 2],
                'name': 'test'
            }],
        'assertEndpoint': 'assert_endpoint_url',
        'enabled': True,
        'encryptionCertificate': 'certificate',
        'providerLoginUrl': 'url',
        'serviceProviderUrl': 'https://pytenable.tenable.ad',
        'signatureCertificate': 'certificate'
    }


def test_saml_configuration_schema(saml_configuration_schema):
    test_response = {
        'activateCreatedUsers': True,
        'allowedGroups': [{
                'defaultProfileId': 1,
                'defaultRoleIds': [1, 2],
                'name': 'test'
            }],
        'assertEndpoint': 'assert_endpoint_url',
        'enabled': True,
        'encryptionCertificate': 'certificate',
        'providerLoginUrl': 'url',
        'serviceProviderUrl': 'https://pytenable.tenable.ad',
        'signatureCertificate': 'certificate'
    }
    schema = SAMLConfigurationSchema()
    req = schema.dump(schema.load(
        saml_configuration_schema))['allowedGroups'][0]
    assert test_response['allowedGroups'][0]['name'] == req['name']
    with pytest.raises(ValidationError):
        saml_configuration_schema['new_val'] = 'something'
        schema.load(saml_configuration_schema)
