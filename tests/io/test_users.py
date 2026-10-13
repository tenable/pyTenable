"""
test users
"""

import uuid

import pytest
import responses
from responses.matchers import query_param_matcher, json_params_matcher

from tenable.errors import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    UnexpectedValueError,
)
from tests.checker import check

USERS = {
    'id': 3344,
    'user_name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
    'username': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
    'email': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
    'name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
    'type': 'local',
    'permissions': 64,
    'login_fail_count': 0,
    'login_fail_total': 0,
    'enabled': True,
    'uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
    'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
    'uuid_id': '88aba081-9505-4e06-9acc-2530b486c8d4',
}

USERS_AUTHORIZATIONS = {
    'account_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
    'user_uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
    'api_permitted': True,
    'password_permitted': True,
    'saml_permitted': True,
}


def guser():
    """
    Returns username
    """
    return '{}@tenable.com'.format(uuid.uuid4())


def gpass():
    """
    Returns password
    """
    return '{}Tt!'.format(uuid.uuid4())


def test_users_create_username_typeerror(tvm):
    """
    test to raise exception when type of username param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.create(False, gpass(), 1)


def test_users_create_password_typeerror(tvm):
    """
    test to raise exception when type of password param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.create(guser(), False, 1)


def test_users_create_permissions_typeerror(tvm):
    """
    test to raise exception when type of permissions param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.create(guser(), gpass(), 'nope')


def test_users_create_name_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.create(guser(), gpass(), 1, name=1)


def test_users_create_email_typeerror(tvm):
    """
    test to raise exception when type of email param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.create(guser(), gpass(), 1, email=1)


def test_users_create_account_type_typeerror(tvm):
    """
    test to raise exception when type of account_type param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.create(guser(), gpass(), 1, account_type=False)


@responses.activate
def test_users_create_permissionserror(tvm):
    """
    test to raise exception when standard_user tries to create user.
    """
    responses.add(
        responses.POST,
        'https://nourl/users',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.create(guser(), gpass(), 16)


@responses.activate
def test_users_create(tvm, user):
    """
    test to create user
    """
    responses.add(responses.POST, 'https://nourl/users', json=user)
    user = tvm.users.create(user['username'], 'Sup3r-s3cret-Tt!', 64)
    assert isinstance(user, dict)
    check(user, 'email', str)
    check(user, 'enabled', bool)
    check(user, 'id', int)
    check(user, 'login_fail_count', int)
    check(user, 'login_fail_total', int)
    check(user, 'permissions', int)
    check(user, 'type', str)
    check(user, 'user_name', str)
    check(user, 'username', str)
    check(user, 'uuid_id', 'uuid')


@responses.activate
def test_users_delete_notfounderror(tvm):
    """
    test to raise exception when user_id not found.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/users/0',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.users.delete(0)


@responses.activate
def test_users_delete_permissionerror(tvm, user):
    """
    test to raise exception when standard_user tries to delete user.
    """
    responses.add(
        responses.DELETE,
        'https://nourl/users/3344',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.delete(user['id'])


@responses.activate
def test_users_delete(tvm, user):
    """
    test to delete user
    """
    responses.add(responses.DELETE, 'https://nourl/users/3344')
    responses.add(responses.GET, 'https://nourl/users', json={'users': []})
    tvm.users.delete(user['id'])
    assert user['id'] not in [u['id'] for u in tvm.users.list()]


@responses.activate
def test_users_details_notfounderror(tvm):
    """
    test to raise exception when user_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/0',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.users.details(0)


@responses.activate
def test_users_details(tvm, user):
    """
    test to get user details
    """
    responses.add(responses.GET, 'https://nourl/users/3344', json=USERS)
    resp = tvm.users.details(user['id'])
    assert isinstance(user, dict)
    check(resp, 'email', str)
    check(resp, 'enabled', bool)
    check(resp, 'id', int)
    check(resp, 'login_fail_count', int)
    check(resp, 'login_fail_total', int)
    check(resp, 'permissions', int)
    check(resp, 'type', str)
    check(resp, 'user_name', str)
    check(resp, 'username', str)
    check(resp, 'uuid_id', 'uuid')


def test_users_edit_email_typeerror(tvm):
    """
    test to raise exception when type of email param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.edit(1, email=1)


def test_users_edit_enabled_typeerror(tvm):
    """
    test to raise exception when type of enabled param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.edit(1, enabled='nope')


@responses.activate
def test_users_edit_notfounderror(tvm):
    """
    test to raise exception when user_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/0',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.users.edit(0, email=guser())


@responses.activate
def test_users_edit_permissionerror(tvm, user):
    """
    test to raise exception when standard user try to edit user.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.edit(user['id'], name=str(uuid.uuid4()))


@responses.activate
def test_users_edit(tvm, user):
    """
    test to edit user
    """
    responses.add(responses.GET, 'https://nourl/users/3344', json=USERS)
    responses.add(
        responses.PUT,
        'https://nourl/users/3344',
        json={
            'id': 3344,
            'user_name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'username': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'email': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'name': 'MODDED NAME',
            'type': 'local',
            'whatsnew_version': '',
            'aggregate': True,
            'permissions': 64,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'enabled': True,
            'uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'uuid_id': '88aba081-9505-4e06-9acc-2530b486c8d4',
        },
    )
    resp = tvm.users.edit(user['id'], name='MODDED NAME')
    assert isinstance(user, dict)
    check(resp, 'id', int)
    check(resp, 'username', str)
    check(resp, 'name', str)
    check(resp, 'email', str)
    check(resp, 'permissions', int)
    check(resp, 'type', str)
    check(resp, 'login_fail_count', int)
    check(resp, 'login_fail_total', int)
    check(resp, 'enabled', bool)
    check(resp, 'uuid_id', 'uuid')
    assert resp['name'] == 'MODDED NAME'


def test_users_enabled_enabled_typeerror(tvm):
    """
    test to raise exception when type of enabled param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.enabled(1, 'nope')


@responses.activate
def test_users_enabled_notfounderror(tvm):
    """
    test to raise exception when user provided user_id not found.
    """
    responses.add(
        responses.PUT,
        'https://nourl/users/0/enabled',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.users.enabled(0, False)


@responses.activate
def test_users_enabled_permissionerror(tvm, user):
    """
    test to raise exception when standard user try to disable user.
    """
    responses.add(
        responses.PUT,
        'https://nourl/users/3344/enabled',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.enabled(user['id'], False)


@responses.activate
def test_users_enabled(tvm, user):
    """
    test to disable user
    """
    responses.add(
        responses.PUT,
        'https://nourl/users/3344/enabled',
        json={
            'id': 3344,
            'user_name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'username': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'email': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'type': 'local',
            'whatsnew_version': '',
            'aggregate': True,
            'permissions': 64,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'enabled': False,
            'uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'uuid_id': '88aba081-9505-4e06-9acc-2530b486c8d4',
        },
    )
    disabled = tvm.users.enabled(user['id'], False)
    assert isinstance(disabled, dict)
    assert disabled['enabled'] is False


def test_users_two_factor_email_typeerror(tvm):
    """
    test to raise exception when type of email param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.two_factor(0, False, 'nope')


def test_users_two_factor_sms_typeerror(tvm):
    """
    test to raise exception when type of sms param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.two_factor('nope', False)


def test_users_two_factor_phone_typeerror(tvm):
    """
    test to raise exception when type of phone param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.two_factor(False, False, 8675309)


@responses.activate
def test_users_two_factor(tvm, user):
    """
    test to configure two-factor authorization for a specific user
    """
    responses.add(
        responses.PUT,
        f'https://nourl/users/{user["id"]}/two-factor',
        match=[
            json_params_matcher({'email_enabled': False, 'sms_enabled': False})
        ],
    )
    tvm.users.two_factor(user['id'], False, False)


def test_users_enable_two_factor_phone_typeerror(tvm):
    """
    test to raise exception when type of phone param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.enable_two_factor(False)


@pytest.mark.skip(reason="Don't want to enable two-facor on the user.")
def test_users_enable_two_factor(tvm):
    """
    test to enable two_factor authentication for user.
    """
    tvm.users.enable_two_factor('867-5309')


def test_users_verify_two_factor_code_typeerror(tvm):
    """
    test to raise exception when type of code param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.verify_two_factor(False)


@pytest.mark.skip(reason="Don't want to enable two-factor on the user.")
def test_users_verify_two_factor(tvm):
    """
    test to verify two_factor authentication for user.
    """
    tvm.users.verify_two_factor(False)


def test_users_impersonate_id_typeerror(tvm):
    """
    test to raise exception when type of name param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.impersonate(1)
        tvm.session.restore()


@responses.activate
def test_users_impersonate_notfounderror(tvm):
    """
    test to raise exception when user provided user_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/session',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Forbidden'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.impersonate(guser())
        tvm.session.details()
        tvm.session.restore()


@responses.activate
def test_users_impersonate_permissionerror(tvm, user):
    """
    test to raise exception when standard user try to impersonate user.
    """
    responses.add(
        responses.GET,
        'https://nourl/session',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Forbidden'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.impersonate(user['username'])
        tvm.session.details()
        tvm.session.restore()


@responses.activate
def test_users_impersonate(tvm, user):
    """
    test to impersonate user
    """
    responses.add(
        responses.GET,
        'https://nourl/session',
        json={
            'id': 3344,
            'uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
            'uuid_id': '88aba081-9505-4e06-9acc-2530b486c8d4',
            'username': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'user_name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'email': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'name': '8367483c-769b-4ad3-bc97-922e2d70c992@pytenable.io',
            'type': 'local',
            'permissions': 64,
            'enabled': True,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'container_id': 1215,
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'container_name': 'pyTenable Test Container',
        },
    )
    responses.add(
        responses.GET,
        'https://nourl/session',
        json={
            'id': 3,
            'uuid': 'a09161a2-3860-4ca8-93c8-b3f7be366e50',
            'uuid_id': 'a09161a2-3860-4ca8-93c8-b3f7be366e50',
            'username': 'test_admin@pytenable.io',
            'user_name': 'test_admin@pytenable.io',
            'email': 'noreply@pytenable.test',
            'name': '00bc5450-497e-4047-9f0b-0e2755d7cd2e',
            'type': 'local',
            'permissions': 64,
            'enabled': True,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'container_id': 1215,
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'container_name': 'pyTenable Test Container',
            'features': {
                'access_groups': True,
                'access_groups_migration': True,
                'advanced_search_v2': True,
                'agent_triage_m2': True,
                'agent_updates': True,
                'analytics': True,
                'analytics_v2': True,
                'asset_deleting_ui': True,
                'asset_management': True,
                'audits_workbench': False,
                'aws_connector_v1': True,
                'cfl_core_ssor': False,
                'connectors_gen2': False,
                'container_security': True,
                'container_security_gen2': True,
                'container_security_gen2_runtime': False,
                'credentials_mgmt': True,
                'credentials_mgmt_v2': True,
                'dashboards_gen2': True,
                'dashboards_gen2_blank_canvas': False,
                'dashboards_gen2_export': True,
                'dashboards_gen2_export_png': False,
                'dashboards_gen2_lumin_enabled': False,
                'dashboards_gen2_schedule': True,
                'dashboards_gen2_tag_filter': False,
                'dashboards_gen2_widget_filters': False,
                'dashboards_gen2_widget_library': False,
                'dynamic_tagging': True,
                'environment_management': False,
                'export_dashboard': True,
                'export_dashboard_pdf': True,
                'general_data_protection_compliance': False,
                'import_data': False,
                'indexing_v2': True,
                'lumin_beta_allowed': False,
                'lumin_beta_enabled': False,
                'modify_vulnerability': False,
                'pci_multiscan': False,
                'qualys_connector': True,
                'qualys_vuln_connector': False,
                'rbac': True,
                'recast_rules': True,
                'reporting': True,
                'scan_service': True,
                'scans_gen2': False,
                'state': True,
                'suggest_feature': True,
                'system': False,
                'tagging': True,
                'vm_service_query': True,
                'vulnerability_management_gen2': True,
                'was_discovery': False,
                'was_multi_scanning': False,
                'was_plugin_selection': True,
                'was_scan_progress': True,
                'webapp_scanning': False,
                'webapp_scanning_gen2': False,
            },
            'apps': {'consec': 'standard', 'was': 'standard'},
            'group_uuids': [],
            'groups': [],
        },
    )
    tvm.users.impersonate(user['username'])
    assert tvm.session.details()['username'] == user['username']
    tvm.session.restore()
    assert tvm.session.details()['username'] != user['username']


@responses.activate
def test_users_list_users(tvm, user):
    """
    test to list users
    """
    responses.add(responses.GET, 'https://nourl/users', json={'users': [user]})
    users = tvm.users.list()
    assert isinstance(users, list)
    assert user['id'] in [u['id'] for u in users]


def test_users_change_password_orig_typeerror(tvm):
    """
    test to raise exception when type of old_password param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.change_password(0, False, 'nope')


def test_users_change_password_new_typeerror(tvm):
    """
    test to raise exception when type of new_password param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.change_password(0, 'nope', False)


@responses.activate
def test_users_change_password_notfounderror(tvm):
    """
    test to raise exception when user_id not found.
    """
    responses.add(
        responses.PUT,
        'https://nourl/users/0/chpasswd',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.users.change_password(0, 'nope', 'nope')


@responses.activate
def test_users_change_password_permissionserror(tvm, user):
    """
    test to raise exception when standard user try to change password.
    """
    responses.add(
        responses.PUT,
        'https://nourl/users/3344/chpasswd',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.change_password(user['id'], 'nope', 'nope')


@responses.activate
def test_users_change_password(tvm):
    """
    test to change password
    """
    responses.add(
        responses.POST,
        'https://nourl/users',
        json={
            'id': 3170,
            'user_name': '1dfdf567-a832-4edb-9d65-692e7ba5ec6f@pytenable.io',
            'username': '1dfdf567-a832-4edb-9d65-692e7ba5ec6f@pytenable.io',
            'email': '1dfdf567-a832-4edb-9d65-692e7ba5ec6f@pytenable.io',
            'name': '1dfdf567-a832-4edb-9d65-692e7ba5ec6f@pytenable.io',
            'type': 'local',
            'aggregate': True,
            'permissions': 16,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'enabled': True,
            'uuid': 'c8e27278-1f81-4fdb-8d7c-4bcfb13748d0',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'uuid_id': 'c8e27278-1f81-4fdb-8d7c-4bcfb13748d0',
        },
    )
    responses.add(responses.PUT, 'https://nourl/users/3170/chpasswd')
    responses.add(responses.DELETE, 'https://nourl/users/3170')
    password = gpass()
    user = tvm.users.create(guser(), password, 16)
    tvm.users.change_password(user['id'], password, gpass())
    tvm.users.delete(user['id'])


@responses.activate
def test_users_list_auths_success(tvm, user):
    """
    test to list user auths
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json=USERS_AUTHORIZATIONS,
    )
    user_auth = tvm.users.list_auths(user['id'])
    assert isinstance(user, dict)
    check(user_auth, 'account_uuid', 'uuid')
    check(user_auth, 'api_permitted', bool)
    check(user_auth, 'password_permitted', bool)
    check(user_auth, 'saml_permitted', bool)
    check(user_auth, 'user_uuid', 'uuid')


@responses.activate
def test_users_list_auths_notfounderror(tvm):
    """
    test to raise exception when user_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/1/authorizations',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.users.list_auths(1)


@responses.activate
def test_users_list_auths_permissionerror(tvm, user):
    """
    test to raise exception when standard user try to get list of user auths.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.list_auths(user['id'])


@responses.activate
def test_users_edit_auths_success(tvm, user):
    """
    test to edit user auths
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json=USERS_AUTHORIZATIONS,
    )
    responses.add(responses.PUT, 'https://nourl/users/3344/authorizations')
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json={
            'account_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'user_uuid': '88aba081-9505-4e06-9acc-2530b486c8d4',
            'api_permitted': False,
            'password_permitted': False,
            'saml_permitted': False,
        },
    )
    tvm.users.edit_auths(user['id'], False, False, False)
    user_auth = tvm.users.list_auths(user['id'])
    assert user_auth['api_permitted'] is False
    assert user_auth['password_permitted'] is False
    assert user_auth['saml_permitted'] is False


@responses.activate
def test_users_edit_auths_notfounderror(tvm):
    """
    test to raise exception when user_id not found.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/1/authorizations',
        json={'statusCode': 404, 'error': 'Not Found', 'message': 'Not Found'},
        status=404,
    )
    with pytest.raises(NotFoundError):
        tvm.users.edit_auths(1)


def test_users_edit_auths_typeerror(tvm):
    """
    test to raise exception when type of user_id param does not match the expected type.
    """
    with pytest.raises(TypeError):
        tvm.users.edit_auths('nope')


@responses.activate
def test_users_edit_auths_api_permitted_typeerror(tvm, user):
    """
    test to raise exception when type of api_permitted param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json=USERS_AUTHORIZATIONS,
    )
    with pytest.raises(TypeError):
        tvm.users.edit_auths(user['id'], api_permitted='nope')


@responses.activate
def test_users_edit_auths_password_permitted_typeerror(tvm, user):
    """
    test to raise exception when type of password_permitted param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json=USERS_AUTHORIZATIONS,
    )
    with pytest.raises(TypeError):
        tvm.users.edit_auths(user['id'], password_permitted='nope')


@responses.activate
def test_users_edit_auths_saml_permitted_typeerror(tvm, user):
    """
    test to raise exception when type of saml_permitted param does not match the expected type.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json=USERS_AUTHORIZATIONS,
    )
    with pytest.raises(TypeError):
        tvm.users.edit_auths(user['id'], saml_permitted='nope')


@responses.activate
def test_users_edit_auths_permissionerror(tvm, user):
    """
    test to raise exception when standard user try to edit user auths.
    """
    responses.add(
        responses.GET,
        'https://nourl/users/3344/authorizations',
        json={'statusCode': 403, 'error': 'Forbidden', 'message': 'Insufficient scope'},
        status=403,
    )
    with pytest.raises(ForbiddenError):
        tvm.users.edit_auths(user['id'])

USER_UUID = '0d67d2fa-558c-4f89-b506-41b4b73101e1'


@responses.activate
@pytest.mark.parametrize(
    'user_id, path',
    [
        (2247978, '2247978'),
        ('2247978', '2247978'),
        (USER_UUID, USER_UUID),
        (USER_UUID.upper(), USER_UUID),
    ],
)
def test_users_delete_id_or_uuid(tvm, user_id, path):
    responses.delete(
        f'https://nourl/users/{path}',
        json={},
        match=[query_param_matcher({})],
    )
    assert tvm.users.delete(user_id) is None
    assert len(responses.calls) == 1


@responses.activate
@pytest.mark.parametrize(
    'user_id, error',
    [('not-a-uuid', UnexpectedValueError), (1.5, TypeError)],
)
def test_users_delete_invalid_user_id(tvm, user_id, error):
    with pytest.raises(error):
        tvm.users.delete(user_id)
    assert len(responses.calls) == 0


SUCCESSOR_UUID = '1697d500-30a5-4a47-bb7a-f239f3c4fe00'


@responses.activate
@pytest.mark.parametrize('successor', [SUCCESSOR_UUID, SUCCESSOR_UUID.upper()])
def test_users_delete_successor(tvm, successor):
    responses.delete(
        f'https://nourl/users/{USER_UUID}',
        json={},
        match=[query_param_matcher({'successor_user_uuid': SUCCESSOR_UUID})],
    )
    assert tvm.users.delete(USER_UUID, successor_user_uuid=successor) is None


@responses.activate
@pytest.mark.parametrize(
    'successor, error',
    [('not-a-uuid', UnexpectedValueError), (2247978, TypeError)],
)
def test_users_delete_successor_invalid(tvm, successor, error):
    with pytest.raises(error):
        tvm.users.delete(1, successor_user_uuid=successor)
    assert len(responses.calls) == 0


def test_users_delete_successor_keyword_only(tvm):
    with pytest.raises(TypeError):
        tvm.users.delete(1, SUCCESSOR_UUID)


@responses.activate
@pytest.mark.parametrize(
    'kwargs, query',
    [({}, {}), ({'with_roles': True}, {'withRoles': 'true'}),
     ({'with_roles': False}, {'withRoles': 'false'})],
)
def test_users_list_with_roles(tvm, kwargs, query):
    users = [{'id': 1, 'rbac_roles': [{'name': 'Administrator', 'uuid': USER_UUID}]}]
    responses.get(
        'https://nourl/users',
        json={'users': users},
        match=[query_param_matcher(query)],
    )
    assert tvm.users.list(**kwargs) == users


@responses.activate
@pytest.mark.parametrize('value', ['maybe', 1])
def test_users_list_with_roles_typeerror(tvm, value):
    with pytest.raises(TypeError):
        tvm.users.list(with_roles=value)
    assert len(responses.calls) == 0
