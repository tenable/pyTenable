'''schema tests for dashboard APIs'''
import pytest
from marshmallow.exceptions import ValidationError
from tenable.ie.dashboard.schema import DashboardSchema


@pytest.fixture
def dashboard_schema():
    return {
        'id': 2,
        'name': 'test_name',
        'order': 5,
        'userId': 10
    }


def test_dashboard_schema(dashboard_schema):
    test_response = {
        'id': 2,
        'name': 'test_name',
        'order': 5,
        'userId': 10
    }
    schema = DashboardSchema()
    assert test_response['name'] == \
           schema.dump(schema.load(dashboard_schema))['name']
    with pytest.raises(ValidationError):
        dashboard_schema['new_val'] = 'something'
        schema.load(dashboard_schema)
