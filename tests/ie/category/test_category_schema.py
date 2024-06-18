'''tests for category schema'''
import pytest
from marshmallow.exceptions import ValidationError
from tenable.ie.category.schema import CategorySchema


@pytest.fixture
def category_schema():
    return {
        'id': 2,
        'name': 'test_category'
    }


def test_category_schema(category_schema):
    test_category_response = {
        'id': 2,
        'name': 'test_category'
    }
    schema = CategorySchema()
    assert test_category_response['name'] == schema.dump(
        schema.load(category_schema))['name']
    with pytest.raises(ValidationError):
        category_schema['new_val'] = 'something'
        schema.load(category_schema)
