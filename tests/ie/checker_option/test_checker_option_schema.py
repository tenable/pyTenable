'''tests for checker option schemas'''
import pytest
from marshmallow.exceptions import ValidationError
from tenable.ie.checker_option.schema import CheckerOptionSchema


@pytest.fixture
def checker_option_schema():
    return [{
        "id": 0,
        "codename": "string",
        "profileId": 0,
        "checkerId": 0,
        "directoryId": 0,
        "value": "string",
        "valueType": "string",
        "name": "string",
        "description": "string",
        "staged": True,
        "translations": ['string']
    }]


def test_checker_option_schema(checker_option_schema):
    test_response = [{
        "id": 0,
        "codename": "string",
        "profileId": 0,
        "checkerId": 0,
        "directoryId": 0,
        "value": "string",
        "valueType": "string",
        "name": "string",
        "description": "string",
        "staged": True
    }]
    schema = CheckerOptionSchema()
    assert test_response[0]['name'] == schema.dump(schema.load(
        checker_option_schema[0]))['name']
    with pytest.raises(ValidationError):
        checker_option_schema[0]['new_val'] = 1
        schema.load(checker_option_schema[0])
