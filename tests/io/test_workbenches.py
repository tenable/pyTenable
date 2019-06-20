from tenable.errors import *
from ..checker import check, single
from io import BytesIO
import uuid, pytest

@pytest.mark.vcr()
def test_workbench_assets_age_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.assets(age='onetwothree')

@pytest.mark.vcr()
def test_workbench_assets_filter_tyype_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.assets(filter_type=1)

@pytest.mark.vcr()
def test_workbench_assets_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.assets(filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_assets(api):
    assets = api.workbenches.assets()
    assert isinstance(assets, list)
    a = assets[0]
    check(a, 'agent_name', list)
    check(a, 'aws_availability_zone', list)
    check(a, 'aws_ec2_instance_ami_id', list)
    check(a, 'aws_ec2_instance_group_name', list)
    check(a, 'aws_ec2_instance_id', list)
    check(a, 'aws_ec2_instance_state_name', list)
    check(a, 'aws_ec2_instance_type', list)
    check(a, 'aws_ec2_name', list)
    check(a, 'aws_ec2_product_code', list)
    check(a, 'aws_owner_id', list)
    check(a, 'aws_region', list)
    check(a, 'aws_subnet_id', list)
    check(a, 'aws_vpc_id', list)
    check(a, 'azure_resource_id', list)
    check(a, 'azure_vm_id', list)
    check(a, 'bios_uuid', list)
    check(a, 'created_at', 'datetime')
    check(a, 'first_scan_time', 'datetime', allow_none=True)
    check(a, 'first_seen', 'datetime', allow_none=True)
    check(a, 'fqdn', list)
    check(a, 'gcp_instance_id', list)
    check(a, 'gcp_project_id', list)
    check(a, 'gcp_zone', list)
    check(a, 'has_agent', bool)
    check(a, 'has_plugin_results', bool)
    check(a, 'hostname', list)
    check(a, 'id', 'uuid')
    check(a, 'ipv4', list)
    check(a, 'ipv6', list)
    check(a, 'last_authenticated_scan_date', 'datetime', allow_none=True)
    check(a, 'last_licensed_scan_date', 'datetime', allow_none=True)
    check(a, 'last_scan_time', 'datetime', allow_none=True)
    check(a, 'last_seen', 'datetime', allow_none=True)
    check(a, 'mac_address', list)
    check(a, 'manufacturer_tpm_id', list)
    check(a, 'mcafee_epo_agent_guid', list)
    check(a, 'mcafee_epo_guid', list)
    check(a, 'netbios_name', list)
    check(a, 'operating_system', list)
    check(a, 'qualys_asset_id', list)
    check(a, 'qualys_host_id', list)
    check(a, 'servicenow_sysid', list)
    check(a, 'sources', list)
    for i in a['sources']:
        check(i, 'first_seen', 'datetime')
        check(i, 'last_seen', 'datetime')
        check(i, 'name', str)
    check(a, 'ssh_fingerprint', list)
    check(a, 'symantec_ep_hardware_key', list)
    check(a, 'system_type', list)
    check(a, 'tags', list)
    check(a, 'tenable_uuid', list)
    check(a, 'terminated_at', 'datetime', allow_none=True)
    check(a, 'terminated_by', str, allow_none=True)
    check(a, 'updated_at', 'datetime')

@pytest.mark.vcr()
def test_workbench_assets_filtered(api):
    assets = api.workbenches.assets(('operating_system', 'match', 'Linux'))
    assert isinstance(assets, list)

@pytest.mark.vcr()
def test_workbench_assets_bad_filter(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.assets(('operating_system', 'contains', 'Linux'))

@pytest.mark.vcr()
def test_workbench_asset_activity_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_activity(1)

@pytest.mark.vcr()
def test_workbench_asset_activity_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_activity('This should fail')

@pytest.mark.vcr()
def test_workbench_asset_activity(api):
    assets = api.workbenches.assets()
    history = api.workbenches.asset_activity(assets[0]['id'])
    assert isinstance(history, list)
    for i in history:
        check(i, 'timestamp', 'datetime')
        check(i, 'type', str)
        if i['type'] in ['tagging', 'updated']:
            check(i, 'updates', list)
            for j in i['updates']:
                check(j, 'method', str)
                check(j, 'property', str)
                check(j, 'value', str)
        if i['type'] == 'discovered':
            check(i, 'details', dict)
            check(i['details'], 'assetId', 'uuid')
            check(i['details'], 'createdAt', 'datetime')
            check(i['details'], 'firstScanTime', 'datetime')
            check(i['details'], 'hasAgent', bool)
            check(i['details'], 'hasPluginResults', bool)
            check(i['details'], 'lastLicensedScanTime', 'datetime')
            check(i['details'], 'lastScanTime', 'datetime')
            check(i['details'], 'properties', dict)
            for j in i['details']['properties'].keys():
                check(i['details']['properties'][j], 'lastObserved', 'datetime')
                check(i['details']['properties'][j], 'values', list)
            check(i['details'], 'sources', list)
            for j in i['details']['sources']:
                check(j, 'firstSeen', 'datetime')
                check(j, 'lastSeen', 'datetime')
                check(j, 'name', str)
            check(i['details'], 'updatedAt', 'datetime')
        if i['type'] in ['discovered', 'seen', 'updated']:
            check(i, 'scan_id', 'scanner-uuid')
            check(i, 'schedule_id', 'scanner-uuid')
            check(i, 'source', str)

@pytest.mark.vcr()
def test_workbench_asset_info_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_info(1)

@pytest.mark.vcr()
def test_workbench_asset_info_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_info('abnc-1234-somethinginvalid')

@pytest.mark.vcr()
def test_workbench_asset_info_all_fields_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_info('', all_fields='one')

@pytest.mark.vcr()
def test_workbench_asset_info(api):
    assets = api.workbenches.assets()
    asset = api.workbenches.asset_info(assets[0]['id'])

@pytest.mark.vcr()
def test_workbench_asset_vulns_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vulns(1)

@pytest.mark.vcr()
def test_workbench_asset_vulns_age_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vulns(str(uuid.uuid4()), age='none')

@pytest.mark.vcr()
def test_workbench_asset_vulns_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vulns(str(uuid.uuid4()), filter_type=123)

@pytest.mark.vcr()
def test_workbench_asset_vulns_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vulns(str(uuid.uuid4()), filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_asset_vulns_invalid_filter(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vulns(str(uuid.uuid4()),
            ('operating_system', 'contains', 'Linux'))

@pytest.mark.vcr()
def test_workbench_asset_vulns(api):
    assets = api.workbenches.assets()
    vulns = api.workbenches.asset_vulns(assets[0]['id'])
    assert isinstance(vulns, list)
    v = vulns[0]
    check(v, 'accepted_count', int)
    check(v, 'count', int)
    check(v, 'counts_by_severity', list)
    for i in v['counts_by_severity']:
        check(i, 'count', int)
        check(i, 'value', int)
    check(v, 'plugin_family', str)
    check(v, 'plugin_id', int)
    check(v, 'plugin_name', str)
    check(v, 'severity', int)
    check(v, 'vulnerability_state', str)

@pytest.mark.vcr()
def test_workbench_asset_vulns_filtered(api):
    assets = api.workbenches.assets()
    vulns = api.workbenches.asset_vulns(assets[0]['id'],
        ('severity', 'eq', 'Info'))
    assert isinstance(vulns, list)
    v = vulns[0]
    check(v, 'accepted_count', int)
    check(v, 'count', int)
    check(v, 'counts_by_severity', list)
    for i in v['counts_by_severity']:
        check(i, 'count', int)
        check(i, 'value', int)
    check(v, 'plugin_family', str)
    check(v, 'plugin_id', int)
    check(v, 'plugin_name', str)
    check(v, 'severity', int)
    check(v, 'vulnerability_state', str)

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(1, 1)

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_info('this is not a valid UUID', 1234)

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 'something here')

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_age_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506, age='none')

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506, filter_type=123)

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506, filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_asset_vuln_info_invalid_filter(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_info(str(uuid.uuid4()), 19506,
            ('operating_system', 'contains', 'Linux'))

@pytest.mark.vcr()
def test_workbench_asset_vuln_info(api):
    assets = api.workbenches.assets()
    info = api.workbenches.asset_vuln_info(assets[0]['id'], 19506)
    check(info, 'count', int)
    check(info, 'description', str)
    check(info, 'discovery', dict)
    check(info['discovery'], 'seen_first', 'datetime')
    check(info['discovery'], 'seen_last', 'datetime')
    check(info, 'plugin_details', dict)
    check(info['plugin_details'], 'family', str)
    check(info['plugin_details'], 'modification_date', 'datetime')
    check(info['plugin_details'], 'name', str)
    check(info['plugin_details'], 'publication_date', 'datetime')
    check(info['plugin_details'], 'severity', int)
    check(info['plugin_details'], 'type', str)
    check(info['plugin_details'], 'version', str)
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
    check(info, 'synopsis', str)
    check(info, 'vuln_count', int)

@pytest.mark.vcr()
def test_workbench_asset_vuln_output_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(1, 1)

@pytest.mark.vcr()
def test_workbench_asset_vuln_output_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_output('this is not a valid UUID', 1234)

@pytest.mark.vcr()
def test_workbench_asset_vuln_output_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 'something here')

@pytest.mark.vcr()
def test_workbench_asset_vuln_output_age_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, age='none')

@pytest.mark.vcr()
def test_workbench_asset_vuln_output_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, filter_type=123)

@pytest.mark.vcr()
def test_workbench_asset_vuln_output_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506, filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_asset_vuln_output_invalid_filter(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.asset_vuln_output(str(uuid.uuid4()), 19506,
            ('operating_system', 'contains', 'Linux'))

@pytest.mark.vcr()
def test_workbench_asset_vuln_output(api):
    assets = api.workbenches.assets()
    outputs = api.workbenches.asset_vuln_output(assets[0]['id'], 19506)
    assert isinstance(outputs, list)
    o = outputs[0]
    check(o, 'plugin_output', str)
    check(o, 'states', list)
    for i in o['states']:
        check(i, 'name', str)
        check(i, 'results', list)
        for j in i['results']:
            check(j, 'application_protocol', str, allow_none=True)
            check(j, 'assets', list)
            for k in j['assets']:
                check(k, 'first_seen', 'datetime')
                check(k, 'fqdn', str, allow_none=True)
                check(k, 'hostname', str)
                check(k, 'id', 'uuid')
                check(k, 'ipv4', str, allow_none=True)
                check(k, 'last_seen', 'datetime')
                check(k, 'netbios_name', str, allow_none=True)
                check(k, 'uuid', 'uuid')
            check(j, 'port', int)
            check(j, 'severity', int)
            check(j, 'transport_protocol', str)

@pytest.mark.vcr()
def test_workbench_vuln_assets(api):
    assets = api.workbenches.vuln_assets()
    assert isinstance(assets, list)
    a = assets[0]
    check(a, 'agent_name', list)
    check(a, 'fqdn', list)
    check(a, 'id', 'uuid')
    check(a, 'ipv4', list)
    check(a, 'ipv6', list)
    check(a, 'last_seen', 'datetime')
    check(a, 'netbios_name', list)
    check(a, 'severities', list)
    for i in a['severities']:
        check(i, 'count', int)
        check(i, 'level', int)
        check(i, 'name', str)
    check(a, 'total', int)

@pytest.mark.vcr()
def test_workbench_export_asset_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.export(asset_uuid=123)

@pytest.mark.vcr()
def test_workbench_export_asset_uuid_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(asset_uuid='something')

@pytest.mark.vcr()
def test_workbench_export_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.export(plugin_id='something')

@pytest.mark.vcr()
def test_workbench_export_format_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.export(format=1234)

@pytest.mark.vcr()
def test_workbench_export_format_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(format='something else')

@pytest.mark.vcr()
def test_workbench_export_chapters_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.export(format='html', chapters='diff')

@pytest.mark.vcr()
def test_workbench_export_chapters_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(format='html', chapters=['something'])

@pytest.mark.vcr()
def test_workbench_export_missing_chapters(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(format='html')

@pytest.mark.vcr()
def test_workbench_export_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.export(filter_type=1)

@pytest.mark.vcr()
def test_workbench_export_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.export(filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_export(api):
    fobj = api.workbenches.export()
    assert isinstance(fobj, BytesIO)

@pytest.mark.vcr()
def test_workbench_export_plugin_id(api):
    fobj = api.workbenches.export(plugin_id=19506)
    assert isinstance(fobj, BytesIO)

@pytest.mark.vcr()
def test_workbench_export_asset_uuid(api):
    assets = api.workbenches.assets()
    fobj = api.workbenches.export(asset_uuid=assets[0]['id'])
    assert isinstance(fobj, BytesIO)

@pytest.mark.vcr()
def test_workbench_vulns_age_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vulns(age='none')

@pytest.mark.vcr()
def test_workbench_vulns_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vulns(filter_type=123)

@pytest.mark.vcr()
def test_workbench_vulns_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vulns(filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_vulns_invalid_filter(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vulns(('nothing here', 'contains', 'Linux'))

@pytest.mark.vcr()
def test_workbench_vulns_authenticated_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vulns(authenticated='nope')

@pytest.mark.vcr()
def test_workbench_vulns_exploitable_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vulns(exploitable='nope')

@pytest.mark.vcr()
def test_workbench_vulns_resolvable_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vulns(resolvable='nope')

@pytest.mark.vcr()
def test_workbench_vulns_severity_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vulns(severity=['low'])

@pytest.mark.vcr()
def test_workbench_vulns_severity_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vulns(severity='something else')

@pytest.mark.vcr()
def test_workbench_vulns(api):
    vulns = api.workbenches.vulns()
    assert isinstance(vulns, list)
    v = vulns[0]
    check(v, 'accepted_count', int)
    check(v, 'counts_by_severity', list)
    for i in v['counts_by_severity']:
        check(i, 'count', int)
        check(i, 'value', int)
    check(v, 'plugin_family', str)
    check(v, 'plugin_id', int)
    check(v, 'plugin_name', str)
    check(v, 'recasted_count', int)
    check(v, 'vulnerability_state', str)

@pytest.mark.vcr()
def test_workbench_vuln_info_age_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vuln_info(19506, age='none')

@pytest.mark.vcr()
def test_workbench_vuln_info_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vuln_info(19506, filter_type=123)

@pytest.mark.vcr()
def test_workbench_vuln_info_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vuln_info(19506, filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_vuln_info_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vuln_info('something')

@pytest.mark.vcr()
def test_workbench_vuln_info(api):
    info = api.workbenches.vuln_info(19506)
    assert isinstance(info, dict)
    check(info, 'count', int)
    check(info, 'description', str)
    check(info, 'discovery', dict)
    check(info['discovery'], 'seen_first', 'datetime')
    check(info['discovery'], 'seen_last', 'datetime')
    check(info, 'plugin_details', dict)
    check(info['plugin_details'], 'family', str)
    check(info['plugin_details'], 'modification_date', 'datetime')
    check(info['plugin_details'], 'name', str)
    check(info['plugin_details'], 'publication_date', 'datetime')
    check(info['plugin_details'], 'severity', int)
    check(info['plugin_details'], 'type', str)
    check(info['plugin_details'], 'version', str)
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
    check(info, 'synopsis', str)
    check(info, 'vuln_count', int)

@pytest.mark.vcr()
def test_workbench_vuln_outputs_age_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vuln_outputs(19506, age='none')

@pytest.mark.vcr()
def test_workbench_vuln_outputs_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vuln_outputs(19506, filter_type=123)

@pytest.mark.vcr()
def test_workbench_vuln_outputs_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.workbenches.vuln_outputs(19506, filter_type='NOT')

@pytest.mark.vcr()
def test_workbench_vuln_outputs_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.vuln_outputs('something')

@pytest.mark.vcr()
def test_workbench_vuln_outputs(api):
    outputs = api.workbenches.vuln_outputs(19506)
    assert isinstance(outputs, list)
    o = outputs[0]
    check(o, 'plugin_output', str)
    check(o, 'states', list)
    for i in o['states']:
        check(i, 'name', str)
        check(i, 'results', list)
        for j in i['results']:
            check(j, 'application_protocol', str, allow_none=True)
            check(j, 'assets', list)
            for k in j['assets']:
                check(k, 'first_seen', 'datetime')
                check(k, 'fqdn', str, allow_none=True)
                check(k, 'hostname', str)
                check(k, 'id', 'uuid')
                check(k, 'ipv4', str, allow_none=True)
                check(k, 'last_seen', 'datetime')
                check(k, 'netbios_name', str, allow_none=True)
                check(k, 'uuid', 'uuid')
            check(j, 'port', int)
            check(j, 'severity', int)
            check(j, 'transport_protocol', str)

@pytest.mark.vcr()
def test_workbenches_asset_delete_asset_uuid_typeerror(api):
    with pytest.raises(TypeError):
        api.workbenches.asset_delete(1)

@pytest.mark.vcr()
def test_workbenches_asset_delete_success(api):
    asset = api.workbenches.assets()[0]
    api.workbenches.asset_delete(asset['id'])