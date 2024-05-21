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
    Test to populate filters and validate filter methods
    '''
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
    base_filter_schema.validate_filter(name=filters_dict['name'], operator=filters_dict['operator'],
                                       value=filters_dict['value'])


@responses.activate
def test_validate_filter_validation_error(api):
    '''
    Test to raise exception when invalid values provided to validate filter method
    '''
    filters_dict: dict = {
        'field': 'field1',
        'operator': 'operator1',
        'value': 'value1',
        'name': 'name1',
        'control': {
            'regex': 'test',
            'operators': ['operator1', 'operator2', 'operator3'],
            'list': ['value2', 'value3', 'value4']
        }
    }
    with pytest.raises(ValidationError) as validation_error:
        base_filter_schema = BaseFilterSchema()

        base_filter_schema.populate_filters(api, path='', filters=[filters_dict], force=True)
        base_filter_schema.validate_filter(name=filters_dict['name'], operator=filters_dict['operator'],
                                           value=filters_dict['value'])
    assert '"value1" must be one of [\'value2\', \'value3\', \'value4\']' in \
           validation_error.value.messages['value'][0], \
        "Invalid choice validation error not raised for 'value' parameter"
    assert '"value1" does not match pattern test' in validation_error.value.messages['value'][1], \
        "'Value' is not matched the regex pattern error is not raised by test-case."


@responses.activate
def test_validate_filter_name_validation_error(api):
    '''
    Test to raise exception when invalid field name provided to validate filter method
    '''
    filters_dict: dict = {
        'field': 'field1',
        'operator': 'operator1',
        'value': 'value4',
        'name': 'name1',
        'control': {
            'regex': 'test' or None,
            'operators': ['operator1', 'operator2', 'operator3'],
            'list': ['value1', 'value2', 'value3'] or None
        }
    }
    with pytest.raises(ValidationError) as validation_error:
        base_filter_schema = BaseFilterSchema()

        base_filter_schema.populate_filters(api, path='', filters=[filters_dict], force=True)
        base_filter_schema.validate_filter(name=filters_dict['field'], operator=filters_dict['operator'],
                                           value=filters_dict['value'])
    assert '"field1" is not a valid filter' in validation_error.value.messages['name'], \
        "Invalid type validation error for name parameter is not raised by test-case."
