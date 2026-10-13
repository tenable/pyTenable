import uuid

import pytest
import responses

from ..checker import check


@responses.activate
def test_session_edit(tvm):
    responses.add(
        responses.PUT,
        'https://nourl/session',
        json={
            'id': 3,
            'user_name': 'test_admin@pytenable.io',
            'username': 'test_admin@pytenable.io',
            'email': 'noreply@pytenable.test',
            'name': '00bc5450-497e-4047-9f0b-0e2755d7cd2e',
            'type': 'local',
            'whatsnew_version': '',
            'aggregate': True,
            'permissions': 64,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'enabled': True,
            'uuid': 'a09161a2-3860-4ca8-93c8-b3f7be366e50',
            'container_uuid': 'a0abbae8-512f-4b9d-93f3-74d9809a1004',
            'uuid_id': 'a09161a2-3860-4ca8-93c8-b3f7be366e50',
        },
    )
    tvm.session.edit(str(uuid.uuid4()), 'noreply@tenable.com')


@responses.activate
def test_session_details(tvm):
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
            'group_uuids': [],
            'groups': [],
        },
    )
    session = tvm.session.details()
    assert isinstance(session, dict)
    check(session, 'container_id', int)
    check(session, 'container_uuid', 'uuid')
    check(session, 'container_name', str)
    check(session, 'email', str)
    check(session, 'enabled', bool)
    check(session, 'group_uuids', list)
    check(session, 'groups', list)
    check(session, 'id', int)
    check(session, 'login_fail_count', int)
    check(session, 'login_fail_total', int)
    check(session, 'name', str)
    check(session, 'user_name', str)
    check(session, 'username', str)
    check(session, 'uuid', 'uuid')
    check(session, 'uuid_id', str)
    check(session, 'features', dict)
    for item in session['features'].keys():
        check(session['features'], item, bool)


@pytest.mark.skip(reason="Don't have old password")
def test_session_change_password(tvm):
    pass


@pytest.mark.skip(reason="Don't want to change the API keys")
def test_session_gen_api_keys(tvm):
    pass


def test_session_two_factor_email_typeerror(tvm):
    with pytest.raises(TypeError):
        tvm.session.two_factor(False, 'nope')


def test_session_two_factor_sms_typeerror(tvm):
    with pytest.raises(TypeError):
        tvm.session.two_factor('nope', False)


def test_session_two_factor_phone_typeerror(tvm):
    with pytest.raises(TypeError):
        tvm.session.two_factor(False, False, 8675309)


@pytest.mark.skip(reason="Don't want to enable two-factor on this user.")
def test_session_two_factor(tvm):
    tvm.session.two_factor(False, False)


def test_session_enable_two_factor_phone_typeerror(tvm):
    with pytest.raises(TypeError):
        tvm.session.enable_two_factor(False)


@pytest.mark.skip(reason="Don't want to enable two-factor on this user.")
def test_session_enable_two_factor(tvm):
    tvm.session.enable_two_factor('867-5309')


def test_session_verify_two_factor_code_typeerror(tvm):
    with pytest.raises(TypeError):
        tvm.session.verify_two_factor(False)


@pytest.mark.skip(reason="Don't want to enable two-factor on this user.")
def test_session_verify_two_factor(tvm):
    tvm.session.verify_two_factor(False)


@pytest.mark.skip(reason="We're testing this in the users test suite.")
# This is likely because we never impersonated in the first place.
def test_session_restore(tvm, user):
    pass
