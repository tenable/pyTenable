from tenable.base.schemas.filters import BaseFilterRuleSchema
from marshmallow import ValidationError, validate
import pytest


def test_input():
    '''
    Test the tuple conversion and filter ingestion.
    '''
    schema = BaseFilterRuleSchema()
    resp = schema.load(
        [
            ('test1', 'eq', 'value'),
            ('test2', 'eq', 'something'),
            {'name': 'test3', 'oper': 'eq', 'value': 'else'},
        ],
        many=True
    )
    expected = [
        {'name': 'test1', 'oper': 'eq', 'value': 'value'},
        {'name': 'test2', 'oper': 'eq', 'value': 'something'},
        {'name': 'test3', 'oper': 'eq', 'value': 'else'}
    ]
    assert resp == expected


@pytest.fixture
def filters():
    return {
        'example1': {'pattern': None, 'operators': None, 'choices': None},
        'example2': {'pattern': '\\d+'},
        'example3': {'operators': ['eq']},
        'example4': {'choices': ['one', 'two']}
    }


def test_filter_loader(filters):
    '''
    Test the load_filters method
    '''
    schema = BaseFilterRuleSchema()
    schema.load_filters(filters)
    assert schema.filters == filters


def test_filter_getter(filters):
    '''
    Test the get_filter method
    '''
    schema = BaseFilterRuleSchema()
    schema.load_filters(filters)
    f = schema.get_filter('example4')
    assert isinstance(f.get('choices'), validate.OneOf)


def test_filtering(filters):
    '''
    Test the filtering capabilities of the base schema.
    '''
    schema = BaseFilterRuleSchema()
    schema.load_filters(filters)
    resp = schema.load(
        [
            ('example1', 'eq', '1'),
            ('example2', 'eq', '1234'),
            ('example3', 'eq', 'something'),
            ('example4', 'eq', 'one')
        ],
        many=True
    )

    # bad pattern match
    with pytest.raises(ValidationError):
        schema.load(('example2', 'eq', 'one'))

    # bad operator
    with pytest.raises(ValidationError):
        schema.load(('example3', 'gt', 'something'))

    # invalid choice
    with pytest.raises(ValidationError):
        schema.load(('example4', 'eq', 'three'))

    # invalid filter
    with pytest.raises(ValidationError):
        schema.load(('example5', 'eq', 'one'))