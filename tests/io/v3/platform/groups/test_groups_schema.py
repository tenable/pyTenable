'''
Testing the Platform groups schemas
'''
import pytest
from marshmallow import ValidationError

from tenable.io.v3.platform.groups.schema import PlatformGroupSchema


def test_platform_groups_schema_for_all_fields():
    '''
    Test the platform_groups schema with name, group_id, user_id
    '''
    name: str = 'sample name'
    group_id: str = '00000000-0000-0000-0000-000000000000'
    user_id: str = '00000000-0000-0000-0000-000000000000'

    payload = {
        'name': name,
        'group_id': group_id,
        'user_id': user_id
    }
    test_resp = {
        'name': name,
        'group_id': group_id,
        'user_id': user_id
    }
    schema = PlatformGroupSchema()
    assert test_resp == schema.dump(schema.load(payload))


def test_groups_schema_parameters_type_error(api):
    '''
    Test to raise exception when values of name, group_id, user_id, don't match expected type.
    '''
    payload = {
        'name': 2,
        'group_id': 00000000-0000-0000-0000-000000000000,
        'user_id': 00000000-0000-0000-0000-000000000000
    }

    with pytest.raises(ValidationError) as validation_error:
        PlatformGroupSchema().load(payload)
    assert len(validation_error.value.messages) == 3, "Test case should raise validation errors for THREE parameters."

    assert len(validation_error.value.messages['name']) == 1, \
        "Only one validation error should be raised by test-case for name parameter."
    assert len(validation_error.value.messages['group_id']) == 1, \
        "Only one validation error should be raised by test-case for group_id parameter."
    assert len(validation_error.value.messages['user_id']) == 1, \
        "Only one validation error should be raised by test-case for user_id parameter."

    assert validation_error.value.messages['name'][0] == "Not a valid string.", \
        "Invalid type validation error for name parameter is not raised by test-case."
    assert validation_error.value.messages['group_id'][0] == "Not a valid UUID.", \
        "Invalid type validation error for group_id parameter is not raised by test-case."
    assert validation_error.value.messages['user_id'][0] == "Not a valid UUID.", \
        "Invalid type validation error for user_id parameter is not raised by test-case."
