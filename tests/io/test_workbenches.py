'''
test workbenches
'''
import uuid
from io import BytesIO
import pytest
from tenable.errors import UnexpectedValueError, NotFoundError
from tests.checker import check

@pytest.mark.vcr()
def test_workbench_assets_age_typeerror(api):
    '''
    test to raise exception when type of age param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.assets(age='onetwothree')

@pytest.mark.vcr()
def test_workbench_assets_filter_tyype_typeerror(api):
    '''
    test to raise exception when type of filter param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.assets(filter_type=1)

@pytest.mark.vcr()
def test_workbench_assets_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.assets(filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_assets(api):
    '''
    test to get workbench assets
    '''
    assets = api.workbenches.assets()
    assert isinstance(assets, list)
    if assets:
        asset = assets[0]
        check(asset, 'access_group_id', list)
        check(asset, 'agent_name', list)
        check(asset, 'aws_availability_zone', list)
        check(asset, 'aws_ec2_instance_ami_id', list)
        check(asset, 'aws_ec2_instance_group_name', list)
        check(asset, 'aws_ec2_instance_id', list)
        check(asset, 'aws_ec2_instance_state_name', list)
        check(asset, 'aws_ec2_instance_type', list)
        check(asset, 'aws_ec2_name', list)
        check(asset, 'aws_ec2_product_code', list)
        check(asset, 'aws_owner_id', list)
        check(asset, 'aws_region', list)
        check(asset, 'aws_subnet_id', list)
        check(asset, 'aws_vpc_id', list)
        check(asset, 'azure_resource_id', list)
        check(asset, 'azure_vm_id', list)
        check(asset, 'bios_uuid', list)
        check(asset, 'created_at', 'datetime')
        check(asset, 'first_scan_time', 'datetime', allow_none=True)
        check(asset, 'first_seen', 'datetime', allow_none=True)
        check(asset, 'fqdn', list)
        check(asset, 'gcp_instance_id', list)
        check(asset, 'gcp_project_id', list)
        check(asset, 'gcp_zone', list)
        check(asset, 'has_agent', bool)
        check(asset, 'hostname', list)
        check(asset, 'id', 'uuid')
        check(asset, 'installed_software', list)
        check(asset, 'interfaces', list)
        for interface in asset['interfaces']:
            check(interface, 'fqdn', list)
            check(interface, 'ipv4', list)
            check(interface, 'ipv6', list)
            check(interface, 'mac_address', list)
            check(interface, 'name', str)
        check(asset, 'ipv4', list)
        check(asset, 'ipv6', list)
        check(asset, 'last_authenticated_scan_date', 'datetime', allow_none=True)
        check(asset, 'last_licensed_scan_date', 'datetime', allow_none=True)
        check(asset, 'last_scan_id', 'scanner-uuid', allow_none=True)
        check(asset, 'last_scan_target', str, allow_none=True)
        check(asset, 'last_schedule_id', str, allow_none=True)
        check(asset, 'last_scan_time', 'datetime', allow_none=True)
        check(asset, 'last_seen', 'datetime', allow_none=True)
        check(asset, 'mac_address', list)
        check(asset, 'manufacturer_tpm_id', list)
        check(asset, 'mcafee_epo_agent_guid', list)
        check(asset, 'mcafee_epo_guid', list)
        check(asset, 'netbios_name', list)
        check(asset, 'network_id', list)
        check(asset, 'operating_system', list)
        check(asset, 'qualys_asset_id', list)
        check(asset, 'qualys_host_id', list)
        check(asset, 'servicenow_sysid', list)
        check(asset, 'sources', list)
        for source in asset['sources']:
            check(source, 'first_seen', 'datetime')
            check(source, 'last_seen', 'datetime')
            check(source, 'name', str)
        check(asset, 'ssh_fingerprint', list)
        check(asset, 'symantec_ep_hardware_key', list)
        check(asset, 'system_type', list)
        check(asset, 'tag_id', list)
        check(asset, 'tags', list)
        check(asset, 'tenable_uuid', list)
        check(asset, 'terminated_at', 'datetime', allow_none=True)
        check(asset, 'terminated_by', str, allow_none=True)
        check(asset, 'updated_at', 'datetime')

@pytest.mark.vcr()
def test_workbench_assets_filtered(api):
    '''
    test to get filtered workbench assets
    '''
    assets = api.workbenches.assets(('operating_system', 'match', 'Linux'))
    assert isinstance(assets, list)


@pytest.mark.vcr()
def test_workbench_assets_bad_filter(api):
    '''
    test to raise exception when any of filter param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.assets(('operating_system', 'contains', 'Linux'))


@pytest.mark.vcr()
def test_workbench_asset_activity_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_activity(1)


@pytest.mark.vcr()
def test_workbench_asset_activity_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_activity('This should fail')


@pytest.mark.vcr()
def test_workbench_asset_activity(api):
    '''
    test to get workbench asset activity
    '''
    assets = api.workbenches.assets()
    try:
        if assets:
            history = api.workbenches.asset_activity(assets[0]['id'])
            assert isinstance(history, list)
            for data in history:
                check(data, 'timestamp', 'datetime')
                check(data, 'type', str)
                if data['type'] in ['tagging', 'updated']:
                    check(data, 'updates', list)
                    for update in data['updates']:
                        check(update, 'method', str)
                        check(update, 'property', str)
                        check(update, 'value', str)
                if data['type'] == 'discovered':
                    check(data, 'details', dict)
                    check(data['details'], 'assetId', 'uuid')
                    check(data['details'], 'createdAt', 'datetime')
                    check(data['details'], 'firstScanTime', 'datetime')
                    check(data['details'], 'hasAgent', bool)
                    check(data['details'], 'lastLicensedScanTime', 'datetime')
                    check(data['details'], 'lastLicensedScanTimeV2', 'datetime')
                    check(data['details'], 'lastScanTime', 'datetime')
                    check(data['details'], 'properties', dict)
                    for keys in data['details']['properties'].keys():
                        check(data['details']['properties'][keys], 'values', list)
                    check(data['details'], 'sources', list)
                    for status in data['details']['sources']:
                        check(status, 'firstSeen', 'datetime')
                        check(status, 'lastSeen', 'datetime')
                        check(status, 'name', str)
                    check(data['details'], 'updatedAt', 'datetime')
                if data['type'] in ['discovered', 'seen', 'updated']:
                    check(data, 'scan_id', 'scanner-uuid')
                    check(data, 'schedule_id', str)
                    check(data, 'source', str)
    except NotFoundError:
        print('Activity for the asset uuid is not found')

@pytest.mark.vcr()
def test_workbench_asset_info_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_info(1)


@pytest.mark.vcr()
def test_workbench_asset_info_unexpectedvalueerror(api):
    '''
    test to raise exception when uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_info('abnc-1234-somethinginvalid')


@pytest.mark.vcr()
def test_workbench_asset_info_all_fields_typeerror(api):
    '''
    test to raise exception when type of all_fields param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_info('', all_fields='one')


@pytest.mark.vcr()
def test_workbench_asset_info(api):
    '''
    test to get workbench assets info
    '''
    assets = api.workbenches.assets()
    api.workbenches.asset_info(assets[0]['id'])

@pytest.mark.vcr()
def test_workbench_asset_vulns_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vulns(1)


@pytest.mark.vcr()
def test_workbench_asset_vulns_age_typeerror(api):
    '''
    test to raise exception when type of age param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vulns(str(uuid.uuid4()), age='none')


@pytest.mark.vcr()
def test_workbench_asset_vulns_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vulns(str(uuid.uuid4()), filter_type=123)


@pytest.mark.vcr()
def test_workbench_asset_vulns_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vulns(str(uuid.uuid4()), filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_asset_vulns_invalid_filter(api):
    '''
    test to raise exception when any of filter param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vulns(str(uuid.uuid4()),
                                    ('operating_system', 'contains', 'Linux'))


@pytest.mark.vcr()
def test_workbench_asset_vulns(api):
    '''
    test to get workbench asset vulnerabilities
    '''
    assets = api.workbenches.assets()
    if assets:
        vulns = api.workbenches.asset_vulns(assets[0]['id'])
        assert isinstance(vulns, list)
        if vulns:
            vulnerability = vulns[0]
            check(vulnerability, 'accepted_count', int)
            check(vulnerability, 'count', int)
            check(vulnerability, 'counts_by_severity', list)
            for counts_by_severity in vulnerability['counts_by_severity']:
                check(counts_by_severity, 'count', int)
                check(counts_by_severity, 'value', int)
            check(vulnerability, 'plugin_family', str)
            check(vulnerability, 'plugin_id', int)
            check(vulnerability, 'plugin_name', str)
            check(vulnerability, 'recasted_count', int)
            check(vulnerability, 'severity', int)
            check(vulnerability, 'vulnerability_state', str)

@pytest.mark.vcr()
def test_workbench_asset_vulns_filtered(api):
    '''
    test to get filtered workbench asset vulnerabilities
    '''
    assets = api.workbenches.assets()
    if assets:
        vulns = api.workbenches.asset_vulns(assets[0]['id'],
            ('severity', 'eq', 'Info'))
        assert isinstance(vulns, list)
        if vulns:
            vulnerability = vulns[0]
            check(vulnerability, 'accepted_count', int)
            check(vulnerability, 'count', int)
            check(vulnerability, 'counts_by_severity', list)
            for counts_by_severity in vulnerability['counts_by_severity']:
                check(counts_by_severity, 'count', int)
                check(counts_by_severity, 'value', int)
            check(vulnerability, 'plugin_family', str)
            check(vulnerability, 'plugin_id', int)
            check(vulnerability, 'plugin_name', str)
            check(vulnerability, 'severity', int)
            check(vulnerability, 'vulnerability_state', str)

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(1, 1)


@pytest.mark.vcr()
def test_workbench_asset_vuln_info_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_info('this is not a valid UUID', 1234)


@pytest.mark.vcr()
def test_workbench_asset_vuln_info_plugin_id_typeerror(api):
    '''
    test to raise exception when type of plugin_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 'something here')


@pytest.mark.vcr()
def test_workbench_asset_vuln_info_age_typeerror(api):
    '''
    test to raise exception when type of age param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506, age='none')


@pytest.mark.vcr()
def test_workbench_asset_vuln_info_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506, filter_type=123)


@pytest.mark.vcr()
def test_workbench_asset_vuln_info_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506, filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_asset_vuln_info_invalid_filter(api):
    '''
    test to raise exception when uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506,
                                        ('operating_system', 'contains', 'Linux'))


@pytest.mark.vcr()
def test_workbench_asset_vuln_info(api):
    '''
    test to get workbench asset vulnerabilities info
    '''
    vuln = api.workbenches.vuln_assets()
    if vuln and vuln[0]['ipv4']:
        vuln_list = api.workbenches.asset_vulns(vuln[0]['id'])
        if vuln_list:
            plugin_id = vuln_list[0]['plugin_id']
            info = api.workbenches.asset_vuln_info(vuln[0]['id'], plugin_id)
            check(info, 'accepted_count', int)
            check(info, 'count', int)
            check(info, 'discovery', dict)
            check(info['discovery'], 'seen_first', 'datetime', allow_none=True)
            check(info['discovery'], 'seen_last', 'datetime', allow_none=True)
            check(info, 'plugin_details', dict)
            check(info['plugin_details'], 'family', str)
            check(info['plugin_details'], 'modification_date', 'datetime', allow_none=True)
            check(info['plugin_details'], 'name', str)
            check(info['plugin_details'], 'publication_date', 'datetime', allow_none=True)
            check(info['plugin_details'], 'severity', int)
            check(info['plugin_details'], 'type', str, allow_none=True)
            check(info['plugin_details'], 'version', str, allow_none=True)
            check(info, 'recasted_count', int)
            check(info, 'reference_information', list)
            check(info, 'risk_information', dict)
            check(info['risk_information'], 'cvss3_base_score', str, allow_none=True)
            check(info['risk_information'], 'cvss3_temporal_score', str, allow_none=True)
            check(info['risk_information'], 'cvss3_temporal_vector', str, allow_none=True)
            check(info['risk_information'], 'cvss3_vector', str, allow_none=True)
            check(info['risk_information'], 'cvss_base_score', str, allow_none=True)
            check(info['risk_information'], 'cvss_temporal_score', str, allow_none=True)
            check(info['risk_information'], 'cvss_temporal_vector', str, allow_none=True)
            check(info['risk_information'], 'cvss_vector', str, allow_none=True)
            check(info['risk_information'], 'risk_factor', str, allow_none=True)
            check(info['risk_information'], 'stig_severity', str, allow_none=True)
            check(info, 'see_also', list)
            check(info, 'severity', int)
            check(info, 'vuln_count', int)


@pytest.mark.vcr()
def test_workbench_asset_vuln_output_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(1, 1)


@pytest.mark.vcr()
def test_workbench_asset_vuln_output_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_output('this is not a valid UUID', 1234)


@pytest.mark.vcr()
def test_workbench_asset_vuln_output_plugin_id_typeerror(api):
    '''
    test to raise exception when type of plugin_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 'something here')


@pytest.mark.vcr()
def test_workbench_asset_vuln_output_age_typeerror(api):
    '''
    test to raise exception when type of age param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, age='none')


@pytest.mark.vcr()
def test_workbench_asset_vuln_output_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, filter_type=123)


@pytest.mark.vcr()
def test_workbench_asset_vuln_output_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_asset_vuln_output_invalid_filter(api):
    '''
    test to raise exception when any of filter param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506,
                                          ('operating_system', 'contains', 'Linux'))


@pytest.mark.vcr()
def test_workbench_asset_vuln_output(api):
    '''
    test to get workbench asset vulnerabilities output
    '''
    vuln = api.workbenches.vuln_assets()
    if vuln and vuln[0]['ipv4']:
        vuln_list = api.workbenches.asset_vulns(vuln[0]['id'])
        if vuln_list:
            plugin_id = vuln_list[0]['plugin_id']
            outputs = api.workbenches.asset_vuln_output(vuln[0]['id'], plugin_id)
            assert isinstance(outputs, list)
            output = outputs[0]
            check(output, 'plugin_output', str)
            check(output, 'states', list)
            for state in output['states']:
                check(state, 'name', str)
                check(state, 'results', list)
                for result in state['results']:
                    check(result, 'application_protocol', str, allow_none=True)
                    check(result, 'assets', list)
                    for asset in result['assets']:
                        check(asset, 'first_seen', 'datetime', allow_none=True)
                        check(asset, 'fqdn', str, allow_none=True)
                        check(asset, 'hostname', str)
                        check(asset, 'id', 'uuid')
                        check(asset, 'ipv4', str, allow_none=True)
                        check(asset, 'last_seen', 'datetime', allow_none=True)
                        check(asset, 'netbios_name', str, allow_none=True)
                        check(asset, 'uuid', 'uuid')
                    check(result, 'port', int)
                    check(result, 'severity', int)
                    check(result, 'transport_protocol', str)

@pytest.mark.vcr()
def test_workbench_vuln_assets(api):
    '''
    test to get workbench vulnerability assets
    '''
    assets = api.workbenches.vuln_assets()
    assert isinstance(assets, list)
    asset = assets[0]
    check(asset, 'agent_name', list)
    check(asset, 'fqdn', list)
    check(asset, 'id', 'uuid')
    check(asset, 'ipv4', list)
    check(asset, 'ipv6', list)
    check(asset, 'last_seen', 'datetime')
    check(asset, 'netbios_name', list)
    check(asset, 'severities', list)
    for severity in asset['severities']:
        check(severity, 'count', int)
        check(severity, 'level', int)
        check(severity, 'name', str)
    check(asset, 'total', int)

@pytest.mark.vcr()
def test_workbench_export_asset_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.export(asset_uuid=123)


@pytest.mark.vcr()
def test_workbench_export_asset_uuid_unexpectedvalueerror(api):
    '''
    test to raise exception when uuid param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(asset_uuid='something')


@pytest.mark.vcr()
def test_workbench_export_plugin_id_typeerror(api):
    '''
    test to raise exception when type of plugin_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.export(plugin_id='something')


@pytest.mark.vcr()
def test_workbench_export_format_typeerror(api):
    '''
    test to raise exception when type of format param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.export(format=1234)


@pytest.mark.vcr()
def test_workbench_export_format_unexpectedvalueerror(api):
    '''
    test to raise exception when format param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(format='something else')


@pytest.mark.vcr()
def test_workbench_export_chapters_typeerror(api):
    '''
    test to raise exception when type of chapter param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.export(format='html', chapters='diff')


@pytest.mark.vcr()
def test_workbench_export_chapters_unexpectedvalueerror(api):
    '''
    test to raise exception when chapter param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(format='html', chapters=['something'])


@pytest.mark.vcr()
def test_workbench_export_missing_chapters(api):
    '''
    test to raise exception when chapter param value not provided with format.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(format='html')


@pytest.mark.vcr()
def test_workbench_export_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.export(filter_type=1)


@pytest.mark.vcr()
def test_workbench_export_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_export(api):
    '''
    test workbench export
    '''
    fobj = api.workbenches.export()
    assert isinstance(fobj, BytesIO)


@pytest.mark.vcr()
def test_workbench_export_plugin_id(api):
    '''
    test workbench export with plugin_id
    '''
    fobj = api.workbenches.export(plugin_id=19506)
    assert isinstance(fobj, BytesIO)


@pytest.mark.vcr()
def test_workbench_export_asset_uuid(api):
    '''
    test workbench export with asset_uuid
    '''
    assets = api.workbenches.assets()
    fobj = api.workbenches.export(asset_uuid=assets[0]['id'])
    assert isinstance(fobj, BytesIO)


@pytest.mark.vcr()
def test_workbench_vulns_age_typeerror(api):
    '''
    test to raise exception when type of age param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vulns(age='none')


@pytest.mark.vcr()
def test_workbench_vulns_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vulns(filter_type=123)


@pytest.mark.vcr()
def test_workbench_vulns_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vulns(filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_vulns_invalid_filter(api):
    '''
    test to raise exception when any of filter param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vulns(('nothing here', 'contains', 'Linux'))


@pytest.mark.vcr()
def test_workbench_vulns_authenticated_typeerror(api):
    '''
    test to raise exception when type of authenticated param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vulns(authenticated='nope')


@pytest.mark.vcr()
def test_workbench_vulns_exploitable_typeerror(api):
    '''
    test to raise exception when type of exploitable param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vulns(exploitable='nope')


@pytest.mark.vcr()
def test_workbench_vulns_resolvable_typeerror(api):
    '''
    test to raise exception when type of resolvable param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vulns(resolvable='nope')


@pytest.mark.vcr()
def test_workbench_vulns_severity_typeerror(api):
    '''
    test to raise exception when type of severity param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vulns(severity=['low'])


@pytest.mark.vcr()
def test_workbench_vulns_severity_unexpectedvalueerror(api):
    '''
    test to raise exception when severity param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vulns(severity='something else')


@pytest.mark.vcr()
def test_workbench_vulns(api):
    '''
    test to get workbench vulnerabilities
    '''
    vulns = api.workbenches.vulns()
    assert isinstance(vulns, list)
    if vulns:
        vulnerability = vulns[0]
        check(vulnerability, 'accepted_count', int)
        check(vulnerability, 'counts_by_severity', list)
        for counts_by_severity in vulnerability['counts_by_severity']:
            check(counts_by_severity, 'count', int)
            check(counts_by_severity, 'value', int)
        check(vulnerability, 'plugin_family', str)
        check(vulnerability, 'plugin_id', int)
        check(vulnerability, 'plugin_name', str)
        check(vulnerability, 'recasted_count', int)
        check(vulnerability, 'vulnerability_state', str)

@pytest.mark.vcr()
def test_workbench_vuln_info_age_typeerror(api):
    '''
    test to raise exception when type of age param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vuln_info(19506, age='none')


@pytest.mark.vcr()
def test_workbench_vuln_info_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vuln_info(19506, filter_type=123)


@pytest.mark.vcr()
def test_workbench_vuln_info_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vuln_info(19506, filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_vuln_info_plugin_id_typeerror(api):
    '''
    test to raise exception when type of plugin_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vuln_info('something')


@pytest.mark.vcr()
def test_workbench_vuln_info(api):
    '''
    test to get workbench vulnerability info
    '''
    vulns = api.workbenches.vulns()
    if vulns:
        info = api.workbenches.vuln_info(vulns[0]['plugin_id'])
        assert isinstance(info, dict)
        check(info, 'accepted_count', int)
        check(info, 'count', int)
        check(info, 'discovery', dict)
        check(info['discovery'], 'seen_first', 'datetime', allow_none=True)
        check(info['discovery'], 'seen_last', 'datetime', allow_none=True)
        check(info, 'plugin_details', dict)
        check(info['plugin_details'], 'family', str)
        check(info['plugin_details'], 'modification_date', 'datetime', allow_none=True)
        check(info['plugin_details'], 'name', str)
        check(info['plugin_details'], 'publication_date', 'datetime', allow_none=True)
        check(info['plugin_details'], 'severity', int)
        check(info['plugin_details'], 'type', str, allow_none=True)
        check(info['plugin_details'], 'version', str, allow_none=True)
        check(info, 'recasted_count', int)
        check(info, 'reference_information', list)
        check(info, 'risk_information', dict)
        check(info['risk_information'], 'cvss3_base_score', str, allow_none=True)
        check(info['risk_information'], 'cvss3_temporal_score', str, allow_none=True)
        check(info['risk_information'], 'cvss3_temporal_vector', str, allow_none=True)
        check(info['risk_information'], 'cvss3_vector', str, allow_none=True)
        check(info['risk_information'], 'cvss_base_score', str, allow_none=True)
        check(info['risk_information'], 'cvss_temporal_score', str, allow_none=True)
        check(info['risk_information'], 'cvss_temporal_vector', str, allow_none=True)
        check(info['risk_information'], 'cvss_vector', str, allow_none=True)
        check(info['risk_information'], 'risk_factor', str, allow_none=True)
        check(info['risk_information'], 'stig_severity', str, allow_none=True)
        check(info, 'see_also', list)
        check(info, 'severity', int)
        check(info, 'vuln_count', int)


@pytest.mark.vcr()
def test_workbench_vuln_outputs_age_typeerror(api):
    '''
    test to raise exception when type of age param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vuln_outputs(19506, age='none')


@pytest.mark.vcr()
def test_workbench_vuln_outputs_filter_type_typeerror(api):
    '''
    test to raise exception when type of filter_type param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vuln_outputs(19506, filter_type=123)


@pytest.mark.vcr()
def test_workbench_vuln_outputs_filter_type_unexpectedvalueerror(api):
    '''
    test to raise exception when filter_type param value does not match the choices.
    '''
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vuln_outputs(19506, filter_type='NOT')


@pytest.mark.vcr()
def test_workbench_vuln_outputs_plugin_id_typeerror(api):
    '''
    test to raise exception when type of plugin_id param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.vuln_outputs('something')


@pytest.mark.vcr()
def test_workbench_vuln_outputs(api):
    '''
    test to get workbench vulnerability output
    '''
    vulns = api.workbenches.vulns()
    if vulns:
        outputs = api.workbenches.vuln_outputs(vulns[0]['plugin_id'])
        assert isinstance(outputs, list)
        if outputs:
            output = outputs[0]
            check(output, 'plugin_output', str)
            check(output, 'states', list)
            for state in output['states']:
                check(state, 'name', str)
                check(state, 'results', list)
                for result in state['results']:
                    check(result, 'application_protocol', str, allow_none=True)
                    check(result, 'assets', list)
                    for asset in result['assets']:
                        check(asset, 'first_seen', 'datetime', allow_none=True)
                        check(asset, 'fqdn', str, allow_none=True)
                        check(asset, 'hostname', str)
                        check(asset, 'id', 'uuid')
                        check(asset, 'ipv4', str, allow_none=True)
                        check(asset, 'last_seen', 'datetime', allow_none=True)
                        check(asset, 'netbios_name', str, allow_none=True)
                        check(asset, 'uuid', 'uuid')
                    check(result, 'port', int)
                    check(result, 'severity', int)
                    check(result, 'transport_protocol', str)

@pytest.mark.vcr()
def test_workbenches_asset_delete_asset_uuid_typeerror(api):
    '''
    test to raise exception when type of uuid param does not match the expected type.
    '''
    with pytest.raises(TypeError):
        api.workbenches.asset_delete(1)


@pytest.mark.vcr()
@pytest.mark.skip('We don\'t want to delete asset')
def test_workbenches_asset_delete_success(api):
    '''
    test to delete asset
    '''
    asset = api.workbenches.assets()[0]
    api.workbenches.asset_delete(asset['id'])

@pytest.mark.vcr()
def test_workbench_assets_fields(api):
    '''
    test to get the workbench assets and verifying their types
    '''
    assets = api.workbenches.assets(all_fields=True,
                                    authenticated=True,
                                    exploitable=True,
                                    resolvable=True,
                                    severity='critical')
    assert isinstance(assets, list)
    asset = assets[0]
    check(asset, 'agent_name', list)
    check(asset, 'aws_availability_zone', list)
    check(asset, 'aws_ec2_instance_ami_id', list)
    check(asset, 'aws_ec2_instance_group_name', list)
    check(asset, 'aws_ec2_instance_id', list)
    check(asset, 'aws_ec2_instance_state_name', list)
    check(asset, 'aws_ec2_instance_type', list)
    check(asset, 'aws_ec2_name', list)
    check(asset, 'aws_ec2_product_code', list)
    check(asset, 'aws_owner_id', list)
    check(asset, 'aws_region', list)
    check(asset, 'aws_subnet_id', list)
    check(asset, 'aws_vpc_id', list)
    check(asset, 'azure_resource_id', list)
    check(asset, 'azure_vm_id', list)
    check(asset, 'bios_uuid', list)
    check(asset, 'created_at', 'datetime')
    check(asset, 'first_scan_time', 'datetime', allow_none=True)
    check(asset, 'first_seen', 'datetime', allow_none=True)
    check(asset, 'fqdn', list)
    check(asset, 'gcp_instance_id', list)
    check(asset, 'gcp_project_id', list)
    check(asset, 'gcp_zone', list)
    check(asset, 'has_agent', bool)
    check(asset, 'hostname', list)
    check(asset, 'id', 'uuid')
    check(asset, 'ipv4', list)
    check(asset, 'ipv6', list)
    check(asset, 'last_authenticated_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_licensed_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_scan_time', 'datetime', allow_none=True)
    check(asset, 'last_seen', 'datetime', allow_none=True)
    check(asset, 'mac_address', list)
    check(asset, 'manufacturer_tpm_id', list)
    check(asset, 'mcafee_epo_agent_guid', list)
    check(asset, 'mcafee_epo_guid', list)
    check(asset, 'netbios_name', list)
    check(asset, 'operating_system', list)
    check(asset, 'qualys_asset_id', list)
    check(asset, 'qualys_host_id', list)
    check(asset, 'servicenow_sysid', list)
    check(asset, 'sources', list)
    for source in asset['sources']:
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')
        check(source, 'name', str)
    check(asset, 'ssh_fingerprint', list)
    check(asset, 'symantec_ep_hardware_key', list)
    check(asset, 'system_type', list)
    check(asset, 'tags', list)
    check(asset, 'tenable_uuid', list)
    check(asset, 'terminated_at', 'datetime', allow_none=True)
    check(asset, 'terminated_by', str, allow_none=True)
    check(asset, 'updated_at', 'datetime')


@pytest.mark.vcr()
def test_workbenches_export_success(api):
    '''
    test to export the data from vulnerability workbench
    '''
    with open('example.nessus', 'wb') as fobj:
        api.workbenches.export(filter_type='or',
                               fobj=fobj)


@pytest.mark.vcr()
def test_workbench_vulns_fields(api):
    '''
    test to get the workbench vulnerabilities
    '''
    vulns = api.workbenches.vulns(authenticated=True,
                                  severity='medium',
                                  exploitable=True,
                                  resolvable=True)
    assert isinstance(vulns, list)
    each_vuln = vulns[0]
    check(each_vuln, 'accepted_count', int)
    check(each_vuln, 'counts_by_severity', list)
    for data in each_vuln['counts_by_severity']:
        check(data, 'count', int)
        check(data, 'value', int)
    check(each_vuln, 'plugin_family', str)
    check(each_vuln, 'plugin_id', int)
    check(each_vuln, 'plugin_name', str)
    check(each_vuln, 'recasted_count', int)
    check(each_vuln, 'vulnerability_state', str)


@pytest.mark.vcr()
def test_workbench_asset_info_success(api):
    '''
    test to get the asset information
    '''
    asset = api.workbenches.assets()
    api.workbenches.asset_info(asset[0]['id'], all_fields=False)



@pytest.mark.vcr()
def test_workbench_assets_fields(api):
    '''
    test to get the workbench assets and verifying their types
    '''
    assets = api.workbenches.assets(all_fields=True,
                                    authenticated=True,
                                    exploitable=True,
                                    resolvable=True,
                                    severity='critical')
    assert isinstance(assets, list)
    asset = assets[0]
    check(asset, 'agent_name', list)
    check(asset, 'aws_availability_zone', list)
    check(asset, 'aws_ec2_instance_ami_id', list)
    check(asset, 'aws_ec2_instance_group_name', list)
    check(asset, 'aws_ec2_instance_id', list)
    check(asset, 'aws_ec2_instance_state_name', list)
    check(asset, 'aws_ec2_instance_type', list)
    check(asset, 'aws_ec2_name', list)
    check(asset, 'aws_ec2_product_code', list)
    check(asset, 'aws_owner_id', list)
    check(asset, 'aws_region', list)
    check(asset, 'aws_subnet_id', list)
    check(asset, 'aws_vpc_id', list)
    check(asset, 'azure_resource_id', list)
    check(asset, 'azure_vm_id', list)
    check(asset, 'bios_uuid', list)
    check(asset, 'created_at', 'datetime')
    check(asset, 'first_scan_time', 'datetime', allow_none=True)
    check(asset, 'first_seen', 'datetime', allow_none=True)
    check(asset, 'fqdn', list)
    check(asset, 'gcp_instance_id', list)
    check(asset, 'gcp_project_id', list)
    check(asset, 'gcp_zone', list)
    check(asset, 'has_agent', bool)
    check(asset, 'hostname', list)
    check(asset, 'id', 'uuid')
    check(asset, 'ipv4', list)
    check(asset, 'ipv6', list)
    check(asset, 'last_authenticated_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_licensed_scan_date', 'datetime', allow_none=True)
    check(asset, 'last_scan_time', 'datetime', allow_none=True)
    check(asset, 'last_seen', 'datetime', allow_none=True)
    check(asset, 'mac_address', list)
    check(asset, 'manufacturer_tpm_id', list)
    check(asset, 'mcafee_epo_agent_guid', list)
    check(asset, 'mcafee_epo_guid', list)
    check(asset, 'netbios_name', list)
    check(asset, 'operating_system', list)
    check(asset, 'qualys_asset_id', list)
    check(asset, 'qualys_host_id', list)
    check(asset, 'servicenow_sysid', list)
    check(asset, 'sources', list)
    for source in asset['sources']:
        check(source, 'first_seen', 'datetime')
        check(source, 'last_seen', 'datetime')
        check(source, 'name', str)
    check(asset, 'ssh_fingerprint', list)
    check(asset, 'symantec_ep_hardware_key', list)
    check(asset, 'system_type', list)
    check(asset, 'tags', list)
    check(asset, 'tenable_uuid', list)
    check(asset, 'terminated_at', 'datetime', allow_none=True)
    check(asset, 'terminated_by', str, allow_none=True)
    check(asset, 'updated_at', 'datetime')


@pytest.mark.vcr()
def test_workbenches_export_success(api):
    '''
    test to export the data from vulnerability workbench
    '''
    with open('example.nessus', 'wb') as fobj:
        api.workbenches.export(filter_type='or',
                               fobj=fobj)


@pytest.mark.vcr()
def test_workbench_vulns_fields(api):
    '''
    test to get the workbench vulnerabilities
    '''
    vulns = api.workbenches.vulns(authenticated=True,
                                  severity='medium',
                                  exploitable=True,
                                  resolvable=True)
    assert isinstance(vulns, list)
    each_vuln = vulns[0]
    check(each_vuln, 'accepted_count', int)
    check(each_vuln, 'counts_by_severity', list)
    for data in each_vuln['counts_by_severity']:
        check(data, 'count', int)
        check(data, 'value', int)
    check(each_vuln, 'plugin_family', str)
    check(each_vuln, 'plugin_id', int)
    check(each_vuln, 'plugin_name', str)
    check(each_vuln, 'recasted_count', int)
    check(each_vuln, 'vulnerability_state', str)


@pytest.mark.vcr()
def test_workbench_asset_info_success(api):
    '''
    test to get the asset information
    '''
    asset = api.workbenches.assets()
    api.workbenches.asset_info(asset[0]['id'], all_fields=False)
