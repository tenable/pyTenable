"""
This file contains tests for the Access Control endpoints.
"""
import os
import string
import uuid
from random import choices

import pytest

from tenable.io import TenableIO
from tests.pytenable_log_handler import setup_logging_to_file


@pytest.fixture
def api():
    """
    Fixture for setting up API Keys
    """
    setup_logging_to_file()
    return TenableIO(
        os.getenv('TIO_TEST_ADMIN_ACCESS', ''),
        os.getenv('TIO_TEST_ADMIN_SECRET', ''),
        vendor='pytest',
        product='pytenable-automated-testing')


def test_details(api: TenableIO):
    uuid_to_search = "4c931fce-699c-4052-a43c-c953e71dd37b"
    details = api.v3.access_control.details(uuid_to_search)
    assert isinstance(details, dict)
    assert details["permission_uuid"] == uuid_to_search


def test_get_user_permission(api: TenableIO):
    user_uuid_to_search = "b83faeec-f790-433f-893c-88c48c82562e"
    user_permission = api.v3.access_control.get_user_permission(user_uuid_to_search)
    assert isinstance(user_permission, dict)
    assert len(user_permission["permissions_available"]) > 0


def test_get_user_group_permission(api: TenableIO):
    group_uuid_to_search = "00000000-0000-0000-0000-000000000000"
    user_group_permission = api.v3.access_control.get_user_group_permission(group_uuid_to_search)
    assert isinstance(user_group_permission, dict)
    assert len(user_group_permission["permissions_available"]) > 0


def test_get_current_user_permission(api: TenableIO):
    current_user_permission = api.v3.access_control.get_current_user_permission()
    assert isinstance(current_user_permission, dict)


def test_create_and_delete(api: TenableIO):
    # Testing creation of permission
    created_permission = _create_permission(api)
    assert isinstance(created_permission, dict)

    created_permission_uuid = created_permission["permission_uuid"]
    print("CREATED: " + created_permission_uuid)
    assert isinstance(created_permission_uuid, str)

    # Testing Deletion of the permission
    deleted_permission = _delete_permission(api, created_permission_uuid)
    assert deleted_permission["permission_uuid"] == created_permission_uuid


def test_update(api: TenableIO):
    # Creation permission only to update it later
    created_permission_uuid = _create_permission(api)["permission_uuid"]
    updated_permission = _update_permission(api, created_permission_uuid)
    print(updated_permission)
    assert updated_permission["status"] == "success"
    assert updated_permission["permission_uuid"] == created_permission_uuid

    # Cleaning up after test
    _delete_permission(api, created_permission_uuid)


@pytest.mark.vcr()
def test_list(api: TenableIO):
    permissions = api.v3.access_control.list()
    for p in permissions:
        print(p)
    assert isinstance(permissions, list)


def _create_permission(api: TenableIO):
    permission = {
        "actions": ["CanView", "CanUse"],
        "objects": [
            {
                "name": "Category,dummy_value",
                "type": "Tag",
                "uuid": f"{str(uuid.uuid4())}"
            }
        ],
        "subjects": [
            {
                "name": "User sub",
                "type": "User",
                "uuid": "b83faeec-f790-433f-893c-88c48c82562e"
            }
        ],
        "name": f"test_{_random_string(5)}"
    }
    created_permission = api.v3.access_control.create(permission)
    return created_permission


def _delete_permission(api: TenableIO, permission_uuid: str):
    return api.v3.access_control.details(permission_uuid)


def _update_permission(api: TenableIO, permission_uuid: str):
    permission_to_update = {
        "actions": ["CanView"],
        "objects": [
            {
                "name": "Category,dummy_value",
                "type": "Tag",
                "uuid": permission_uuid
            }
        ],
        "subjects": [
            {
                "name": "User sub",
                "type": "User",
                "uuid": "b83faeec-f790-433f-893c-88c48c82562e"
            }
        ],
        "name": f"test_{_random_string(5)}"
    }
    return api.v3.access_control.update(permission_uuid, permission_to_update)


def _random_string(length: int):
    return "".join(choices(string.ascii_letters, k=length))
