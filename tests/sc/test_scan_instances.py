"""
test file for testing various scenarios in security center's
scan instances functionality
"""

import os
import time

import pytest
import responses
from responses import matchers

from tenable.errors import APIError, UnexpectedValueError
from ..checker import check


@pytest.fixture
def scan_instance():
    """
    test fixture for scan instance
    """
    return {
        'id': '120',
        'name': 'Daily Agent Scan [Agent Scan Import]',
        'description': '',
        'status': 'Completed',
    }


def test_scan_instance_copy_id_typeerror(tsc):
    """
    test scan instance copy for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.copy('nothing', 1)


def test_scan_instance_copy_users_typeerror(tsc):
    """
    test scan instance copy for 'users' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.copy(1, 'user_id')


@responses.activate
def test_scan_instances_copy_success(tsc, scan_instance):
    """
    test scan instances copy for success
    """
    responses.post(
        'https://nourl/rest/scanResult/120/copy',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189100,
        },
    )
    tsc.scan_instances.copy(int(scan_instance['id']), 1)


def test_scan_instances_delete_id_typeerror(tsc):
    """
    test scan instances delete for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.delete('nothing')


@responses.activate
def test_scan_instances_delete_success(tsc, scan_instance):
    """
    test scan instance delete for success
    """
    responses.delete(
        'https://nourl/rest/scanResult/120',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189101,
        },
    )
    tsc.scan_instances.delete(int(scan_instance['id']))


def test_scan_instances_details_id_typeerror(tsc):
    """
    test scan instances details for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.details('nothing')


def test_scan_instances_details_fields_typeerror(tsc):
    """
    test scan instances details for 'fields' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.details(1, 'something')


def test_scan_instances_details_field_item_typeerror(tsc):
    """
    test scan instances details for 'field item' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.details(1, [1])


@responses.activate
def test_scan_instances_details_success(tsc, scan_instance):
    """
    test scan instances details for success
    """
    responses.get(
        'https://nourl/rest/scanResult/120',
        json={
            'type': 'regular',
            'response': {
                'id': '121',
                'name': 'Daily Internal Scan',
                'description': '',
                'details': 'Full Safe Scan',
                'status': 'Completed',
                'importStatus': 'Finished',
                'importStart': '1550039581',
                'importFinish': '1550039582',
                'importDuration': '1',
                'diagnosticAvailable': 'false',
                'downloadAvailable': 'true',
                'downloadFormat': 'v2',
                'dataFormat': 'IPv4',
                'resultType': 'active',
                'resultSource': 'internal',
                'running': 'false',
                'errorDetails': '',
                'importErrorDetails': '',
                'totalIPs': '2048',
                'scannedIPs': '2048',
                'startTime': '1550037606',
                'finishTime': '1550039578',
                'scanDuration': '1972',
                'createdTime': '1550037600',
                'completedIPs': '2048',
                'completedChecks': '209686528',
                'totalChecks': '209686528',
                'progress': {
                    'completedIPs': '2048',
                    'completedChecks': '209686528',
                    'totalChecks': '209686528',
                    'checksPerHost': '102386',
                    'totalIPs': '2048',
                    'runState': 'Stopped',
                    'scanningIPs': '',
                    'scanningSize': 0,
                    'scannedIPs': '192.168.100.1,192.168.100.3-192.168.100.5,192.168.100.10,192.168.100.50-192.168.100.51,192.168.100.136,192.168.101.1,192',
                    'scannedSize': 49,
                    'awaitingDownloadIPs': '',
                    'awaitingDownloadSize': 0,
                    'distributedSize': 2048,
                    'status': 'Completed',
                    'deadHostSize': 1999,
                    'deadHostIPs': '192.168.100.0,192.168.100.2,192.168.100.6-192.168.100.9,192.168.100.11-192.168.100.49,192.168.100.52-192.168.100.135,192',
                    'scanners': [
                        {
                            'id': '1',
                            'loadAvg': '0.0',
                            'chunkCompleted': '2048',
                            'completedChecks': '209686528',
                            'name': 'Internal Scanner',
                            'description': '',
                            'chunks': [],
                            'scannedSize': 49,
                            'scannedIPs': '192.168.100.1,192.168.100.3-192.168.100.5,192.168.100.10,192.168.100.50-192.168.100.51,192.168.100.136,192.168.101.1,192',
                            'scanningSize': 0,
                            'scanningIPs': '',
                            'awaitingDownloadSize': 0,
                            'awaitingDownloadIPs': '',
                            'deadHostSize': 1999,
                            'deadHostIPs': '192.168.100.0,192.168.100.2,192.168.100.6-192.168.100.9,192.168.100.11-192.168.100.49,192.168.100.52-192.168.100.135,192',
                            'distributedSize': 2048,
                        }
                    ],
                },
                'initiator': {
                    'id': '1',
                    'username': 'steve',
                    'firstname': 'Steve',
                    'lastname': 'McGrath',
                },
                'owner': {
                    'id': '1',
                    'username': 'steve',
                    'firstname': 'Steve',
                    'lastname': 'McGrath',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
                'scan': {'id': -1, 'name': '', 'description': ''},
                'repository': {'id': '1', 'name': 'Default', 'description': ''},
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1550189101,
        },
    )
    scan = tsc.scan_instances.details(int(scan_instance['id']))
    assert isinstance(scan, dict)
    check(scan, 'dataFormat', str)
    check(scan, 'description', str)
    check(scan, 'details', str)
    check(scan, 'diagnosticAvailable', str)
    check(scan, 'downloadAvailable', str)
    check(scan, 'downloadFormat', str)
    check(scan, 'errorDetails', str)
    check(scan, 'finishTime', str)
    check(scan, 'id', str)
    check(scan, 'importDuration', str)
    check(scan, 'importErrorDetails', str)
    check(scan, 'importFinish', str)
    check(scan, 'importStart', str)
    check(scan, 'importStatus', str)
    check(scan, 'initiator', dict)
    check(scan['initiator'], 'firstname', str)
    check(scan['initiator'], 'id', str)
    check(scan['initiator'], 'lastname', str)
    check(scan['initiator'], 'username', str)
    check(scan, 'name', str)
    check(scan, 'owner', dict)
    check(scan['owner'], 'firstname', str)
    check(scan['owner'], 'id', str)
    check(scan['owner'], 'lastname', str)
    check(scan['owner'], 'username', str)
    check(scan, 'ownerGroup', dict)
    check(scan['ownerGroup'], 'description', str)
    check(scan['ownerGroup'], 'id', str)
    check(scan['ownerGroup'], 'name', str)
    check(scan, 'progress', dict)
    check(scan['progress'], 'awaitingDownloadIPs', str)
    check(scan['progress'], 'checksPerHost', str)
    check(scan['progress'], 'completedChecks', str)
    check(scan['progress'], 'completedIPs', str)
    check(scan['progress'], 'deadHostIPs', str)
    check(scan['progress'], 'deadHostSize', int)
    check(scan['progress'], 'distributedSize', int)
    check(scan['progress'], 'runState', str)
    check(scan['progress'], 'scannedIPs', str)
    check(scan['progress'], 'scannedSize', int)
    check(scan['progress'], 'scanners', list)
    for scanner in scan['progress']['scanners']:
        check(scanner, 'awaitingDownloadIPs', str)
        check(scanner, 'awaitingDownloadSize', int)
        check(scanner, 'chunkCompleted', str)
        check(scanner, 'chunks', list)
        check(scanner, 'completedChecks', str)
        check(scanner, 'deadHostIPs', str)
        check(scanner, 'deadHostSize', int)
        check(scanner, 'description', str)
        check(scanner, 'distributedSize', int)
        check(scanner, 'id', str)
        check(scanner, 'loadAvg', str)
        check(scanner, 'name', str)
        check(scanner, 'scannedIPs', str)
        check(scanner, 'scannedSize', int)
        check(scanner, 'scanningIPs', str)
        check(scanner, 'scanningSize', int)
    check(scan['progress'], 'scanningIPs', str)
    check(scan['progress'], 'scanningSize', int)
    check(scan['progress'], 'status', str)
    check(scan['progress'], 'totalChecks', str)
    check(scan['progress'], 'totalIPs', str)
    check(scan, 'repository', dict)
    check(scan['repository'], 'description', str)
    check(scan['repository'], 'id', str)
    check(scan['repository'], 'name', str)
    check(scan, 'resultSource', str)
    check(scan, 'resultType', str)
    check(scan, 'running', str)
    check(scan, 'scan', dict)
    check(scan['scan'], 'description', str)
    check(scan['scan'], 'id', int)
    check(scan['scan'], 'name', str)
    check(scan, 'scanDuration', str)
    check(scan, 'scannedIPs', str)
    check(scan, 'startTime', str)
    check(scan, 'status', str)
    check(scan, 'totalChecks', str)
    check(scan, 'totalIPs', str)


def test_scan_instances_email_id_typeerror(tsc):
    """
    test scan instances email for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.email('nope')


def test_scan_instances_email_email_typeerror(tsc):
    """
    test scan instances email for 'email' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.email(1, 1)


@responses.activate
def test_scan_instances_email_success(tsc, scan_instance):
    """
    test scan instances email for success
    """
    responses.post(
        'https://nourl/rest/scanResult/120/email',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': 'Scan Result email failed.\nError sending email.\nInvalid address:  (From): noreply@localhost\n',
            'warnings': [],
            'timestamp': 1550189102,
        },
    )
    tsc.scan_instances.email(int(scan_instance['id']), 'no-reply@tenable.com')


def test_scan_instances_export_scan_id_typeerror(tsc):
    """
    test scan instances export for 'scan id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.export_scan('nothing')


def test_scan_instances_export_scan_export_format_typeerror(tsc):
    """
    test scan instances export scan for 'export format' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.export_scan(1, export_format=1)


def test_scan_instances_export_scan_export_format_unexpectedvalueerror(tsc):
    """
    test scan instances export scan for 'export format' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.scan_instances.export_scan(1, export_format='something')


@responses.activate
def test_scan_instances_export_scan_success(tsc, scan_instance):
    """
    test scan instances export scan for success
    """
    responses.post(
        'https://nourl/rest/scanResult/124/download',
        body=b'PK\x05\x06' + b'\x00' * 18,  # an empty zip archive
        content_type='application/zip',
        headers={'content-disposition': 'attachment; filename=124-nessus.zip'},
    )
    with open('{}.zip'.format(scan_instance['id']), 'wb') as scanfile:
        tsc.scan_instances.export_scan(124, fobj=scanfile)
    os.remove('{}.zip'.format(scan_instance['id']))


@responses.activate
def test_scan_instances_export_scan_success_no_file(tsc, scan_instance):
    """
    test scan instances export scan success with no file
    """
    responses.post(
        'https://nourl/rest/scanResult/124/download',
        body='empty content !!',
        content_type='application/zip',
        headers={'content-disposition': 'attachment; filename=124-nessus.zip'},
    )
    with open('{}.zip'.format(scan_instance['id']), 'wb'):
        tsc.scan_instances.export_scan(124)
    os.remove('{}.zip'.format(scan_instance['id']))


@pytest.mark.datafiles(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'test_files',
        'example.nessus',
    )
)
@responses.activate
def test_scan_instances_import_scan_success(tsc, datafiles):
    """
    test scan instances import scan for success
    """
    responses.post(
        'https://nourl/rest/file/upload',
        json={
            'type': 'regular',
            'response': {
                'filename': 'fdSzCv',
                'originalFilename': 'example.nessus',
                'content': '',
                'context': '',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189106,
        },
    )
    responses.post(
        'https://nourl/rest/scanResult/import',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189106,
        },
    )
    with open(os.path.join(str(datafiles), 'example.nessus'), 'rb') as fobj:
        tsc.scan_instances.import_scan(fobj, 1)


def test_scan_instances_reimport_scan_id_typeerror(tsc):
    """
    test scan instances reimport scan for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.reimport_scan('nope')


@responses.activate
def test_scan_instances_reimport_success(tsc, scan_instance):
    """
    test scan instances reimport for success
    """
    responses.post(
        'https://nourl/rest/scanResult/120/import',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189107,
        },
    )
    tsc.scan_instances.reimport_scan(int(scan_instance['id']))


def test_scan_instances_list_start_time_typerror(tsc):
    """
    test scan instances list for 'start time' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.list(start_time='none')


def test_scan_instances_list_end_time_typerror(tsc):
    """
    test scan instances list for 'end time' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.list(end_time='none')


@responses.activate
def test_scan_instances_list(tsc):
    """
    test scan instances list for success
    """
    responses.get(
        'https://nourl/rest/scanResult',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {
                        'id': '121',
                        'name': 'Daily Internal Scan',
                        'description': '',
                        'status': 'Completed',
                    },
                    {
                        'id': '122',
                        'name': 'Daily Agent Scan [Agent Scan Import]',
                        'description': '',
                        'status': 'Completed',
                    },
                ],
                'manageable': [
                    {
                        'id': '121',
                        'name': 'Daily Internal Scan',
                        'description': '',
                        'status': 'Completed',
                    },
                    {
                        'id': '122',
                        'name': 'Daily Agent Scan [Agent Scan Import]',
                        'description': '',
                        'status': 'Completed',
                    },
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189107,
        },
        match=[matchers.query_param_matcher({'optimizeCompletedScanResults': 'true'})],
    )
    scans = tsc.scan_instances.list()
    assert isinstance(scans, dict)
    check(scans, 'manageable', list)
    for manageable in scans['manageable']:
        check(manageable, 'id', str)
        check(manageable, 'name', str)
        check(manageable, 'description', str)
        check(manageable, 'status', str)
    check(scans, 'usable', list)
    for usable in scans['usable']:
        check(usable, 'id', str)
        check(usable, 'name', str)
        check(usable, 'description', str)
        check(usable, 'status', str)


@responses.activate
def test_scan_instances_list_for_fields(tsc):
    """
    test scan instances list success for fields
    """
    responses.get(
        'https://nourl/rest/scanResult',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {'id': '121', 'name': 'Daily Internal Scan', 'description': ''},
                    {
                        'id': '122',
                        'name': 'Daily Agent Scan [Agent Scan Import]',
                        'description': '',
                    },
                ],
                'manageable': [
                    {'id': '121', 'name': 'Daily Internal Scan', 'description': ''},
                    {
                        'id': '122',
                        'name': 'Daily Agent Scan [Agent Scan Import]',
                        'description': '',
                    },
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1550189107,
        },
        match=[
            matchers.query_param_matcher(
                {
                    'optimizeCompletedScanResults': 'true',
                    'fields': 'id,name,description',
                }
            )
        ],
    )
    scan_instances = tsc.scan_instances.list(fields=['id', 'name', 'description'])
    assert isinstance(scan_instances, dict)
    check(scan_instances, 'manageable', list)
    for manageable in scan_instances['manageable']:
        check(manageable, 'id', str)
        check(manageable, 'name', str)
        check(manageable, 'description', str)
    check(scan_instances, 'usable', list)
    for usable in scan_instances['usable']:
        check(usable, 'id', str)
        check(usable, 'name', str)
        check(usable, 'description', str)


def test_scan_instances_pause_id_typeerror(tsc):
    """
    test scan instances pause for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.pause('nope')


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
def test_scan_instances_pause_success(tsc):
    """
    test scan instances pause for success
    """
    scan = tsc.scans.create(
        'Example Scan',
        1,
        schedule_type='template',
        targets=['192.168.101.0/24'],
        policy_id=1000001,
    )
    instance = tsc.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        scan = tsc.scan_instances.pause(int(instance['scanResult']['id']))
    except APIError:
        pass
    else:
        check(scan, 'canManage', str)
        check(scan, 'canUse', str)
        check(scan, 'createdTime', str)
        check(scan, 'dataFormat', str)
        check(scan, 'description', str)
        check(scan, 'details', str)
        check(scan, 'diagnosticAvailable', str)
        check(scan, 'downloadAvailable', str)
        check(scan, 'downloadFormat', str)
        check(scan, 'errorDetails', str)
        check(scan, 'finishTime', str)
        check(scan, 'id', str)
        check(scan, 'importDuration', str)
        check(scan, 'importErrorDetails', str)
        check(scan, 'importFinish', str)
        check(scan, 'importStart', str)
        check(scan, 'importStatus', str)
        check(scan, 'initiator', dict)
        check(scan['initiator'], 'firstname', str)
        check(scan['initiator'], 'id', str)
        check(scan['initiator'], 'lastname', str)
        check(scan['initiator'], 'username', str)
        check(scan, 'jobID', str)
        check(scan, 'name', str)
        check(scan, 'owner', dict)
        check(scan['owner'], 'firstname', str)
        check(scan['owner'], 'id', str)
        check(scan['owner'], 'lastname', str)
        check(scan['owner'], 'username', str)
        check(scan, 'ownerGroup', str)
        check(scan['ownerGroup'], 'description', str)
        check(scan['ownerGroup'], 'id', str)
        check(scan['ownerGroup'], 'name', str)
        check(scan, 'repository', dict)
        check(scan['repository'], 'description', str)
        check(scan['repository'], 'id', str)
        check(scan['repository'], 'name', str)
        check(scan, 'resultSource', str)
        check(scan, 'resultType', str)
        check(scan, 'resultsSyncID', str)
        check(scan, 'running', str)
        check(scan, 'scan', dict)
        check(scan['scan'], 'description', str)
        check(scan['scan'], 'id', str)
        check(scan['scan'], 'name', str)
        check(scan, 'scanDuration', str)
        check(scan, 'scannedIPs', str)
        check(scan, 'startTime', str)
        check(scan, 'status', str)
        check(scan, 'totalChecks', str)
        check(scan, 'totalIPs', str)


def test_scan_instances_resume_id_typeerror(tsc):
    """
    test scan instances resume for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.resume('nope')


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
def test_scan_instances_resume_success(tsc):
    """
    test scan instances resume for success
    """
    scan = tsc.scans.create(
        'Example Scan',
        1,
        schedule_type='template',
        targets=['192.168.101.0/24'],
        policy_id=1000001,
    )
    instance = tsc.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        tsc.scan_instances.pause(int(instance['scanResult']['id']))
    except APIError:
        pass

    time.sleep(30)
    try:
        scan = tsc.scan_instances.resume(int(instance['scanResult']['id']))
    except APIError:
        pass
    else:
        check(scan, 'canManage', str)
        check(scan, 'canUse', str)
        check(scan, 'createdTime', str)
        check(scan, 'dataFormat', str)
        check(scan, 'description', str)
        check(scan, 'details', str)
        check(scan, 'diagnosticAvailable', str)
        check(scan, 'downloadAvailable', str)
        check(scan, 'downloadFormat', str)
        check(scan, 'errorDetails', str)
        check(scan, 'finishTime', str)
        check(scan, 'id', str)
        check(scan, 'importDuration', str)
        check(scan, 'importErrorDetails', str)
        check(scan, 'importFinish', str)
        check(scan, 'importStart', str)
        check(scan, 'importStatus', str)
        check(scan, 'initiator', dict)
        check(scan['initiator'], 'firstname', str)
        check(scan['initiator'], 'id', str)
        check(scan['initiator'], 'lastname', str)
        check(scan['initiator'], 'username', str)
        check(scan, 'jobID', str)
        check(scan, 'name', str)
        check(scan, 'owner', dict)
        check(scan['owner'], 'firstname', str)
        check(scan['owner'], 'id', str)
        check(scan['owner'], 'lastname', str)
        check(scan['owner'], 'username', str)
        check(scan, 'ownerGroup', str)
        check(scan['ownerGroup'], 'description', str)
        check(scan['ownerGroup'], 'id', str)
        check(scan['ownerGroup'], 'name', str)
        check(scan, 'repository', dict)
        check(scan['repository'], 'description', str)
        check(scan['repository'], 'id', str)
        check(scan['repository'], 'name', str)
        check(scan, 'resultSource', str)
        check(scan, 'resultType', str)
        check(scan, 'resultsSyncID', str)
        check(scan, 'running', str)
        check(scan, 'scan', dict)
        check(scan['scan'], 'description', str)
        check(scan['scan'], 'id', str)
        check(scan['scan'], 'name', str)
        check(scan, 'scanDuration', str)
        check(scan, 'scannedIPs', str)
        check(scan, 'startTime', str)
        check(scan, 'status', str)
        check(scan, 'totalChecks', str)
        check(scan, 'totalIPs', str)


def test_scan_instances_stop_id_typeerror(tsc):
    """
    test scan instances stop for 'id' type error
    """
    with pytest.raises(TypeError):
        tsc.scan_instances.pause('nope')


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
def test_scan_instances_stop_success(tsc):
    """
    test scan instances stop for success
    """
    scan = tsc.scans.create(
        'Example Scan',
        1,
        schedule_type='template',
        targets=['192.168.101.0/24'],
        policy_id=1000001,
    )
    instance = tsc.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        scan = tsc.scan_instances.stop(int(instance['scanResult']['id']))
    except APIError:
        pass
    else:
        check(scan, 'canManage', str)
        check(scan, 'canUse', str)
        check(scan, 'createdTime', str)
        check(scan, 'dataFormat', str)
        check(scan, 'description', str)
        check(scan, 'details', str)
        check(scan, 'diagnosticAvailable', str)
        check(scan, 'downloadAvailable', str)
        check(scan, 'downloadFormat', str)
        check(scan, 'errorDetails', str)
        check(scan, 'finishTime', str)
        check(scan, 'id', str)
        check(scan, 'importDuration', str)
        check(scan, 'importErrorDetails', str)
        check(scan, 'importFinish', str)
        check(scan, 'importStart', str)
        check(scan, 'importStatus', str)
        check(scan, 'initiator', dict)
        check(scan['initiator'], 'firstname', str)
        check(scan['initiator'], 'id', str)
        check(scan['initiator'], 'lastname', str)
        check(scan['initiator'], 'username', str)
        check(scan, 'jobID', str)
        check(scan, 'name', str)
        check(scan, 'owner', dict)
        check(scan['owner'], 'firstname', str)
        check(scan['owner'], 'id', str)
        check(scan['owner'], 'lastname', str)
        check(scan['owner'], 'username', str)
        check(scan, 'ownerGroup', str)
        check(scan['ownerGroup'], 'description', str)
        check(scan['ownerGroup'], 'id', str)
        check(scan['ownerGroup'], 'name', str)
        check(scan, 'repository', dict)
        check(scan['repository'], 'description', str)
        check(scan['repository'], 'id', str)
        check(scan['repository'], 'name', str)
        check(scan, 'resultSource', str)
        check(scan, 'resultType', str)
        check(scan, 'resultsSyncID', str)
        check(scan, 'running', str)
        check(scan, 'scan', dict)
        check(scan['scan'], 'description', str)
        check(scan['scan'], 'id', str)
        check(scan['scan'], 'name', str)
        check(scan, 'scanDuration', str)
        check(scan, 'scannedIPs', str)
        check(scan, 'startTime', str)
        check(scan, 'status', str)
        check(scan, 'totalChecks', str)
        check(scan, 'totalIPs', str)
