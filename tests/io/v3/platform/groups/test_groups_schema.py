'''
Testing the Platform groups schemas
'''
from tenable.io.v3.platform.groups.schema import PlatformGroupSchema

def test_platform_groups_schema_for_all_fields():
    '''
    Test the platform_groups schema with name, group_id, user_id
    '''
    name: str = 'sample name'
    group_id: str = '00000000-0000-0000-0000-000000000000'
    user_id: str = '00000000-0000-0000-0000-000000000000'

    payload = {
        'name': name,
        'group_id': group_id,
        'user_id': user_id
    }
    test_resp = {
        'name': name,
        'group_id': group_id,
        'user_id': user_id
    }
    schema = PlatformGroupSchema()
    assert test_resp == schema.dump(schema.load(payload))
