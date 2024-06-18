'''
Testing the license schemas
'''
import datetime
import pytest
from tenable.ie.license.schema import LicenseSchema


@pytest.fixture()
def license_schema_request_payload():
    return {
        'license': 'license'
    }


def test_license_schema_request_payload(license_schema_request_payload):
    '''
    test license create payload input to schema
    '''
    schema = LicenseSchema()
    req = schema.dump(schema.load(license_schema_request_payload))
    assert req['license'] == 'license'


@pytest.fixture()
def license_schema_response():
    return {
        'customerName': 'pytenable',
        'maxActiveUserCount': 100,
        'currentActiveUserCount': 0,
        'expirationDateUTC': '2021-11-17T13:44:24.259Z',
        'inAppEula': False,
        'features': ['something'],
        'type': 'license type'
    }


def test_license_schema_response(license_schema_response):
    '''
    test license get response to schema
    '''
    schema = LicenseSchema()
    req = schema.load(license_schema_response)
    assert req['customer_name'] == 'pytenable'
    assert req['max_active_user_count'] == 100
    assert req['current_active_user_count'] == 0
    assert req['expiration_date_utc'] == datetime.datetime(
        2021, 11, 17, 13, 44, 24, 259000, tzinfo=datetime.timezone.utc)
    assert req['in_app_eula'] is False
    assert req['features'][0] == 'something'
    assert req['license_type'] == 'license type'
