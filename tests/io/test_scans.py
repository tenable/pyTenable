from tenable.errors import *
from ..checker import check, single
from .conftest import SCAN_ID_WITH_RESULTS
import uuid, time, pytest, os

@pytest.mark.vcr()
def test_scan_create_scan_document_template_typeerror(api):
    with pytest.raises(TypeError):
        api.scans._create_scan_document({'template': 123})

@pytest.mark.vcr()
def test_scan_create_scan_document_template_unexpected_value_error(api):
    with pytest.raises(UnexpectedValueError):
        api.scans._create_scan_document({'template': 'nothing_here'})

@pytest.mark.vcr()
def test_scan_create_scan_socument_template_pass(api):
    templates = api.policies.templates()
    resp = api.scans._create_scan_document({'template': 'basic'})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    assert resp['uuid'] == templates['basic']

@pytest.mark.vcr()
def test_scan_create_scan_document_policies_id_pass(api):
    policies = api.policies.list()
    p = policies[0]
    resp = api.scans._create_scan_document({'policy': p['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == p['id']

@pytest.mark.vcr()
def test_scan_create_scan_document_policies_name_pass(api):
    policies = api.policies.list()
    p = policies[0]
    resp = api.scans._create_scan_document({'policy': p['name']})
    assert isinstance(resp, dict)
    check(resp, 'uuid', 'scanner-uuid')
    check(resp, 'settings', dict)
    check(resp['settings'], 'policy_id', int)
    assert resp['settings']['policy_id'] == p['id']

#def test_scan_create_scan_document_targets

@pytest.mark.vcr()
def test_scan_create_scan_document_scanner_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.scans._create_scan_document({'scanner': 'nothing to see here'})

@pytest.mark.vcr()
def test_scan_create_scan_document_scanner_uuid_pass(api):
    scanners = api.scanners.allowed_scanners()
    s = scanners[0]
    resp = api.scans._create_scan_document({'scanner': s['id']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', 'scanner-uuid')
    assert resp['settings']['scanner_id'] == s['id']

@pytest.mark.vcr()
def test_scan_create_scan_document_scanner_name_pass(api):
    scanners = api.scanners.allowed_scanners()
    s = scanners[0]
    resp = api.scans._create_scan_document({'scanner': s['name']})
    assert isinstance(resp, dict)
    check(resp, 'settings', dict)
    check(resp['settings'], 'scanner_id', str)
    assert resp['settings']['scanner_id'] == s['id']

@pytest.mark.vcr()
def test_scan_attachment_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.attachment('nope', 1)

@pytest.mark.vcr()
def test_scan_attachment_attachement_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.attachment(1, 'nope')

@pytest.mark.vcr()
@pytest.mark.xfail(raises=InvalidInputError)
def test_scan_attachement_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.attachment(1, 1, 'none')

@pytest.mark.vcr()
def test_scan_configure_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.configure('abc123')

@pytest.mark.vcr()
def test_scan_configure_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.configure('nope')

@pytest.mark.vcr()
def test_scan_configure_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.configure(1, name=str(uuid.uuid4()))

@pytest.mark.vcr()
def test_scan_configure(api, scan):
    mod = api.scans.configure(scan['id'], name='MODIFIED')
    assert mod['id'] == scan['id']
    assert mod['name'] == 'MODIFIED'

@pytest.mark.vcr()
def test_scan_copy_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.copy('nope')

@pytest.mark.vcr()
def test_scan_copy_folder_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.copy(1, folder_id='nope')

@pytest.mark.vcr()
def test_scan_copy_name_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.copy(1, name=1)

@pytest.mark.vcr()
def test_scan_copy_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.copy(1)

@pytest.mark.vcr()
def test_scan_copy(api, scan):
    clone = api.scans.copy(scan['id'])
    assert isinstance(clone, dict)
    check(clone, 'control', bool)
    check(clone, 'creation_date', int)
    check(clone, 'enabled', bool)
    check(clone, 'id', int)
    check(clone, 'last_modification_date', int)
    check(clone, 'owner', str)
    check(clone, 'name', str)
    check(clone, 'read', bool)
    check(clone, 'rrules', str, allow_none=True)
    # This is in the documentation, however isn't always returned oddly.
    #check(clone, 'schedule_uuid', 'scanner-uuid')
    check(clone, 'shared', bool)
    check(clone, 'starttime', str, allow_none=True)
    check(clone, 'status', str)
    check(clone, 'timezone', str, allow_none=True)
    check(clone, 'user_permissions', int)
    check(clone, 'uuid', 'scanner-uuid')

@pytest.mark.vcr()
def test_scan_create_no_template_pass(api, scan):
    assert isinstance(scan, dict)
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)

@pytest.mark.vcr()
def test_scan_create_was_scan_pass(api):
    scan = api.scans.create(template='was_scan', name=str(uuid.uuid4()),
        plugins={
            'Authentication & Session': {'status': 'enabled'},
            'Code Execution': {'status': 'enabled'},
            'Component Vulnerability': {'status': 'enabled'},
            'Cross Site Request Forgery': {'status': 'enabled'},
            'Cross Site Scripting': {'status': 'enabled'},
            'Data Exposure': {'status': 'enabled'},
            'File Inclusion': {'status': 'enabled'},
            'Injection': {'status': 'enabled'},
            'Web Applications': {'status': 'enabled'},
            'Web Servers': {'status': 'enabled'},
        },
        assessment_mode='Quick',
        targets=['http://127.0.0.1:3000'],
        was_timeout='00:05:00'
    )
    check(scan, 'creation_date', int)
    check(scan, 'custom_targets', str)
    check(scan, 'default_permissions', int)
    check(scan, 'description', str, allow_none=True)
    check(scan, 'emails', str, allow_none=True)
    check(scan, 'enabled', bool)
    check(scan, 'id', int)
    check(scan, 'last_modification_date', int)
    check(scan, 'owner', str)
    check(scan, 'owner_id', int)
    check(scan, 'policy_id', int)
    check(scan, 'name', str)
    check(scan, 'rrules', str, allow_none=True)
    check(scan, 'scanner_id', 'scanner-uuid', allow_none=True)
    check(scan, 'shared', int)
    check(scan, 'starttime', str, allow_none=True)
    check(scan, 'timezone', str, allow_none=True)
    check(scan, 'type', str)
    check(scan, 'user_permissions', int)
    check(scan, 'uuid', str)

@pytest.mark.vcr()
def test_scan_delete_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.delete('nope')

@pytest.mark.vcr()
def test_scan_delete_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.delete(0)

@pytest.mark.vcr()
def test_scan_delete(api, scan):
    api.scans.delete(scan['id'])

@pytest.mark.vcr()
def test_scan_delete_history_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.delete_history('nope', 1)

@pytest.mark.vcr()
def test_scan_delete_history_history_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.delete_history(1, 'nope')

@pytest.mark.vcr()
def test_scan_delete_history_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.delete_history(1, 1)

@pytest.mark.vcr()
def test_scan_details_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.details('nope')

@pytest.mark.vcr()
def test_scan_details_history_it_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.details(1, 'nope')

@pytest.mark.vcr()
def test_scan_results(api, scan_results):
    assert isinstance(scan_results, dict)
    s = scan_results
    check(s, 'info', dict)
    info = s['info']
    check(info, 'acls', list, allow_none=True)
    for i in s['info']['acls']:
        check(i, 'owner', int, allow_none=True)
        check(i, 'type', str, allow_none=True)
        check(i, 'permissions', int, allow_none=True)
        check(i, 'id', int, allow_none=True)
        check(i, 'name', str, allow_none=True)
        check(i, 'display_name', str, allow_none=True)
    check(info, 'schedule_uuid', 'scanner-uuid', allow_none=True)
    check(info, 'edit_allowed', bool)
    check(info, 'status', str)
    check(info, 'alt_targets_used', str, allow_none=True)
    check(info, 'scanner_start', int, allow_none=True)
    check(info, 'policy', str, allow_none=True)
    check(info, 'pci-can-upload', bool, allow_none=True)
    check(info, 'scan_start', int, allow_none=True)
    check(info, 'hasaudittrail', bool)
    check(info, 'user_permissions', int)
    check(info, 'folder_id', int, allow_none=True)
    check(info, 'no_target', bool)
    check(info, 'owner', str)
    check(info, 'targets', str, allow_none=True)
    check(info, 'control', bool)
    check(info, 'object_id', int)
    check(info, 'scanner_name', str, allow_none=True)
    check(info, 'uuid', str)
    check(info, 'haskb', bool)
    check(info, 'scanner_end', int, allow_none=True)
    check(info, 'scan_end', int)
    check(info, 'hostcount', int)
    check(info, 'scan_type', str, allow_none=True)
    check(info, 'name', str)

    check(s, 'comphosts', list)
    for i in s['comphosts']:
        check(i, 'totalchecksconsidered', int)
        check(i, 'numchecksconsidered', int)
        check(i, 'scanprogresstotal', int)
        check(i, 'scanprogresscurrent', int)
        check(i, 'host_index', int)
        check(i, 'score', int)
        check(i, 'severitycount', dict)
        check(i, 'progress', str)
        check(i, 'critical', int)
        check(i, 'high', int)
        check(i, 'medium', int)
        check(i, 'low', int)
        check(i, 'info', int)
        check(i, 'host_id', int)
        check(i, 'hostname', str)

    check(s, 'hosts', list)
    for i in s['hosts']:
        check(i, 'totalchecksconsidered', int)
        check(i, 'numchecksconsidered', int)
        check(i, 'scanprogresstotal', int)
        check(i, 'scanprogresscurrent', int)
        check(i, 'host_index', int)
        check(i, 'score', int)
        check(i, 'severitycount', dict)
        check(i, 'progress', str)
        check(i, 'critical', int)
        check(i, 'high', int)
        check(i, 'medium', int)
        check(i, 'low', int)
        check(i, 'info', int)
        check(i, 'host_id', int)
        check(i, 'hostname', str)

    check(s, 'notes', list)
    for i in s['notes']:
        check(i, 'title', str)
        check(i, 'message', str)
        check(i, 'severity', int)

    check(s, 'remediations', dict)
    check(s['remediations'], 'num_hosts', int)
    check(s['remediations'], 'num_cves', int)
    check(s['remediations'], 'num_impacted_hosts', int)
    check(s['remediations'], 'num_remediated_cves', int)
    check(s['remediations'], 'remediations', list)
    for i in s['remediations']['remediations']:
        check(i, 'value', str)
        check(i, 'remediation', str)
        check(i, 'hosts', int)
        check(i, 'vulns', int)

    check(s, 'vulnerabilities', list)
    for i in s['vulnerabilities']:
        check(i, 'count', int)
        check(i, 'plugin_name', str)
        check(i, 'vuln_index', int)
        check(i, 'severity', int)
        check(i, 'plugin_id', int)
        # Mentioned in the docs, however doesn't appear to show in testing
        #check(i, 'severity_index', int)
        check(i, 'plugin_family', str)

    check(s, 'history', list)
    for i in s['history']:
        check(i, 'alt_targets_used', bool)
        check(i, 'scheduler', int)
        check(i, 'status', str)
        check(i, 'type', str, allow_none=True)
        check(i, 'uuid', str)
        check(i, 'last_modification_date', int)
        check(i, 'creation_date', int)
        check(i, 'owner_id', int)
        check(i, 'history_id', int)

    check(s, 'compliance', list)
    for i in s['compliance']:
        check(i, 'count', int)
        check(i, 'plugin_name', str)
        check(i, 'vuln_index', int)
        check(i, 'severity', int)
        check(i, 'plugin_id', int)
        # Mentioned in the docs, however doesn't appear to show in testing
        #check(i, 'severity_index', int)
        check(i, 'plugin_family', str)

@pytest.mark.vcr()
def test_scan_export_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.export('nope')

@pytest.mark.vcr()
def test_scan_export_history_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.export(1, history_id='nope')

@pytest.mark.vcr()
def test_scan_export_format_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.export(1, format=1)

@pytest.mark.vcr()
def test_scan_export_format_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.scans.export(1, format='something else')

@pytest.mark.vcr()
def test_scan_export_password_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.export(1, password=1)

@pytest.mark.vcr()
def test_scan_export_chapters_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.export(1, chapters=1)

@pytest.mark.vcr()
def test_scan_export_chapters_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.scans.export(1, chapters=['nothing to see here'])

@pytest.mark.vcr()
def test_scan_export_filter_type_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.export(1, filter_type=1)

@pytest.mark.vcr()
def test_scan_export_filter_type_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.scans.export(1, filter_type='nothing')

@pytest.mark.vcr()
def test_scan_export_was_typeerror(api):
    with pytest.raises(UnexpectedValueError):
      api.scans.export(SCAN_ID_WITH_RESULTS, scan_type='bad-value')

@pytest.mark.vcr()
def test_scan_export_was(api):
    api.scans.export(SCAN_ID_WITH_RESULTS, scan_type='web-app')

@pytest.mark.vcr()
def test_scan_export_bytesio(api):
    from io import BytesIO
    from tenable.reports.nessusv2 import NessusReportv2
    fobj = api.scans.export(SCAN_ID_WITH_RESULTS)
    assert isinstance(fobj, BytesIO)

    counter = 0
    for i in NessusReportv2(fobj):
        counter += 1
        if counter > 10:
            break

@pytest.mark.vcr()
def test_scan_export_file_object(api):
    from tenable.reports.nessusv2 import NessusReportv2
    fn = '{}.nessus'.format(uuid.uuid4())
    with open(fn, 'wb') as fobj:
        api.scans.export(SCAN_ID_WITH_RESULTS, fobj=fobj)

    with open(fn, 'rb') as fobj:
        counter = 0
        for i in NessusReportv2(fobj):
            counter += 1
            if counter > 10:
                break
    os.remove(fn)

@pytest.mark.vcr()
def test_scan_host_details_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.host_details('nope', 1)

@pytest.mark.vcr()
def test_scan_host_details_host_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.host_details(1, 'nope')

@pytest.mark.vcr()
def test_scan_host_details_history_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.host_details(1, 1, 'nope')

@pytest.mark.vcr()
def test_scan_host_details_notfounderror(api):
    with pytest.raises(NotFoundError):
        api.scans.host_details(1, 1)

@pytest.mark.vcr()
def test_scan_host_details(api, scan_results):
    host = api.scans.host_details(
        SCAN_ID_WITH_RESULTS, scan_results['hosts'][0]['asset_id'])
    assert isinstance(host, dict)
    check(host, 'info', dict)
    check(host['info'], 'host-fqdn', str, allow_none=True)
    check(host['info'], 'host_end', str)
    check(host['info'], 'host_start', str)
    check(host['info'], 'operating-system', list)
    check(host['info'], 'host-ip', str)
    check(host['info'], 'mac-address', str, allow_none=True)

    check(host, 'vulnerabilities', list)
    for i in host['vulnerabilities']:
        check(i, 'count', int)
        check(i, 'severity', int)
        check(i, 'plugin_family', str)
        check(i, 'hostname', str)
        check(i, 'plugin_name', str)
        check(i, 'severity_index', int)
        check(i, 'vuln_index', int)
        check(i, 'host_id', int)
        check(i, 'plugin_id', int)

    check(host, 'compliance', list)
    for i in host['compliance']:
        check(i, 'count', int)
        check(i, 'plugin_name', str)
        check(i, 'vuln_index', int)
        check(i, 'severity', int)
        check(i, 'plugin_id', int)
        check(i, 'severity_index', int)
        check(i, 'plugin_family', str)

@pytest.mark.vcr()
def test_scan_import_scan_folder_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.import_scan(None, folder_id='nope')

@pytest.mark.vcr()
def test_scan_import_scan_password_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.import_scan(None, password=1)

@pytest.mark.vcr()
def test_scan_import_scan(api):
    fobj = api.scans.export(SCAN_ID_WITH_RESULTS)
    api.scans.import_scan(fobj)

@pytest.mark.vcr()
def test_scan_launch_scanid_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.launch('nope')

@pytest.mark.vcr()
def test_scan_launch_targets_typerror(api):
    with pytest.raises(TypeError):
        api.scans.launch(1, targets='nope')

@pytest.mark.skip(reason="Switching between scan states can be tricky")
def test_scan_launch(api, scan):
    api.scans.launch(scan['id'])
    time.sleep(5)
    api.scans.stop(scan['id'], block=True)

@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
def test_scan_launch_alt_targets(api, scan):
    api.scans.launch(scan['id'], targets=['127.0.0.2'])
    time.sleep(5)
    api.scans.stop(scan['id'], block=True)

@pytest.mark.vcr()
def test_scan_list_folder_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.list(folder_id='nope')

@pytest.mark.vcr()
def test_scan_list_last_modified_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.list(last_modified='nope')

@pytest.mark.vcr()
def test_scan_list(api):
    scans = api.scans.list()
    assert isinstance(scans, list)
    s = scans[0]
    check(s, 'control', bool)
    check(s, 'creation_date', int)
    check(s, 'enabled', bool)
    check(s, 'id', int)
    check(s, 'last_modification_date', int)
    check(s, 'legacy', bool)
    check(s, 'owner', str)
    check(s, 'name', str)
    check(s, 'permissions', int)
    check(s, 'read', bool)
    check(s, 'rrules', str, allow_none=True)
    check(s, 'schedule_uuid', 'scanner-uuid')
    check(s, 'shared', bool)
    check(s, 'starttime', str, allow_none=True)
    check(s, 'status', str)
    check(s, 'timezone', str, allow_none=True)
    check(s, 'user_permissions', int)
    check(s, 'uuid', 'scanner-uuid')

@pytest.mark.vcr()
def test_scan_pause_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.pause('nope')

@pytest.mark.skip(reason="Switching between scan states can be tricky")
def test_scan_pause_scan(api, scan):
    hid = api.scans.launch(scan['id'])
    api.scans.pause(scan['id'], block=True)

@pytest.mark.vcr()
def test_scan_plugin_output_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output('nope', 1, 1)

@pytest.mark.vcr()
def test_scan_plugin_output_host_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 'nope', 1)

@pytest.mark.vcr()
def test_scan_plugin_output_plugin_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 1, 'nope')

@pytest.mark.vcr()
def test_scan_plugin_output_history_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.plugin_output(1, 1, 1, history_id='nope')

@pytest.mark.vcr()
def test_scan_plugin_output(api, scan_results):
    host = api.scans.host_details(
        SCAN_ID_WITH_RESULTS, scan_results['hosts'][0]['asset_id'])
    output = api.scans.plugin_output(
        SCAN_ID_WITH_RESULTS,
        host['vulnerabilities'][0]['host_id'],
        host['vulnerabilities'][0]['plugin_id'])
    assert isinstance(output, dict)
    check(output, 'info', dict)
    check(output['info'], 'plugindescription', dict)
    check(output['info']['plugindescription'], 'pluginattributes', dict)
    check(output['info']['plugindescription'], 'pluginfamily', str)
    check(output['info']['plugindescription'], 'pluginid', str)
    check(output['info']['plugindescription'], 'pluginname', str)
    check(output['info']['plugindescription'], 'severity', int)
    check(output['info']['plugindescription']['pluginattributes'], 'description', str)
    check(output['info']['plugindescription']['pluginattributes'], 'has_patch', bool)
    check(output['info']['plugindescription']['pluginattributes'], 'plugin_information', dict)
    check(output['info']['plugindescription']['pluginattributes']['plugin_information'], 'plugin_family', str)
    check(output['info']['plugindescription']['pluginattributes']['plugin_information'], 'plugin_id', int)
    check(output['info']['plugindescription']['pluginattributes']['plugin_information'], 'plugin_modification_date', str)
    check(output['info']['plugindescription']['pluginattributes']['plugin_information'], 'plugin_publication_date', str)
    check(output['info']['plugindescription']['pluginattributes']['plugin_information'], 'plugin_type', str)
    check(output['info']['plugindescription']['pluginattributes']['plugin_information'], 'plugin_version', str)
    check(output['info']['plugindescription']['pluginattributes'], 'risk_information', dict)
    check(output['info']['plugindescription']['pluginattributes']['risk_information'], 'risk_factor', str)
    check(output['info']['plugindescription']['pluginattributes'], 'solution', str, allow_none=True)
    check(output['info']['plugindescription']['pluginattributes'], 'synopsis', str, allow_none=True)

    check(output, 'outputs', list)
    for i in output['outputs']:
        check(i, 'has_attachment', int)
        check(i, 'hosts', list, allow_none=True)
        check(i, 'plugin_output', str, allow_none=True)
        check(i, 'ports', dict)
        for port in i['ports']:
            check(i['ports'], port, list)
            for h in i['ports'][port]:
                check(h, 'hostname', str)
        check(i, 'severity', int)

@pytest.mark.vcr()
def test_scan_read_status_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.set_read_status('nope', False)

@pytest.mark.vcr()
def test_scan_read_status_read_status_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.set_read_status(1, 'nope')

@pytest.mark.vcr()
def test_scan_read_status(api, scan):
    scans = api.scans.list()
    s = scans[0]
    api.scans.set_read_status(scans[0]['id'], not scans[0]['read'])
    for i in api.scans.list():
        if i['id'] == s['id']:
            assert s['read'] != i['read']

@pytest.mark.vcr()
def test_scan_resume_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.resume('nope')

@pytest.mark.skip(reason="Switching between scan states can be tricky")
@pytest.mark.vcr()
def test_scan_resume(api, scan):
    api.scans.launch(scan['id'])
    time.sleep(5)
    api.scans.pause(scan['id'], block=True)
    time.sleep(5)
    api.scans.resume(scan['id'])
    time.sleep(5)
    api.scans.stop(scan['id'], block=True)

@pytest.mark.vcr()
def test_scan_schedule_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.schedule('nope', False)

@pytest.mark.vcr()
def test_scan_schedule_enabled_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.schedule(1, 'nope')

@pytest.mark.skip(reason="Need to configure the scan w/ a schedule.")
@pytest.mark.vcr()
def test_scan_schedule(api, scan):
    api.scans.schedule(scan['id'], False)

@pytest.mark.vcr()
def test_scan_stop_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.stop('nope')

@pytest.mark.skip(reason="Switching between scan states can be tricky")
@pytest.mark.vcr()
def test_scan_stop(api, scan):
    api.scans.launch(scan['id'])
    time.sleep(5)
    api.scans.stop(scan['id'])

@pytest.mark.vcr()
def test_scan_status_scan_id_typeerror(api):
    with pytest.raises(TypeError):
        api.scans.status('no')

@pytest.mark.vcr()
def test_scan_status(api, scan):
    status = api.scans.status(scan['id'])
    single(status, str)

@pytest.mark.vcr()
def test_scan_timezones(api):
    assert isinstance(api.scans.timezones(), list)