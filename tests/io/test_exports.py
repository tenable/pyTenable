from datetime import datetime, timedelta
from tenable.errors import *
from ..checker import check, single
from tenable.io.exports import ExportsIterator
import pytest

@pytest.mark.vcr()
def test_exports_vuln_num_assets_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.vulns(num_assets='nope')

@pytest.mark.vcr()
def test_exports_vuln_severity_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.vulns(severity='info')

@pytest.mark.vcr()
def test_exports_vuln_state_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.vulns(state=1)

@pytest.mark.vcr()
def test_exports_vuln_state_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.exports.vulns(state=['nothing here'])

@pytest.mark.vcr()
def test_exports_vuln_plugin_family_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.vulns(plugin_family='yes')

@pytest.mark.vcr()
def test_exports_vuln_since_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.vulns(since='nothing here')

@pytest.mark.vcr()
def test_exports_vuln_cidr_range_invalid_cidr(api):
    with pytest.raises(UnexpectedValueError):
        api.exports.vulns(cidr_range='999.168.0.0/24')
    with pytest.raises(UnexpectedValueError):
        api.exports.vulns(cidr_range='192.168.0.0/999')

@pytest.mark.vcr()
def test_exports_vulns(api):
    vulns = api.exports.vulns()
    assert isinstance(vulns, ExportsIterator)

    v = vulns.next()
    assert isinstance(v, dict)

    # The asset dictionary appears to be highly variable, so we wont be testing,
    # simply verifying it's presence.
    check(v, 'asset', dict)
    check(v, 'first_found', str)
    check(v, 'last_found', str)
    check(v, 'output', str)
    check(v, 'plugin', dict)

    # Just like with the asset dictionary, the plug-in sub-document is highly
    # dynamic based on the vulnerability.  We will be focusing on the bare
    # minimums in an attempt to make sure we see the commonalities.
    check(v['plugin'], 'description', str)
    check(v['plugin'], 'family', str)
    check(v['plugin'], 'family_id', int)
    check(v['plugin'], 'has_patch', bool)
    check(v['plugin'], 'id', int)
    check(v['plugin'], 'name', str)
    check(v['plugin'], 'risk_factor', str)

    check(v, 'port', dict)
    check(v['port'], 'port', int)
    check(v['port'], 'protocol', str)

    check(v, 'scan', dict)
    check(v['scan'], 'completed_at', str)
    check(v['scan'], 'schedule_uuid', str)
    check(v['scan'], 'started_at', str)
    check(v['scan'], 'uuid', str)

    check(v, 'severity', str)
    check(v, 'severity_default_id', int)
    check(v, 'severity_id', int)
    check(v, 'severity_modification_type', str)
    check(v, 'state', str)

@pytest.mark.vcr()
def test_exports_assets_chunk_size_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(chunk_size='something')

@pytest.mark.vcr()
def test_exports_assets_created_at_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(created_at='nope')

@pytest.mark.vcr()
def test_exports_assets_updated_at_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(updated_at='something')

@pytest.mark.vcr()
def test_exports_assets_terminated_at_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(terminated_at='something')

@pytest.mark.vcr()
def test_exports_assets_deleted_at_typerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(deleted_at='something')

@pytest.mark.vcr()
def test_exports_assets_last_authenticated_scan_time_typerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(last_authenticated_scan_time='something')

@pytest.mark.vcr()
def test_exports_assets_last_assessed_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(last_assessed='something')

@pytest.mark.vcr()
def test_exports_assets_servicenow_sysid_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(servicenow_sysid='something')

@pytest.mark.vcr()
def test_exports_assets_sources_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(sources=1)

@pytest.mark.vcr()
def test_exports_assets_has_plugin_results_typeerror(api):
    with pytest.raises(TypeError):
        api.exports.assets(has_plugin_results='something')

@pytest.mark.vcr()
def test_exports_assets(api):
    assets = api.exports.assets()
    assert isinstance(assets, ExportsIterator)

    a = assets.next()
    assert isinstance(a, dict)

    check(a, 'agent_names', list)
    check(a, 'agent_uuid', str, allow_none=True)
    check(a, 'aws_availability_zone', str, allow_none=True)
    check(a, 'aws_ec2_instance_ami_id', str, allow_none=True)
    check(a, 'aws_ec2_instance_group_name', str, allow_none=True)
    check(a, 'aws_ec2_instance_id', str, allow_none=True)
    check(a, 'aws_ec2_instance_state_name', str, allow_none=True)
    check(a, 'aws_ec2_instance_type', str, allow_none=True)
    check(a, 'aws_ec2_name', str, allow_none=True)
    check(a, 'aws_ec2_product_code', str, allow_none=True)
    check(a, 'aws_owner_id', str, allow_none=True)
    check(a, 'aws_region', str, allow_none=True)
    check(a, 'aws_subnet_id', str, allow_none=True)
    check(a, 'aws_vpc_id', str, allow_none=True)
    check(a, 'azure_resource_id', str, allow_none=True)
    check(a, 'azure_vm_id', str, allow_none=True)
    check(a, 'bios_uuid', str, allow_none=True)
    check(a, 'created_at', str)
    check(a, 'deleted_at', str, allow_none=True)
    check(a, 'deleted_by', str, allow_none=True)
    check(a, 'first_scan_time', str, allow_none=True)
    check(a, 'first_seen', str, allow_none=True)
    check(a, 'fqdns', list)
    check(a, 'has_agent', bool)
    check(a, 'has_plugin_results', bool)
    check(a, 'hostnames', list)
    check(a, 'id', 'uuid')
    check(a, 'ipv4s', list)
    check(a, 'ipv6s', list)
    check(a, 'last_authenticated_scan_date', str, allow_none=True)
    check(a, 'last_licensed_scan_date', str, allow_none=True)
    check(a, 'last_scan_time', str, allow_none=True)
    check(a, 'last_seen', str, allow_none=True)
    check(a, 'mac_addresses', list)
    check(a, 'mcafee_epo_agent_guid', str, allow_none=True)
    check(a, 'mcafee_epo_guid', str, allow_none=True)
    check(a, 'netbios_names', list)
    check(a, 'network_interfaces', list)
    check(a, 'operating_systems', list)
    check(a, 'qualys_asset_ids', list)
    check(a, 'qualys_host_ids', list)
    check(a, 'servicenow_sysid', str, allow_none=True)

    check(a, 'sources', list)
    for i in a['sources']:
        check(i, 'first_seen', str)
        check(i, 'last_seen', str)
        check(i, 'name', str)

    check(a, 'ssh_fingerprints', list)
    check(a, 'symantec_ep_hardware_keys', list)
    check(a, 'system_types', list)
    check(a, 'tags', list)
    check(a, 'terminated_at', str, allow_none=True)
    check(a, 'terminated_by', str, allow_none=True)
    check(a, 'updated_at', str)