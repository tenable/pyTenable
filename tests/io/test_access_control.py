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


@pytest.mark.vcr()
def test_details(api: TenableIO):
    uuid_to_search = "4c931fce-699c-4052-a43c-c953e71dd37b"
    details = api.access_control.details(uuid_to_search)
    assert isinstance(details, dict)
    assert details["permission_uuid"] == uuid_to_search


@pytest.mark.vcr()
def test_get_user_permission(api: TenableIO):
    user_uuid_to_search = "b83faeec-f790-433f-893c-88c48c82562e"
    user_permission = api.access_control.get_user_permission(user_uuid_to_search)
    assert isinstance(user_permission, dict)
    assert len(user_permission["permissions_available"]) > 0


@pytest.mark.vcr()
def test_get_user_group_permission(api: TenableIO):
    group_uuid_to_search = "00000000-0000-0000-0000-000000000000"
    user_group_permission = api.access_control.get_user_group_permission(group_uuid_to_search)
    assert isinstance(user_group_permission, dict)
    assert len(user_group_permission["permissions_available"]) > 0


@pytest.mark.vcr()
def test_get_current_user_permission(api: TenableIO):
    current_user_permission = api.access_control.get_current_user_permission()
    assert isinstance(current_user_permission, dict)


@pytest.mark.vcr()
def test_create_and_delete(api: TenableIO):
    # Testing creation of permission
    created_permission = _create_permission(api)
    assert isinstance(created_permission, dict)

    created_permission_uuid = created_permission["permission_uuid"]
    assert isinstance(created_permission_uuid, str)

    # Testing Deletion of the permission
    deleted_permission = _delete_permission(api, created_permission_uuid)
    assert deleted_permission["permission_uuid"] == created_permission_uuid


@pytest.mark.vcr()
def test_update(api: TenableIO):
    # Creation permission only to update it later
    created_permission_uuid = _create_permission(api)["permission_uuid"]
    updated_permission = _update_permission(api, created_permission_uuid)
    assert updated_permission is None

    # Cleaning up after test
    _delete_permission(api, created_permission_uuid)


@pytest.mark.vcr()
def test_list(api: TenableIO):
    permissions = api.access_control.list()
    assert isinstance(permissions, list)


def _create_permission(api: TenableIO):
    """
    Invokes the creation API for testing.
    """
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
    created_permission = api.access_control.create(permission)
    return created_permission


def _delete_permission(api: TenableIO, permission_uuid: str):
    """
    Invokes the deletion API for testing.
    """
    return api.access_control.details(permission_uuid)


def _update_permission(api: TenableIO, permission_uuid: str):
    """
    Invokes the update API for testing.
    """
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
    return api.access_control.update(permission_uuid, permission_to_update)


def _random_string(length: int):
    """
    Creates a random string of a given length
    Args:
        length: Length of the string to be generated

    Returns: str

    """
    return "".join(choices(string.ascii_letters, k=length))
