'''
Test case for Policies Schema
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.vm.policies.schema import PolicySchema


@pytest.fixture
def policies_schema():
    '''
    Policy schema
    '''
    return {
        'settings': {
            'patch_audit_over_telnet': 'no',
            'enable_plugin_list': 'no',
            'enumerate_all_ciphers': 'yes'
        },
        'uuid': '123e4567-e89b-12d3-a456-556642440000',
        'credentials': {
            'current': {}
        }
    }


def test_policies_schema(policies_schema):
    '''
    Test the policies schema
    '''
    schema = PolicySchema()
    payload = schema.dump(
        schema.load(policies_schema)
    )
    assert payload['uuid'] == policies_schema['uuid']
    assert isinstance(payload['settings'], dict)
    assert isinstance(payload['credentials'], dict)


def test_policies_schema_invalid(policies_schema):
    '''
    Test the policies schema
    '''
    schema = PolicySchema()
    policies_schema['uuid'] = 1
    with pytest.raises(ValidationError):
        schema.dump(
            schema.load(policies_schema)
        )
