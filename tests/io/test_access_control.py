"""
This file contains tests for the Access Control endpoints.
"""

import string
import uuid
from random import choices

import responses

from tenable.io import TenableIO


@responses.activate
def test_details(tvm: TenableIO):
    responses.add(
        responses.GET,
        'https://nourl/api/v3/access-control/permissions/4c931fce-699c-4052-a43c-c953e71dd37b',
        json={
            'permission_uuid': '4c931fce-699c-4052-a43c-c953e71dd37b',
            'name': 'AG-tag-retesing:1 - Default Permissions',
            'subjects': [
                {
                    'type': 'UserGroup',
                    'uuid': '00000000-0000-0000-0000-000000000000',
                    'name': 'All Users',
                },
                {
                    'type': 'User',
                    'uuid': 'ec466b2b-0e76-4ce6-9e54-7db8552655a6',
                    'name': 'kandarp_test1@tenable.com',
                },
            ],
            'actions': ['CanUse', 'CanEdit'],
            'objects': [
                {
                    'type': 'Tag',
                    'uuid': '55ba39c1-9498-4090-b81a-e17b3a0ccbcb',
                    'name': 'AG-tag-retesing:1',
                }
            ],
            'created_at': 1643389648056,
            'created_by': 'SYSTEM',
            'updated_at': 1662708497394,
            'updated_by': 'admin_a@sandbox.a.io',
        },
    )
    uuid_to_search = '4c931fce-699c-4052-a43c-c953e71dd37b'
    details = tvm.access_control.details(uuid_to_search)
    assert isinstance(details, dict)
    assert details['permission_uuid'] == uuid_to_search


@responses.activate
def test_get_user_permission(tvm: TenableIO):
    responses.add(
        responses.GET,
        'https://nourl/api/v3/access-control/permissions/users/b83faeec-f790-433f-893c-88c48c82562e',
        json={
            'permissions_available': [
                {
                    'permission_uuid': '2ac52c69-e4cc-4252-be33-077a52f6e29d',
                    'name': 'ytest Tag Category:ytest_tag - [CanUse, CanEdit]',
                    'created_at': 1643389638871,
                    'created_by': 'SYSTEM',
                    'updated_at': 1648535223467,
                    'updated_by': 'admin_a@sandbox.a.io',
                }
            ]
        },
    )
    user_uuid_to_search = 'b83faeec-f790-433f-893c-88c48c82562e'
    user_permission = tvm.access_control.get_user_permission(user_uuid_to_search)
    assert isinstance(user_permission, dict)
    assert len(user_permission['permissions_available']) > 0


@responses.activate
def test_get_user_group_permission(tvm: TenableIO):
    responses.add(
        responses.GET,
        'https://nourl/api/v3/access-control/permissions/user-groups/00000000-0000-0000-0000-000000000000',
        json={
            'permissions_available': [
                {
                    'permission_uuid': '00e3ae10-804a-466e-9f3f-628d9bec888b',
                    'name': 'Microsoft Windows 7 Professional Service Pack 1-252.47.38.159:Microsoft Windows 7 Professional Service Pack 1-252.47.38.159 - [CanUse, CanEdit]',
                    'created_at': 1643389583432,
                    'created_by': 'SYSTEM',
                    'updated_at': 1648535219157,
                    'updated_by': 'admin_a@sandbox.a.io',
                }
            ]
        },
    )
    group_uuid_to_search = '00000000-0000-0000-0000-000000000000'
    user_group_permission = tvm.access_control.get_user_group_permission(
        group_uuid_to_search
    )
    assert isinstance(user_group_permission, dict)
    assert len(user_group_permission['permissions_available']) > 0


@responses.activate
def test_get_current_user_permission(tvm: TenableIO):
    responses.add(
        responses.GET,
        'https://nourl/api/v3/access-control/permissions/users/me',
        json={
            'permissions_available': [],
            'permissions_granted': [
                {
                    'permission_uuid': '00e3ae10-804a-466e-9f3f-628d9bec888b',
                    'name': 'Microsoft Windows 7 Professional Service Pack 1-252.47.38.159:Microsoft Windows 7 Professional Service Pack 1-252.47.38.159 - [CanUse, CanEdit]',
                    'subjects': [
                        {
                            'type': 'User',
                            'uuid': 'b83faeec-f790-433f-893c-88c48c82562e',
                            'name': 'admin_a@sandbox.a.io',
                        }
                    ],
                    'actions': ['CanUse', 'CanEdit'],
                    'objects': [
                        {
                            'type': 'Tag',
                            'uuid': '3ae41835-9d92-443f-953a-606950a1cb10',
                            'name': 'Microsoft Windows 7 Professional Service Pack 1-252.47.38.159:Microsoft Windows 7 Professional Service Pack 1-252.47.38.159',
                        }
                    ],
                    'created_at': 1643389583432,
                    'created_by': 'SYSTEM',
                    'updated_at': 1648535219157,
                    'updated_by': 'admin_a@sandbox.a.io',
                }
            ],
        },
    )
    current_user_permission = tvm.access_control.get_current_user_permission()
    assert isinstance(current_user_permission, dict)


@responses.activate
def test_create_and_delete(tvm: TenableIO):
    # Testing creation of permission
    responses.add(
        responses.POST,
        'https://nourl/api/v3/access-control/permissions',
        json={
            'permission_uuid': '52b63814-810f-4012-a023-8d29913d3cc1',
            'name': 'test_lIWbd',
            'subjects': [
                {
                    'type': 'User',
                    'uuid': 'b83faeec-f790-433f-893c-88c48c82562e',
                    'name': 'admin_a@sandbox.a.io',
                }
            ],
            'actions': ['CanView', 'CanUse'],
            'objects': [
                {
                    'type': 'Tag',
                    'uuid': '3c30dc7d-7bd5-458b-a2e1-f74207f8e2ed',
                    'name': 'Category:dummy_value',
                }
            ],
            'created_at': 1663229046424,
            'created_by': 'admin_a@sandbox.a.io',
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/api/v3/access-control/permissions/52b63814-810f-4012-a023-8d29913d3cc1',
        json={
            'permission_uuid': '52b63814-810f-4012-a023-8d29913d3cc1',
            'name': 'test_lIWbd',
            'subjects': [
                {
                    'type': 'User',
                    'uuid': 'b83faeec-f790-433f-893c-88c48c82562e',
                    'name': 'admin_a@sandbox.a.io',
                }
            ],
            'actions': ['CanView', 'CanUse'],
            'objects': [
                {
                    'type': 'Tag',
                    'uuid': '3c30dc7d-7bd5-458b-a2e1-f74207f8e2ed',
                    'name': 'Category:dummy_value',
                }
            ],
            'created_at': 1663229046424,
            'created_by': 'admin_a@sandbox.a.io',
        },
    )
    created_permission = _create_permission(tvm)
    assert isinstance(created_permission, dict)

    created_permission_uuid = created_permission['permission_uuid']
    assert isinstance(created_permission_uuid, str)

    # Testing Deletion of the permission
    deleted_permission = _delete_permission(tvm, created_permission_uuid)
    assert deleted_permission['permission_uuid'] == created_permission_uuid


@responses.activate
def test_update(tvm: TenableIO):
    # Creation permission only to update it later
    responses.add(
        responses.POST,
        'https://nourl/api/v3/access-control/permissions',
        json={
            'permission_uuid': '79259141-f7fc-47f3-b7ad-23ac1fa3b132',
            'name': 'test_eRAsM',
            'subjects': [
                {
                    'type': 'User',
                    'uuid': 'b83faeec-f790-433f-893c-88c48c82562e',
                    'name': 'admin_a@sandbox.a.io',
                }
            ],
            'actions': ['CanView', 'CanUse'],
            'objects': [
                {
                    'type': 'Tag',
                    'uuid': '58a6976a-106a-4d85-b8ca-031acb8808d8',
                    'name': 'Category:dummy_value',
                }
            ],
            'created_at': 1663229048509,
            'created_by': 'admin_a@sandbox.a.io',
        },
    )
    responses.add(
        responses.PUT,
        'https://nourl/api/v3/access-control/permissions/79259141-f7fc-47f3-b7ad-23ac1fa3b132',
    )
    responses.add(
        responses.GET,
        'https://nourl/api/v3/access-control/permissions/79259141-f7fc-47f3-b7ad-23ac1fa3b132',
        json={
            'permission_uuid': '79259141-f7fc-47f3-b7ad-23ac1fa3b132',
            'name': 'test_IBtpt',
            'subjects': [
                {
                    'type': 'User',
                    'uuid': 'b83faeec-f790-433f-893c-88c48c82562e',
                    'name': 'admin_a@sandbox.a.io',
                }
            ],
            'actions': ['CanView'],
            'objects': [
                {
                    'type': 'Tag',
                    'uuid': '79259141-f7fc-47f3-b7ad-23ac1fa3b132',
                    'name': 'Category:dummy_value',
                }
            ],
            'created_at': 1663229048509,
            'created_by': 'admin_a@sandbox.a.io',
            'updated_at': 1663229049777,
            'updated_by': 'admin_a@sandbox.a.io',
        },
    )
    created_permission_uuid = _create_permission(tvm)['permission_uuid']
    updated_permission = _update_permission(tvm, created_permission_uuid)
    assert updated_permission is None

    # Cleaning up after test
    _delete_permission(tvm, created_permission_uuid)


@responses.activate
def test_list(tvm: TenableIO):
    responses.add(
        responses.GET,
        'https://nourl/api/v3/access-control/permissions',
        json={
            'permissions': [
                {
                    'permission_uuid': '00000000-0000-0000-0000-000000000000',
                    'name': 'Administrators',
                    'subjects': [{'type': 'AllAdmins'}],
                    'actions': ['CanScan', 'CanView', 'CanEdit'],
                    'objects': [{'type': 'AllObjects'}],
                }
            ]
        },
    )
    permissions = tvm.access_control.list()
    assert isinstance(permissions, list)


def _create_permission(tvm: TenableIO):
    """
    Invokes the creation API for testing.
    """
    permission = {
        'actions': ['CanView', 'CanUse'],
        'objects': [
            {
                'name': 'Category,dummy_value',
                'type': 'Tag',
                'uuid': f'{str(uuid.uuid4())}',
            }
        ],
        'subjects': [
            {
                'name': 'User sub',
                'type': 'User',
                'uuid': 'b83faeec-f790-433f-893c-88c48c82562e',
            }
        ],
        'name': f'test_{_random_string(5)}',
    }
    created_permission = tvm.access_control.create(permission)
    return created_permission


def _delete_permission(tvm: TenableIO, permission_uuid: str):
    """
    Invokes the deletion API for testing.
    """
    return tvm.access_control.details(permission_uuid)


def _update_permission(tvm: TenableIO, permission_uuid: str):
    """
    Invokes the update API for testing.
    """
    permission_to_update = {
        'actions': ['CanView'],
        'objects': [
            {'name': 'Category,dummy_value', 'type': 'Tag', 'uuid': permission_uuid}
        ],
        'subjects': [
            {
                'name': 'User sub',
                'type': 'User',
                'uuid': 'b83faeec-f790-433f-893c-88c48c82562e',
            }
        ],
        'name': f'test_{_random_string(5)}',
    }
    return tvm.access_control.update(permission_uuid, permission_to_update)


def _random_string(length: int):
    """
    Creates a random string of a given length
    Args:
        length: Length of the string to be generated

    Returns: str

    """
    return ''.join(choices(string.ascii_letters, k=length))
