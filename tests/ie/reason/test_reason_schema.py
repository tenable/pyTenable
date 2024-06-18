'''schea test for reason API schema'''
import pytest
from marshmallow import ValidationError
from tenable.ie.reason.schema import ReasonSchema


@pytest.fixture
def reason_schema():
    return {
        'id': 0,
        'codename': 'codename',
        'name': 'some_name',
        'description': 'some_desc'
    }


def test_reason_schema(reason_schema):
    test_response = {
        'id': 0,
        'codename': 'codename',
        'name': 'some_name',
        'description': 'some_desc'
    }
    schema = ReasonSchema()
    for key, value in test_response.items():
        assert schema.dump(schema.load(reason_schema))[key] == value
    with pytest.raises(ValidationError):
        reason_schema['new_val'] = 'something'
        schema.load(reason_schema)
