"""
This file contains tests for the Access Control endpoints.
"""
import os

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
    details = api.v3.access_control.details("4c931fce-699c-4052-a43c-c953e71dd37b")
    print(details)
    assert isinstance(details, dict)


def test_get_user_permission(api: TenableIO):
    user_permission = api.v3.access_control.get_user_permission("b83faeec-f790-433f-893c-88c48c82562e")
    print(user_permission)
    assert isinstance(user_permission, dict)


def test_get_user_group_permission(api: TenableIO):
    user_group_permission = api.v3.access_control.get_user_group_permission("00000000-0000-0000-0000-000000000000")
    print(user_group_permission)
    assert isinstance(user_group_permission, dict)


def test_get_current_user_permission(api: TenableIO):
    current_user_permission = api.v3.access_control.get_current_user_permission()
    print(current_user_permission)
    assert isinstance(current_user_permission, dict)


def test_delete(api: TenableIO):
    pass


def test_create(api: TenableIO):
    permission = {
        "actions": ["CanView", "CanUse"],
        "objects": [
            {
                "name": "Category,dummyvalue",
                "type": "Tag",
                "uuid": "7a8b02a0-3367-11ed-a261-0242ac120099"
            }
        ],
        "subjects": [
            {
                "name": "User sub",
                "type": "User",
                "uuid": "b83faeec-f790-433f-893c-88c48c82562e"
            }
        ],
        "name": "dummy name1"
    }
    created_permission = api.v3.access_control.create(permission)
    assert isinstance(created_permission, dict)
    assert isinstance(created_permission["permission_uuid"], str)
    print(created_permission)


def test_update(api: TenableIO):
    pass


@pytest.mark.vcr()
def test_list(api: TenableIO):
    permissions = api.v3.access_control.list()
    for p in permissions:
        print(p)
    assert isinstance(permissions, list)
