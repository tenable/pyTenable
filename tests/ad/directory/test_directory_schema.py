'''test directory schema'''
import pytest
from marshmallow import INCLUDE, ValidationError

from tenable.ad.directories.schema import DirectorySchema


@pytest.fixture
def directory_schema():
    return {'infrastructureId': 1,
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
    test_response = {'dns': 'company.tld',
                     'global_catalog_port': 3268,
                     'id': 13,
                     'infrastructure_id': 2,
                     'ip': '172.16.0.1',
                     'ldapInitialized': None,
                     'ldap_port': 389,
                     'name': 'dheeraj2',
                     'smb_port': 445,
                     'sysvolInitialized': None,
                     'type': 'type'
                     }
    schema = DirectorySchema()
    assert test_response['dns'] == \
           schema.dump(schema.load(directory_schema))['dns']
    with pytest.raises(ValidationError):
        directory_schema['new_val'] = 'something'
        schema.load(directory_schema)
