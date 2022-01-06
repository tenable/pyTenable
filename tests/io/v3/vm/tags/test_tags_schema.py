'''
Testing the Tags schemas
'''
from tenable.io.v3.vm.tags import schema as s


def test_tag_category_schema():
    '''
    Test for tag category schema
    '''
    name: str = 'New York'
    description: str = 'Tag category for new york'
    payload = {
        'name': name,
        'description': description
    }
    test_resp = {
        'name': name,
        'description': description
    }
    schema = s.TagCategorySchema()
    assert test_resp == schema.dump(schema.load(payload))


def test_asset_tag_schema():
    '''
    Test for create category schema
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
    schema = s.AssetTagSchema()
    assert payload == schema.dump(schema.load(payload))


def test_tag_value_schema_with_only_values():
    '''
        Test for tag value schema for only values ids
        '''
    payload = {
        'values': [
            'bd55c970-6e10-11ec-90d6-0242ac120003',
            'bd55cd1c-6e10-11ec-90d6-0242ac120003',
            'bd55b656-6e10-11ec-90d6-0242ac120003'
        ]
    }
    schema = s.TagValueSchema(only=['value_id'])
    assert payload == schema.dump(schema.load(payload))


def test_tag_value_schema_with_only_filtertype():
    '''
    Test for tag value schema for only filter type
    '''
    payload = {
        'filter_type': 'and'
    }
    schema = s.TagValueSchema(only=['filter_type'])
    assert payload == schema.dump(schema.load(payload))


def test_tag_value_schema():
    '''
    Test for tag value schema
    '''
    payload = {
        'category_name': 'Location',
        'access_control': {
            'current_user_permissions': [
                'ALL',
                'CAN_EDIT',
                'CAN_SET_PERMISSIONS'
            ],
            'all_users_permissions': [
                'CAN_EDIT'
            ],
            'current_domain_permissions': [
                {
                    'permissions': [
                        'CAN_EDIT'
                    ],
                    'type': 'USER',
                    'id': 'c2f2d080-ac2b-4278-914b-29f148682ee1',
                    'name': 'user@company.com'
                },
                {
                    'permissions': [
                        'CAN_EDIT'
                    ],
                    'type': 'USER',
                    'id': 'c2f2d080-ac2b-4278-914b-29f148682ee1',
                    'name': 'user@company.com'
                }
            ]
        },
        'filters': {
            'asset': {
                'and': [
                    {
                        'field': 'tag.sample category 1',
                        'operator': 'set-has',
                        'value': 'dfgsgf'
                    }
                ]
            }
        },
        'filter_type': 'and',
        'value': 'Washington 34'
    }
    schema = s.TagValueSchema()
    assert payload == schema.dump(schema.load(payload))
