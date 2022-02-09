import pytest
import responses

from tests.io.v3.definitions.objects import (MSSP_DEFINITIONS,
                                             PLATFORM_DEFINITIONS,
                                             VM_DEFINITIONS)

BASE_URL = 'https://cloud.tenable.com/api/v3/definitions'


@responses.activate
def test_connectors(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/connectors',
        json=PLATFORM_DEFINITIONS['CONNECTORS']
    )
    res = api.v3.definitions.connectors()
    assert res == PLATFORM_DEFINITIONS['CONNECTORS']


@responses.activate
def test_groups(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/groups',
        json=PLATFORM_DEFINITIONS['GROUPS']
    )
    res = api.v3.definitions.groups()
    assert res == PLATFORM_DEFINITIONS['GROUPS']


@responses.activate
def test_mssp_accounts(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/mssp/accounts',
        json=MSSP_DEFINITIONS['ACCOUNTS']
    )
    res = api.v3.definitions.mssp.accounts()
    assert res == MSSP_DEFINITIONS['ACCOUNTS']


@responses.activate
def test_mssp_logos(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/mssp/logos',
        json=MSSP_DEFINITIONS['LOGOS']
    )
    res = api.v3.definitions.mssp.logos()
    assert res == MSSP_DEFINITIONS['LOGOS']


@responses.activate
def test_users(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.users()


@responses.activate
def test_vm_agent_exclusions(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/agent-exclusions',
        json=VM_DEFINITIONS['AGENT_EXCLUSIONS']
    )
    res = api.v3.definitions.vm.agent_exclusions()
    assert res == VM_DEFINITIONS['AGENT_EXCLUSIONS']


@responses.activate
def test_vm_agent_groups(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/agent-groups',
        json=VM_DEFINITIONS['AGENT_GROUPS']
    )
    res = api.v3.definitions.vm.agent_groups()
    assert res == VM_DEFINITIONS['AGENT_GROUPS']


@responses.activate
def test_vm_agents(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/agents',
        json=VM_DEFINITIONS['AGENTS']
    )
    res = api.v3.definitions.vm.agents()
    assert res == VM_DEFINITIONS['AGENTS']


@responses.activate
def test_vm_assets(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.assets()


@responses.activate
def test_vm_audit_logs(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.audit_logs()


@responses.activate
def test_vm_credentials(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/credentials',
        json=VM_DEFINITIONS['CREDENTIALS']
    )
    res = api.v3.definitions.vm.credentials()
    assert res == VM_DEFINITIONS['CREDENTIALS']


@responses.activate
def test_vm_editors(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.editors()


@responses.activate
def test_vm_exclusions(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.exclusions()


@responses.activate
def test_vm_folders(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.folders()


@responses.activate
def test_vm_networks(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.networks()


@responses.activate
def test_vm_plugin_families(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.plugin_families()


@responses.activate
def test_vm_plugins(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/plugins',
        json=VM_DEFINITIONS['PLUGINS']
    )
    res = api.v3.definitions.vm.plugins()
    assert res == VM_DEFINITIONS['PLUGINS']


@responses.activate
def test_vm_policies(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.policies()


@responses.activate
def test_vm_remediation_scans(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.remediation_scans()


@responses.activate
def test_vm_scanner_groups(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/scanner-groups',
        json=VM_DEFINITIONS['SCANNER_GROUPS']
    )
    res = api.v3.definitions.vm.scanner_groups()
    assert res == VM_DEFINITIONS['SCANNER_GROUPS']


@responses.activate
def test_vm_scanners(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.scanners()


@responses.activate
def test_vm_scans(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/scans',
        json=VM_DEFINITIONS['SCANS']
    )
    res = api.v3.definitions.vm.scans()
    assert res == VM_DEFINITIONS['SCANS']


@responses.activate
def test_vm_tag_categories(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.tag_categories()


@responses.activate
def test_vm_tags(api):
    responses.add(
        responses.GET,
        f'{BASE_URL}/tags/assets/',
        json=VM_DEFINITIONS['TAGS']
    )
    res = api.v3.definitions.vm.tags()
    assert res == VM_DEFINITIONS['TAGS']


@responses.activate
def test_vm_vulnerabilities(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.vulnerabilities()


@responses.activate
def test_was_configurations(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.configurations()


@responses.activate
def test_was_folders(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.folders()


@responses.activate
def test_was_plugins(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.plugins()


@responses.activate
def test_was_vulnerabilities(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.vulnerabilities()


@responses.activate
def test_was_scan_vulnerabilities(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.scan_vulnerabilities()


@responses.activate
def test_was_scans(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.scans()


@responses.activate
def test_was_templates(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.templates()


@responses.activate
def test_was_user_templates(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.was.user_templates()
