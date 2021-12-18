'''
Testing the Network schemas
'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.io.v3.vm.networks.schema import NetworkSchema


def test_create_fields_positive():
    '''
    Test the vulnerability finding schema
    '''
    expected_payload = {
            'name': 'name',
            'description': 'description',
            'assets_ttl_days': 64
        }
    schema = NetworkSchema()
    payload = schema.dump(
        schema.load({
            'name': 'name',
            'description': 'description',
            'assets_ttl_days': 64
        })
    )
    assert expected_payload == payload


def test_field_assets_ttl_days():
    '''
    Test the vulnerability finding schema
    '''
    expected_payload = {
            'name': 'name',
            'description': 'description'
        }
    schema = NetworkSchema()
    payload = schema.dump(
        schema.load({
            'name': 'name',
            'description': 'description'
        })
    )
    assert expected_payload == payload


def test_field_description():
    '''
    Test the vulnerability finding schema
    '''
    expected_payload = {
            'name': 'name',
            'description': ''
        }
    schema = NetworkSchema()
    payload = schema.dump(schema.load({'name': 'name'}))
    assert expected_payload == payload


def test_field_scanner_uuids_positive():
    '''
    Test the vulnerability finding schema
    '''
    scanner_uuids = ['00000000-0000-0000-0000-000000000000']
    expected_payload = {'scanner_uuids': scanner_uuids}
    schema = NetworkSchema(only=["scanner_uuids"])
    payload = schema.dump(
        schema.load({'scanner_uuids': scanner_uuids})
    )
    assert expected_payload == payload


def test_field_scanner_uuids_negative():
    '''
    Test the vulnerability finding schema
    '''
    scanner_uuids = ['invalid_uuid']
    schema = NetworkSchema()
    with pytest.raises(ValidationError):
        schema.dump(
            schema.load({'scanner_uuids': scanner_uuids})
        )
