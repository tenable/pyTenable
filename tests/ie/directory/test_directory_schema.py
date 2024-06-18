'''test directory schema'''
import pytest
from marshmallow import ValidationError
from tenable.ie.directories.schema import DirectorySchema


@pytest.fixture
def directory_schema():
    return {
        'infrastructureId': 1,
        'id': 1,
        'name': 'test',
        'ip': '172.32.68.1',
        'dns': 'company.tld',
        'type': 'type',
        'ldapPort': 321,
        'globalCatalogPort': 0,
        'smbPort': 0
    }


def test_directory_schema(directory_schema):
    '''
    tests the directory schema
    '''
    test_response = {
        'dns': 'company.tld',
        'global_catalog_port': 1,
        'id': 1,
        'infrastructure_id': 2,
        'ip': '172.16.0.1',
        'ldapInitialized': None,
        'ldap_port': 389,
        'name': 'some_name',
        'smb_port': 445,
        'sysvolInitialized': None,
        'type': 'type',
        "ldapCrawlingStatus": "string",
        "sysvolCrawlingStatus": "string",
        "honeyAccountAdObjectId": 0,
        "honeyAccountDistinguishedName": "honey",
        "honeyAccountConfigurationStatus": "string"
    }
    schema = DirectorySchema()
    assert test_response['dns'] == \
           schema.dump(schema.load(directory_schema))['dns']
    with pytest.raises(ValidationError):
        directory_schema['new_val'] = 'something'
        schema.load(directory_schema)
