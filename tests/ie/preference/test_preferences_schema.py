'''
Testing the preferences schemas
'''
import pytest
from tenable.ie.preference.schema import PreferenceSchema


@pytest.fixture()
def preferences_schema():
    return {
        'language': 'en',
        'preferred_profile_id': 1
    }


def test_preferences_schema(preferences_schema):
    '''
    test preference schema
    '''
    test_resp = {
        'language': 'en',
        'preferredProfileId': 1
    }
    schema = PreferenceSchema()
    req = schema.dump(schema.load(preferences_schema))
    assert test_resp['language'] == req['language']
    assert test_resp['preferredProfileId'] == req['preferredProfileId']
