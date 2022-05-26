'''
Tests cases for filter schema
'''
import pytest
import responses
from marshmallow.exceptions import ValidationError
from tenable.io.base.schemas.filters.base import BaseFilterSchema


@responses.activate
def test_populate_filters_validate_filter_success(api):
    '''
    Test case for BaseFilterSchema
    '''
    # Let's create test response
    filters_dict: dict = {
        'field': 'field1',
        'operator': 'operator1',
        'value': ['value1', 'value2'],
        'name': 'name1',
        'control': {
                'regex': 'val',
                'operators': ['operator1', 'operator2', 'operator3'],
                'list': ['value1', 'value2', 'value3']
        }
    }

    base_filter_schema = BaseFilterSchema()
    base_filter_schema.populate_filters(api, path='', filters=[filters_dict], force=True)
    base_filter_schema.validate_filter(name=filters_dict['name'], operator=filters_dict['operator'], value=filters_dict['value'])


@responses.activate
def test_populate_filters_validate_filter_validation_error(api):
    '''
    Test case for populate_filters and validate_filter validation error
    '''
    # Let's create test response
    filters_dict: dict = {
        'field': 'field1',
        'operator': 'operator1',
        'value': 'value1',
        'name' : 'name1',
        'control': {
                'regex': 'test',
                'operators': ['operator1', 'operator2', 'operator3'],
                'list': ['value2', 'value3', 'value4']
        }
    }
    with pytest.raises(ValidationError) as validation_error:
        base_filter_schema = BaseFilterSchema()

        base_filter_schema.populate_filters(api, path='', filters=[filters_dict], force=True)
        base_filter_schema.validate_filter(name=filters_dict['name'], operator=filters_dict['operator'], value=filters_dict['value'])
    assert '"value1" must be one of [\'value2\', \'value3\', \'value4\']' in validation_error.value.messages['value'][0]
    assert '"value1" does not match pattern test' in validation_error.value.messages['value'][1]


@responses.activate
def test_populate_filters_validate_filter_name_validation_error(api):
    '''
    Test case for populate_filters and validate_filter name validation error
    '''
    # Let's create test response
    filters_dict: dict = {
        'field': 'field1',
        'operator': 'operator1',
        'value': 'value4',
        'name' : 'name1',
        'control': {
                'regex': 'test' or None,
                'operators': ['operator1', 'operator2', 'operator3'],
                'list': ['value1', 'value2', 'value3'] or None
        }
    }
    with pytest.raises(ValidationError) as validation_error:
        base_filter_schema = BaseFilterSchema()

        base_filter_schema.populate_filters(api, path='', filters=[filters_dict], force=True)
        base_filter_schema.validate_filter(name=filters_dict['field'], operator=filters_dict['operator'], value=filters_dict['value'])
    assert '"field1" is not a valid filter' in validation_error.value.messages['name']
