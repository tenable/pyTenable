'''tests for infrastructure schema'''
import pytest
from marshmallow.exceptions import ValidationError
from tenable.ie.infrastructure.schema import InfrastructureSchema


@pytest.fixture
def infrastructure_schema():
    return {
        'id': 1,
        'name': 'test',
        'login': 'test@tenable.com',
        'password': 'password',
        'directories': [0, 1, 2],
        'infrastructure_id': '1'
    }


def test_infrastructure_schema(infrastructure_schema):
    test_response = {
        'id': 1,
        'name': 'test',
        'login': 'test@tenable.com',
        'password': 'password',
        'directories': [0, 1, 2],
        'infrastructure_id': '1'
    }
    schema = InfrastructureSchema()
    assert test_response == schema.dump(schema.load(
        infrastructure_schema))
    with pytest.raises(ValidationError):
        infrastructure_schema['new_val'] = 'something'
        schema.load(infrastructure_schema)
