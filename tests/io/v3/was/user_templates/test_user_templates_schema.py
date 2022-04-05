'''
Test User Template Schema
'''
from tenable.io.v3.was.user_templates.schema import (PermissionSchema,
                                                     UserTemplateSchema)

permission_obj = {
    'entity': 'user',
    'entity_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    'permissions_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    'level': 'no_access',
}

user_template_obj = {
    'name': 'Edited template name',
    'default_permissions': 'no_access',
    'permissions': [permission_obj],
    'description': 'edited description',
    'owner_id': 'a8ff6f60-a7e0-43a5-a9d4-0bd079e1d9fa',
    'results_visibility': 'private'
}


def test_user_template_schema():
    '''
    Test user template schema
    '''
    schema = UserTemplateSchema()
    assert user_template_obj == schema.dump(schema.load(user_template_obj))


def test_permission_schema():
    '''
    Test permission schema
    '''
    schema = PermissionSchema()
    assert permission_obj == schema.dump(schema.load(permission_obj))
