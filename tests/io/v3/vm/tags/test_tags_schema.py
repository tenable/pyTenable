'''
Test cases for the tags API schemas
'''
import responses

from tenable.io.v3.vm.tags.schema import (AssetTagSchema, TagCategorySchema,
                                          TagValueSchema)

ASSET_TAG_FILTER_ENDPOINT = 'https://cloud.tenable.com/api/v3/definitions'


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
    schema = TagCategorySchema()
    assert payload == schema.dump(schema.load(payload))


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
    schema = AssetTagSchema()
    assert payload == schema.dump(schema.load(payload))


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

    schema = TagValueSchema()
    assert output_payload == schema.dump(schema.load(input_payload))
