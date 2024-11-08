'''
Testing the profiles schemas
'''
import pytest
from marshmallow import ValidationError
from tenable.ie.profiles.schema import ProfileSchema


@pytest.fixture()
def profile_schema():
    return {
        'name': 'name',
        'directories': [1, 2]
    }


def test_profile_schema(profile_schema):
    '''
    Test the profile schema with create payload inputs
    '''
    test_resp = [{
        'id': 1,
        'name': 'name',
        'deleted': True,
        'directories': [1, 2],
        'dirty': True,
        'hasEverBeenCommitted': True
    }]

    schema = ProfileSchema()
    req = schema.dump(schema.load(profile_schema))
    assert test_resp[0]['name'] == req['name']
    assert test_resp[0]['directories'] == req['directories']

    with pytest.raises(ValidationError):
        profile_schema['some_val'] = 'something'
        schema.load(profile_schema)
