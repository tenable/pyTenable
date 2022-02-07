import pytest
import responses


@responses.activate
def test_connectors(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.connectors()


@responses.activate
def test_groups(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.groups()


@responses.activate
def test_mssp_accounts(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.mssp.accounts()


@responses.activate
def test_mssp_logos(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.mssp.logos()


@responses.activate
def test_users(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.users()


@responses.activate
def test_vm_agent_exclusions(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.agent_exclusions()


@responses.activate
def test_vm_agent_groups(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.agent_groups()


@responses.activate
def test_vm_agents(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.agents()


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
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.credentials()


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
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.plugins()


@responses.activate
def test_vm_policies(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.policies()


@responses.activate
def test_vm_remediation_scans(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.remediation_scans()


@responses.activate
def test_vm_sccanner_groups(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.scanner_groups()


@responses.activate
def test_vm_scanners(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.scanners()


@responses.activate
def test_vm_scans(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.scans()


@responses.activate
def test_vm_tag_categories(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.tag_categories()


@responses.activate
def test_vm_tags(api):
    with pytest.raises(NotImplementedError):
        api.v3.definitions.vm.tags()


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
