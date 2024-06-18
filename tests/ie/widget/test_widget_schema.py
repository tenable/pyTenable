'''test widget schema'''
import pytest
from marshmallow.exceptions import ValidationError

from tenable.ie.widget.schema import WidgetSchema, WidgetOptionSchema


@pytest.fixture
def widget_schema():
    return {
        'posX': 11,
        'posY': 12,
        'width': 21,
        'height': 22,
        'title': 'test_widget'
    }


@pytest.fixture
def widget_options_schema():
    return {'type': 'BigNumber',
            'series': [
                {
                    'dataOptions': {
                        'duration': 10,
                        'interval': '10',
                        'directoryIds': [1, 2, 3],
                        'active': True
                    },
                    'displayOptions': {
                        'label': 'User'
                    }
                }
            ]
            }


def test_widget_schema(widget_schema):
    '''
    tests the widget schema
    '''
    test_response = {'dashboardId': '1',
                     'height': 22,
                     'id': 1,
                     'posX': 11,
                     'posY': 12,
                     'title': 'test_widget',
                     'width': 21
                     }
    schema = WidgetSchema()
    assert test_response['title'] == schema.dump(schema.load(widget_schema))['title']
    with pytest.raises(ValidationError):
        widget_schema['new_val'] = 'something'
        schema.load(widget_schema)


def test_widget_option_schema(widget_options_schema):
    '''
    tests the widget options schema
    '''
    test_response = {'series': [{'data_options': {'active': True,
                                                  'directory_ids': [1, 2, 3],
                                                  'duration': 10,
                                                  'interval': '10'},
                                 'display_options': {'label': 'User'}}],
                     'type': 'BigNumber'}
    schema = WidgetOptionSchema()
    assert test_response['type'] == schema.dump(schema.load(widget_options_schema))['type']
    with pytest.raises(ValidationError):
        widget_options_schema['new_val'] = 'something'
        schema.load(widget_options_schema)
