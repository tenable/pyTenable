'''tests for checker option schemas'''
import pytest
from marshmallow.exceptions import ValidationError
from tenable.ad.checker_option.schema import CheckerOptionSchema


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
        "staged": 'true',
        "translations": ['string'],
        "perPage": '1',
        "page": '1'
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
        "staged": 'true',
        "perPage": '1',
        "page": '1'
    }]
    schema = CheckerOptionSchema()
    assert test_response[0]['name'] == schema.dump(schema.load(
        checker_option_schema[0]))['name']
    with pytest.raises(ValidationError):
        checker_option_schema[0]['new_val'] = 'something'
        schema.load(checker_option_schema)


def test_checker_option_schema_validation_error(checker_option_schema):
    schema = CheckerOptionSchema()
    with pytest.raises(ValidationError):
        checker_option_schema[0]['staged'] = 1
        schema.load(checker_option_schema)
