'''
test exports
'''
import time
import uuid
import pytest
from ..checker import check
from tenable.io.exports import ExportsIterator
from tests.pytenable_log_handler import log_exception
from tenable.errors import UnexpectedValueError, TioExportsError


@pytest.mark.vcr()
def test_exports_vuln_num_assets_typeerror(api):
    '''test to raise the exception when type of num_assets is not as defined'''
    with pytest.raises(TypeError):
        api.exports.vulns(num_assets='nope')


@pytest.mark.vcr()
def test_exports_vuln_severity_typeerror(api):
    '''test to raise the exception when type of severity is not as defined'''
    with pytest.raises(TypeError):
        api.exports.vulns(severity='info')


@pytest.mark.vcr()
def test_exports_vuln_state_typeerror(api):
    '''test to raise the exception when type of state is not as defined'''
    with pytest.raises(TypeError):
        api.exports.vulns(state=1)


@pytest.mark.vcr()
def test_exports_vuln_state_unexpectedvalueerror(api):
    '''test to raise the exception when value of state is not as defined'''
    with pytest.raises(UnexpectedValueError):
        api.exports.vulns(state=['nothing here'])


@pytest.mark.vcr()
def test_exports_vuln_plugin_family_typeerror(api):
    '''test to raise the exception when type of plugin_family is not as defined'''

    with pytest.raises(TypeError):
        api.exports.vulns(plugin_family='yes')


@pytest.mark.vcr()
def test_exports_vuln_since_typeerror(api):
    '''test to raise the exception when type of since is not as defined'''
    with pytest.raises(TypeError):
        api.exports.vulns(since='nothing here')


@pytest.mark.vcr()
def test_exports_vuln_cidr_range_invalid_cidr(api):
    '''test to raise the exception when cidr_range is not correct'''
    with pytest.raises(UnexpectedValueError):
        api.exports.vulns(cidr_range='999.168.0.0/24')
    with pytest.raises(UnexpectedValueError):
        api.exports.vulns(cidr_range='192.168.0.0/999')


def test_process_page(api):
    '''test to process the page'''
    exports_iterator = ExportsIterator(getattr(api.exports, '_api'))
    getattr(exports_iterator, '_process_page')(page_data='page_data')
    assert exports_iterator.page is not None
    assert exports_iterator.page == 'page_data'


@pytest.mark.vcr()
def test_exports_vulns_success(api):
    '''test to export vulns data on some parameters'''
    vulns = api.exports.vulns(
        since=1,
        include_unlicensed=True,
        plugin_ids=[1, 2],
        plugin_id=[1],
        severity=['info'],
        state=['OPEN'],
        plugin_family=['family'],
        cidr_range='192.168.0.0/24',
        tags=[('tag_name', 'tag_value')],
        vpr={'gte': 7},
    )
    assert isinstance(vulns, ExportsIterator)


@pytest.mark.vcr()
def test_exports_vulns(api):
    '''test to export the vulns data'''
    vulns = api.exports.vulns()
    assert isinstance(vulns, ExportsIterator)

    vuln = vulns.next()
    assert isinstance(vuln, dict)

    # The asset dictionary appears to be highly variable, so we wont be testing,
    # simply verifying it's presence.
    check(vuln, 'asset', dict)
    check(vuln, 'first_found', str)
    check(vuln, 'last_found', str)
    check(vuln, 'output', str)
    check(vuln, 'plugin', dict)

    # Just like with the asset dictionary, the plug-in sub-document is highly
    # dynamic based on the vulnerability.  We will be focusing on the bare
    # minimums in an attempt to make sure we see the commonalities.
    check(vuln['plugin'], 'description', str)
    check(vuln['plugin'], 'family', str)
    check(vuln['plugin'], 'family_id', int)
    check(vuln['plugin'], 'has_patch', bool)
    check(vuln['plugin'], 'id', int)
    check(vuln['plugin'], 'name', str)
    check(vuln['plugin'], 'risk_factor', str)

    check(vuln, 'port', dict)
    check(vuln['port'], 'port', int)
    check(vuln['port'], 'protocol', str)

    check(vuln, 'scan', dict)
    check(vuln['scan'], 'completed_at', str)
    check(vuln['scan'], 'schedule_uuid', str)
    check(vuln['scan'], 'started_at', str)
    check(vuln['scan'], 'uuid', str)

    check(vuln, 'severity', str)
    check(vuln, 'severity_default_id', int)
    check(vuln, 'severity_id', int)
    check(vuln, 'severity_modification_type', str)
    check(vuln, 'state', str)


@pytest.mark.vcr()
def test_exports_assets_chunk_size_typeerror(api):
    '''test to raise the exception when type of chunk_size is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(chunk_size='something')


@pytest.mark.vcr()
def test_exports_assets_created_at_typeerror(api):
    '''test to raise the exception when type of created_at is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(created_at='nope')


@pytest.mark.vcr()
def test_exports_assets_updated_at_typeerror(api):
    '''test to raise the exception when type of updated_at is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(updated_at='something')


@pytest.mark.vcr()
def test_exports_assets_terminated_at_typeerror(api):
    '''test to raise the exception when type of terminated_at is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(terminated_at='something')


@pytest.mark.vcr()
def test_exports_assets_deleted_at_typerror(api):
    '''test to raise the exception when type of deleted_at is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(deleted_at='something')


@pytest.mark.vcr()
def test_exports_assets_last_authenticated_scan_time_typerror(api):
    '''test to raise the exception when type of last_authenticated_scan_time is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(last_authenticated_scan_time='something')


@pytest.mark.vcr()
def test_exports_assets_last_assessed_typeerror(api):
    '''test to raise the exception when type of last_assessed is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(last_assessed='something')


@pytest.mark.vcr()
def test_exports_assets_servicenow_sysid_typeerror(api):
    '''test to raise the exception when type of servicenow_sysid is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(servicenow_sysid='something')


@pytest.mark.vcr()
def test_exports_assets_sources_typeerror(api):
    '''test to raise the exception when type of sources is not as defined'''
    with pytest.raises(TypeError):
        api.exports.assets(sources=1)


@pytest.mark.vcr()
def test_exports_assets_has_plugin_results_typeerror(api):
    '''test to raise the exception when type of has_plugin_details
    is not matching with the type defined'''
    with pytest.raises(TypeError):
        api.exports.assets(has_plugin_results='something')


@pytest.mark.vcr()
def test_exports_assets_success(api):
    '''test to export the assets data of particular source, tag and uuid'''
    assets = api.exports.assets(sources=['source1'],
                                tags=[('tag_name', 'tag_value')],
                                uuid='12121213')
    assert isinstance(assets, ExportsIterator)


@pytest.mark.vcr()
def test_exports_assets(api):
    '''test to export the asset data'''
    assets = api.exports.assets()
    assert isinstance(assets, ExportsIterator)
    asset = assets.next()
    assert isinstance(asset, dict)
    check(asset, 'agent_names', list)
    check(asset, 'agent_uuid', str, allow_none=True)
    check(asset, 'aws_availability_zone', str, allow_none=True)
    check(asset, 'aws_ec2_instance_ami_id', str, allow_none=True)
    check(asset, 'aws_ec2_instance_group_name', str, allow_none=True)
    check(asset, 'aws_ec2_instance_id', str, allow_none=True)
    check(asset, 'aws_ec2_instance_state_name', str, allow_none=True)
    check(asset, 'aws_ec2_instance_type', str, allow_none=True)
    check(asset, 'aws_ec2_name', str, allow_none=True)
    check(asset, 'aws_ec2_product_code', str, allow_none=True)
    check(asset, 'aws_owner_id', str, allow_none=True)
    check(asset, 'aws_region', str, allow_none=True)
    check(asset, 'aws_subnet_id', str, allow_none=True)
    check(asset, 'aws_vpc_id', str, allow_none=True)
    check(asset, 'azure_resource_id', str, allow_none=True)
    check(asset, 'azure_vm_id', str, allow_none=True)
    check(asset, 'bios_uuid', str, allow_none=True)
    check(asset, 'created_at', str)
    check(asset, 'deleted_at', str, allow_none=True)
    check(asset, 'deleted_by', str, allow_none=True)
    check(asset, 'first_scan_time', str, allow_none=True)
    check(asset, 'first_seen', str, allow_none=True)
    check(asset, 'fqdns', list)
    check(asset, 'has_agent', bool)
    check(asset, 'hostnames', list)
    check(asset, 'id', 'uuid')
    check(asset, 'ipv4s', list)
    check(asset, 'ipv6s', list)
    check(asset, 'last_authenticated_scan_date', str, allow_none=True)
    check(asset, 'last_licensed_scan_date', str, allow_none=True)
    check(asset, 'last_scan_time', str, allow_none=True)
    check(asset, 'last_seen', str, allow_none=True)
    check(asset, 'mac_addresses', list)
    check(asset, 'mcafee_epo_agent_guid', str, allow_none=True)
    check(asset, 'mcafee_epo_guid', str, allow_none=True)
    check(asset, 'netbios_names', list)
    check(asset, 'network_interfaces', list)
    check(asset, 'operating_systems', list)
    check(asset, 'qualys_asset_ids', list)
    check(asset, 'qualys_host_ids', list)
    check(asset, 'servicenow_sysid', str, allow_none=True)

    check(asset, 'sources', list)
    for i in asset['sources']:
        check(i, 'first_seen', str)
        check(i, 'last_seen', str)
        check(i, 'name', str)

    check(asset, 'ssh_fingerprints', list)
    check(asset, 'symantec_ep_hardware_keys', list)
    check(asset, 'system_types', list)
    check(asset, 'tags', list)
    check(asset, 'terminated_at', str, allow_none=True)
    check(asset, 'terminated_by', str, allow_none=True)
    check(asset, 'updated_at', str)


@pytest.mark.vcr()
def test_exports_compliance_num_findings_typeerror(api):
    '''test to raise exception when type of num_findings param does not match the expected type'''
    with pytest.raises(TypeError):
        api.exports.compliance(num_findings='something')


@pytest.mark.vcr()
def test_exports_compliance_num_findings_unexpectedvalueerror(api):
    '''test to raise exception when num_findings param value does not match the choices'''
    with pytest.raises(UnexpectedValueError):
        api.exports.compliance(num_findings=1)


@pytest.mark.vcr()
def test_exports_compliance_asset_typeerror(api):
    '''test to raise exception when type of asset param does not match the expected type'''
    with pytest.raises(TypeError):
        api.exports.compliance(asset='something')


@pytest.mark.vcr()
def test_exports_compliance_asset_unexpectedvalueerror(api):
    '''test to raise exception when any of asset param value
    does not match the expected type'''
    with pytest.raises(UnexpectedValueError):
        api.exports.compliance(asset=['something'])


@pytest.mark.vcr()
def test_exports_compliance_asset_limit_exceed_unexpectedvalueerror(api):
    '''test to raise exception when count of asset param values exceeds allowed count'''
    with pytest.raises(UnexpectedValueError):
        api.exports.compliance(asset=[str(uuid.uuid4()) for _ in range(202)])


@pytest.mark.vcr()
def test_exports_compliance_last_seen_typeerror(api):
    ''''test to raise exception when type of last_seen param does not match the expected type'''
    with pytest.raises(TypeError):
        api.exports.compliance(last_seen='something')


@pytest.mark.vcr()
def test_exports_compliance_first_seen_typeerror(api):
    '''test to raise exception when type of first_seen param does not match the expected type'''
    with pytest.raises(TypeError):
        api.exports.compliance(last_seen=1, first_seen='something')


@pytest.mark.vcr()
def test_exports_compliance_success(api):
    '''test to export the compliance data'''
    last_seen = int(time.time()) - (12 * 60 * 60)
    compliance = api.exports.compliance(num_findings=51,
                                        last_seen=last_seen
                                        )
    assert isinstance(compliance, ExportsIterator)


@pytest.mark.vcr()
def test_exports_compliance(api):
    '''test to export the compliance data'''
    compliance = api.exports.compliance(last_seen=1626168578)
    assert isinstance(compliance, ExportsIterator)
    try:
        for resp in compliance:
            # common keys for all status types
            check(resp, 'asset_uuid', 'uuid')
            if 'audit_file' in resp:
                check(resp, 'audit_file', str)
            check(resp, 'check_id', str)
            if 'check_name' in resp:
                check(resp, 'check_name', str)
            check(resp, 'first_seen', str)
            check(resp, 'last_seen', str)
            check(resp, 'plugin_id', int)
            check(resp, 'status', str)

            # keys available in failed and warning and may be available in other status types
            if resp['status'] == 'FAILED' or resp['status'] == 'WARNING':
                check(resp, 'check_info', str)
                check(resp, 'see_also', str)
                check(resp, 'solution', str)
                check(resp, 'reference', list)

                for data in resp['reference']:
                    check(data, 'control', str)
                    check(data, 'framework', str)

            # keys available in passed, failed and warning type status
            if resp['status'] == 'FAILED' or resp['status'] == 'WARNING':
                check(resp, 'expected_value', str)

            # keys available in error type status
            if resp['status'] == 'ERROR':
                check(resp, 'check_error', str)
    except TioExportsError as error:
        print(error.msg)
        log_exception(error)
