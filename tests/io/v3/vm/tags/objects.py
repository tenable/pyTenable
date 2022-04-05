NEGATIVE_TAGS_CATEGORY_SCHEMA = [
    {'invalid': 'key'},
    {'description': 'Negative case'},
    {'name': 11},
    {'name': ''},
    {'name': 'a' * 128},
    {
        'name': 'Category',
        'description': 123
    }
]

NEGATIVE_ASSET_TAG_SCHEMA = [
    {'invalid': 'key'},
    {'action': 1},
    {'assets': {'not_a_list'}},
    {'assets': ['not_uuid']},
    {'assets': 1},
    {'tags': {'not_a_list'}},
    {'tags': ['not_uuid']},
    {'tags': 1}
]

NEGATIVE_CURRENT_DOMAIN_PERMISSION = [
    {'invalid': 'key'},
    {
        'name': 'abc',
        'type': 'USER',
        'permissions': ['ALL']
    },
    {
        'id': 'invalid_uuid',
        'name': 'abc',
        'type': 'USER',
        'permissions': ['ALL']
    },
    {
        'id': 111,
        'name': 'abc',
        'type': 'USER',
        'permissions': ['ALL']
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'type': 'USER',
        'permissions': ['ALL']
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 111,
        'type': 'USER',
        'permissions': ['ALL']
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 'abc',
        'permissions': ['ALL']
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 'abc',
        'type': 'INVALID',
        'permissions': ['ALL']
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 'abc',
        'type': 123,
        'permissions': ['ALL']
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 'abc',
        'type': 'USER'
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 'abc',
        'type': 'USER',
        'permissions': {}
    },
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 'abc',
        'type': 'USER',
        'permissions': ['ALL', 'INVALID']
    },
    # Testing pre-load
    (
        'c74f05b6-d83a-413d-97c2-c54beed0fc91', 'abc', 'USER'
    ),
    (
        'c74f05b6-d83a-413d-97c2-c54beed0fc91', 'abc', 'USER', 'ALL', 'invalid'
    ),
    {
        'id': 'c74f05b6-d83a-413d-97c2-c54beed0fc91',
        'name': 'abc',
        'type': 'USER',
        'permissions': ['ALL', 'INVALID'],
        'invalid': 'key'
    }
]

NEGATIVE_ACCESS_CONTROL_SCHEMA = [
    {'invalid': 'key'},
    {'current_user_permissions': {}},
    {'current_user_permissions': ['ALL', 'INVALID']},
    {'all_users_permissions': {}},
    {'all_users_permissions': ['ALL', 'INVALID']},
    {'current_domain_permissions': {}},
    {'current_domain_permissions': [{'key': 'value'}]},
    {'defined_domain_permissions': {}},
    {'defined_domain_permissions': ['ALL', 'INVALID']},
    {'version': 'string'}
]

NEGATIVE_TAGS_FILTER_SCHEMA = [
    {'invalid': 'key'},
]

NEGATIVE_TAG_VALUE_SCHEMA = [
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'values': {},
        'value': 'value'
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'values': ['invalid_uuid'],
        'value': 'value'
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'category_uuid': 'invalid_uuid',
        'value': 'value'
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'category_name': 123214,
        'value': 'value'
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'category_description': 1234,
        'value': 'value'
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'category_uuid': 'invalid_uuid',
        'value': 'value'
    },
    {
        'category_uuid': 'ff90b353-8347-4d10-8da9-f961d6fd0d39',
        'access_control': {'current_user_permissions': ['ALL']}
    },
    {
        'category_uuid': 'ff90b353-8347-4d10-8da9-f961d6fd0d39',
        'values': 'missing access control'
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'value': 'value',
        'filter_type': 123
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'value': 'value',
        'filter_type': 'invalid'
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'value': 'value',
        'filters': {}
    },
    {
        'access_control': {'current_user_permissions': ['ALL']},
        'value': 'value',
        'filters': [{'invalid': 'key'}]
    },
    {'invalid': 'key'}
]
