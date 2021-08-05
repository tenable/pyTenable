'''
test file for testing various scenarios in security center's
scan instances functionality
'''
import os
import time

import pytest

from tenable.errors import APIError, UnexpectedValueError
from ..checker import check


@pytest.fixture
def scan_instance(vcr, security_center):
    '''
    test fixture for scan instance
    '''
    with vcr.use_cassette('scan_instance'):
        return security_center.scan_instances.list()['manageable'][0]


def test_scan_instance_copy_id_typeerror(security_center):
    '''
    test scan instance copy for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.copy('nothing', 1)


def test_scan_instance_copy_users_typeerror(security_center):
    '''
    test scan instance copy for 'users' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.copy(1, 'user_id')


@pytest.mark.vcr()
def test_scan_instances_copy_success(security_center, scan_instance):
    '''
    test scan instances copy for success
    '''
    security_center.scan_instances.copy(int(scan_instance['id']), 1)


def test_scan_instances_delete_id_typeerror(security_center):
    '''
    test scan instances delete for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.delete('nothing')


@pytest.mark.vcr()
def test_scan_instances_delete_success(security_center, scan_instance):
    '''
    test scan instance delete for success
    '''
    security_center.scan_instances.delete(int(scan_instance['id']))


def test_scan_instances_details_id_typeerror(security_center):
    '''
    test scan instances details for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.details('nothing')


def test_scan_instances_details_fields_typeerror(security_center):
    '''
    test scan instances details for 'fields' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.details(1, 'something')


def test_scan_instances_details_field_item_typeerror(security_center):
    '''
    test scan instances details for 'field item' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.details(1, [1])


@pytest.mark.vcr()
def test_scan_instances_details_success(security_center, scan_instance):
    '''
    test scan instances details for success
    '''
    scan = security_center.scan_instances.details(int(scan_instance['id']))
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


def test_scan_instances_email_id_typeerror(security_center):
    '''
    test scan instances email for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.email('nope')


def test_scan_instances_email_email_typeerror(security_center):
    '''
    test scan instances email for 'email' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.email(1, 1)


@pytest.mark.vcr()
def test_scan_instances_email_success(security_center, scan_instance):
    '''
    test scan instances email for success
    '''
    security_center.scan_instances.email(int(scan_instance['id']), 'no-reply@tenable.com')


def test_scan_instances_export_scan_id_typeerror(security_center):
    '''
    test scan instances export for 'scan id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.export_scan('nothing')


def test_scan_instances_export_scan_export_format_typeerror(security_center):
    '''
    test scan instances export scan for 'export format' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.export_scan(1, export_format=1)


def test_scan_instances_export_scan_export_format_unexpectedvalueerror(security_center):
    '''
    test scan instances export scan for 'export format' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.scan_instances.export_scan(1, export_format='something')


@pytest.mark.vcr()
def test_scan_instances_export_scan_success(security_center, scan_instance):
    '''
    test scan instances export scan for success
    '''
    with open('{}.zip'.format(scan_instance['id']), 'wb') as scanfile:
        security_center.scan_instances.export_scan(124, fobj=scanfile)
    os.remove('{}.zip'.format(scan_instance['id']))


@pytest.mark.vcr()
def test_scan_instances_export_scan_success_no_file(security_center, scan_instance):
    '''
    test scan instances export scan success with no file
    '''
    with open('{}.zip'.format(scan_instance['id']), 'wb'):
        security_center.scan_instances.export_scan(124)
    os.remove('{}.zip'.format(scan_instance['id']))


@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'example.nessus'))
def test_scan_instances_import_scan_success(security_center, datafiles):
    '''
    test scan instances import scan for success
    '''
    with open(os.path.join(str(datafiles), 'example.nessus'), 'rb') as fobj:
        security_center.scan_instances.import_scan(fobj, 1)


def test_scan_instances_reimport_scan_id_typeerror(security_center):
    '''
    test scan instances reimport scan for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.reimport_scan('nope')


@pytest.mark.vcr()
def test_scan_instances_reimport_success(security_center, scan_instance):
    '''
    test scan instances reimport for success
    '''
    security_center.scan_instances.reimport_scan(int(scan_instance['id']))


def test_scan_instances_list_start_time_typerror(security_center):
    '''
    test scan instances list for 'start time' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.list(start_time='none')


def test_scan_instances_list_end_time_typerror(security_center):
    '''
    test scan instances list for 'end time' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.list(end_time='none')


@pytest.mark.vcr()
def test_scan_instances_list(security_center):
    '''
    test scan instances list for success
    '''
    scans = security_center.scan_instances.list()
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


@pytest.mark.vcr()
def test_scan_instances_list_for_fields(security_center):
    '''
    test scan instances list success for fields
    '''
    scan_instances = security_center.scan_instances.list(fields=['id', 'name', 'description'])
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


def test_scan_instances_pause_id_typeerror(security_center):
    '''
    test scan instances pause for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.pause('nope')


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
@pytest.mark.vcr()
def test_scan_instances_pause_success(security_center):
    '''
    test scan instances pause for success
    '''
    scan = security_center.scans.create('Example Scan', 1,
                                        schedule_type='template',
                                        targets=['192.168.101.0/24'],
                                        policy_id=1000001)
    instance = security_center.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        scan = security_center.scan_instances.pause(int(instance['scanResult']['id']))
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


def test_scan_instances_resume_id_typeerror(security_center):
    '''
    test scan instances resume for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.resume('nope')


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
@pytest.mark.vcr()
def test_scan_instances_resume_success(security_center):
    '''
    test scan instances resume for success
    '''
    scan = security_center.scans.create('Example Scan', 1,
                                        schedule_type='template',
                                        targets=['192.168.101.0/24'],
                                        policy_id=1000001)
    instance = security_center.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        security_center.scan_instances.pause(int(instance['scanResult']['id']))
    except APIError:
        pass

    time.sleep(30)
    try:
        scan = security_center.scan_instances.resume(int(instance['scanResult']['id']))
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


def test_scan_instances_stop_id_typeerror(security_center):
    '''
    test scan instances stop for 'id' type error
    '''
    with pytest.raises(TypeError):
        security_center.scan_instances.pause('nope')


@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
@pytest.mark.vcr()
def test_scan_instances_stop_success(security_center):
    '''
    test scan instances stop for success
    '''
    scan = security_center.scans.create('Example Scan', 1,
                                        schedule_type='template',
                                        targets=['192.168.101.0/24'],
                                        policy_id=1000001)
    instance = security_center.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        scan = security_center.scan_instances.stop(int(instance['scanResult']['id']))
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
