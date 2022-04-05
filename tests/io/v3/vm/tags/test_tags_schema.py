'''
Test cases for the tags API schemas
'''
import pytest
import responses
from marshmallow import ValidationError

from tenable.io.v3.vm.tags.schema import (AccessControlSchema, AssetTagSchema,
                                          CurrentDomainPermissionSchema,
                                          TagCategorySchema, TagsFilterSchema,
                                          TagValueSchema)
from tests.io.v3.vm.tags.objects import (NEGATIVE_ACCESS_CONTROL_SCHEMA,
                                         NEGATIVE_ASSET_TAG_SCHEMA,
                                         NEGATIVE_CURRENT_DOMAIN_PERMISSION,
                                         NEGATIVE_TAG_VALUE_SCHEMA,
                                         NEGATIVE_TAGS_CATEGORY_SCHEMA,
                                         NEGATIVE_TAGS_FILTER_SCHEMA)

ASSET_TAG_FILTER_ENDPOINT = 'https://cloud.tenable.com/api/v3/definitions'
tag_category_schema = TagCategorySchema()
asset_tag_schema = AssetTagSchema()
current_domain_permission_schema = CurrentDomainPermissionSchema()
access_control_schema = AccessControlSchema()
tag_value_schema = TagValueSchema()
tags_filter_schema = TagsFilterSchema()


def test_tag_category_schema():
    '''
    Test case for tag category schema
    '''
    name: str = 'New York'
    description: str = 'Tag category for new york'
    payload = {
        'name': name,
        'description': description
    }
    assert payload == tag_category_schema.dump(
        tag_category_schema.load(payload)
    )


def test_asset_tag_schema():
    '''
    Test case for asset tag schema
    '''
    payload = {
        'action': 'add',
        'assets': [
            'f7aa967e-6e0f-11ec-90d6-0242ac120003',
            'f7aa98f4-6e0f-11ec-90d6-0242ac120003'
        ],
        'tags': [
            'f7aa9ce6-6e0f-11ec-90d6-0242ac120003',
            'f7aa9e26-6e0f-11ec-90d6-0242ac120003'
        ]
    }
    assert payload == asset_tag_schema.dump(asset_tag_schema.load(payload))


@responses.activate
def test_tag_value_schema():
    '''
    Test case for tag value schema
    '''
    category_name: str = 'Category_1'
    category_description: str = 'Description for category'
    value: str = 'Value_1'
    description: str = 'Description for Value'
    current_user_permissions: list = ['ALL', 'CAN_EDIT', 'CAN_SET_PERMISSIONS']
    all_users_permissions: list = ['CAN_EDIT']
    current_domain_permissions: list = [
        {
            'id': 'c2f2d080-ac2b-4278-914b-29f148682ee1',
            'name': 'user@company.com',
            'type': 'USER',
            'permissions': [
                'CAN_EDIT'
            ]
        }
    ]
    filter_type: str = 'or'
    filters: list = [('field_1', 'oper_1', ['value_1'])]

    input_payload: dict = {
        'category_name': category_name,
        'category_description': category_description,
        'value': value,
        'description': description,
        'access_control': {
            'current_user_permissions': current_user_permissions,
            'all_users_permissions': all_users_permissions,
            'current_domain_permissions':
                current_domain_permissions,
        },
        'filter_type': filter_type,
        'filters': filters
    }

    output_payload: dict = {
        'category_name': category_name,
        'category_description': category_description,
        'value': value,
        'description': description,
        'filters': {
            'asset': {
                filter_type: [
                    {
                        'operator': 'oper_1',
                        'field': 'field_1',
                        'value': [
                            'value_1'
                        ]
                    }
                ]
            }
        },
        'access_control': {
            'current_user_permissions': current_user_permissions,
            'current_domain_permissions': current_domain_permissions,
            'all_users_permissions': all_users_permissions
        },
    }

    # Let's register the response for asset tag filter endpoint
    responses.add(
        responses.GET,
        f'{ASSET_TAG_FILTER_ENDPOINT}/tags/assets/filters',
        json={
            'field_1': {
                'operators': ['oper_1', 'oper_2'],
                'choices': None,
                'pattern': '.*'
            }
        }
    )

    assert output_payload == tag_value_schema.dump(
        tag_value_schema.load(input_payload)
    )

# Negative test cases


@pytest.mark.parametrize("test_input", NEGATIVE_TAGS_CATEGORY_SCHEMA)
def test_tags_category_negative(test_input):
    with pytest.raises(ValidationError):
        tag_category_schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_ASSET_TAG_SCHEMA)
def test_asset_tag_negative(test_input):
    with pytest.raises(ValidationError):
        asset_tag_schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_CURRENT_DOMAIN_PERMISSION)
def test_current_domain_permission_negative(test_input):
    with pytest.raises(ValidationError):
        current_domain_permission_schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_ACCESS_CONTROL_SCHEMA)
def test_access_control_negative(test_input):
    with pytest.raises(ValidationError):
        access_control_schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_TAGS_FILTER_SCHEMA)
def test_tags_filter_negative(test_input):
    with pytest.raises(ValidationError):
        tags_filter_schema.load(test_input)


@pytest.mark.parametrize("test_input", NEGATIVE_TAG_VALUE_SCHEMA)
def test_tag_value_negative(test_input):
    with pytest.raises(ValidationError):
        tag_value_schema.load(test_input)
