from tenable.errors import *
from ..checker import check, single
import pytest, time, os

@pytest.fixture
def scaninstance(request, vcr, sc):
    with vcr.use_cassette('scan_instance'):
        return sc.scan_instances.list()['manageable'][0]


def test_scan_instance_copy_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.copy('nothing', 1)

def test_scan_instance_copy_users_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.copy(1, 'user_id')

@pytest.mark.vcr()
def test_scan_instances_copy_success(sc, scaninstance):
    newscan = sc.scan_instances.copy(int(scaninstance['id']), 1)

def test_scan_instances_delete_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.delete('nothing')

@pytest.mark.vcr()
def test_scan_instances_delete_success(sc, scaninstance):
    sc.scan_instances.delete(int(scaninstance['id']))

def test_scan_instances_details_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.details('nothing')

def test_scan_instances_details_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.details(1, 'something')

def test_scan_instances_details_field_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.details(1, [1])

@pytest.mark.vcr()
def test_scan_instances_details_success(sc, scaninstance):
    s = sc.scan_instances.details(int(scaninstance['id']))
    assert isinstance(s, dict)
    check(s, 'dataFormat', str)
    check(s, 'description', str)
    check(s, 'details', str)
    check(s, 'diagnosticAvailable', str)
    check(s, 'downloadAvailable', str)
    check(s, 'downloadFormat', str)
    check(s, 'errorDetails', str)
    check(s, 'finishTime', str)
    check(s, 'id', str)
    check(s, 'importDuration', str)
    check(s, 'importErrorDetails', str)
    check(s, 'importFinish', str)
    check(s, 'importStart', str)
    check(s, 'importStatus', str)
    check(s, 'initiator', dict)
    check(s['initiator'], 'firstname', str)
    check(s['initiator'], 'id', str)
    check(s['initiator'], 'lastname', str)
    check(s['initiator'], 'username', str)
    check(s, 'name', str)
    check(s, 'owner', dict)
    check(s['owner'], 'firstname', str)
    check(s['owner'], 'id', str)
    check(s['owner'], 'lastname', str)
    check(s['owner'], 'username', str)
    check(s, 'ownerGroup', dict)
    check(s['ownerGroup'], 'description', str)
    check(s['ownerGroup'], 'id', str)
    check(s['ownerGroup'], 'name', str)
    check(s, 'progress', dict)
    check(s['progress'], 'awaitingDownloadIPs', str)
    check(s['progress'], 'checksPerHost', str)
    check(s['progress'], 'completedChecks', str)
    check(s['progress'], 'completedIPs', str)
    check(s['progress'], 'deadHostIPs', str)
    check(s['progress'], 'deadHostSize', int)
    check(s['progress'], 'distributedSize', int)
    check(s['progress'], 'runState', str)
    check(s['progress'], 'scannedIPs', str)
    check(s['progress'], 'scannedSize', int)
    check(s['progress'], 'scanners', list)
    for i in s['progress']['scanners']:
        check(i, 'awaitingDownloadIPs', str)
        check(i, 'awaitingDownloadSize', int)
        check(i, 'chunkCompleted', str)
        check(i, 'chunks', list)
        check(i, 'completedChecks', str)
        check(i, 'deadHostIPs', str)
        check(i, 'deadHostSize', int)
        check(i, 'description', str)
        check(i, 'distributedSize', int)
        check(i, 'id', str)
        check(i, 'loadAvg', str)
        check(i, 'name', str)
        check(i, 'scannedIPs', str)
        check(i, 'scannedSize', int)
        check(i, 'scanningIPs', str)
        check(i, 'scanningSize', int)
    check(s['progress'], 'scanningIPs', str)
    check(s['progress'], 'scanningSize', int)
    check(s['progress'], 'status', str)
    check(s['progress'], 'totalChecks', str)
    check(s['progress'], 'totalIPs', str)
    check(s, 'repository', dict)
    check(s['repository'], 'description', str)
    check(s['repository'], 'id', str)
    check(s['repository'], 'name', str)
    check(s, 'resultSource', str)
    check(s, 'resultType', str)
    check(s, 'running', str)
    check(s, 'scan', dict)
    check(s['scan'], 'description', str)
    check(s['scan'], 'id', int)
    check(s['scan'], 'name', str)
    check(s, 'scanDuration', str)
    check(s, 'scannedIPs', str)
    check(s, 'startTime', str)
    check(s, 'status', str)
    check(s, 'totalChecks', str)
    check(s, 'totalIPs', str)

def test_scan_instances_email_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.email('nope')

def test_scan_instances_email_email_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.email(1, 1)

@pytest.mark.vcr()
def test_scan_instances_email_success(sc, scaninstance):
    sc.scan_instances.email(int(scaninstance['id']), 'no-reply@tenable.com')

def test_scan_instances_export_scan_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.export_scan('nothing')

def test_scan_instances_export_scan_export_format_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.export_scan(1, export_format=1)

def test_scan_instances_export_scan_export_format_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.scan_instances.export_scan(1, export_format='something')

@pytest.mark.vcr()
def test_scan_instances_export_scan_success(sc, scaninstance):
    with open('{}.zip'.format(scaninstance['id']), 'wb') as scanfile:
        sc.scan_instances.export_scan(124, fobj=scanfile)
    os.remove('{}.zip'.format(scaninstance['id']))

@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'example.nessus'))
def test_scan_instances_import_scan_success(sc, datafiles):
    with open(os.path.join(str(datafiles), 'example.nessus'), 'rb') as fobj:
        sc.scan_instances.import_scan(fobj, 1)

def test_scan_instances_reimport_scan_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.reimport_scan('nope')

@pytest.mark.vcr()
def test_scan_instances_reimport_success(sc, scaninstance):
    sc.scan_instances.reimport_scan(int(scaninstance['id']))

def test_scan_instances_list_start_time_typerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.list(start_time='none')

def test_scan_instances_list_end_time_typerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.list(end_time='none')

@pytest.mark.vcr()
def test_scan_instances_list(sc):
    r = sc.scan_instances.list()
    assert isinstance(r, dict)
    check(r, 'manageable', list)
    for i in r['manageable']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
        check(i, 'status', str)
    check(r, 'usable', list)
    for i in r['usable']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
        check(i, 'status', str)

def test_scan_instances_pause_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.pause('nope')

@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
@pytest.mark.vcr()
def test_scan_instances_pause_success(sc):
    scan = sc.scans.create('Example Scan', 1,
        schedule_type='template',
        targets=['192.168.101.0/24'],
        policy_id=1000001)
    instance = sc.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        s = sc.scan_instances.pause(int(instance['scanResult']['id']))
    except APIError as error:
        pass
    else:
        check(s, 'canManage', str)
        check(s, 'canUse', str)
        check(s, 'createdTime', str)
        check(s, 'dataFormat', str)
        check(s, 'description', str)
        check(s, 'details', str)
        check(s, 'diagnosticAvailable', str)
        check(s, 'downloadAvailable', str)
        check(s, 'downloadFormat', str)
        check(s, 'errorDetails', str)
        check(s, 'finishTime', str)
        check(s, 'id', str)
        check(s, 'importDuration', str)
        check(s, 'importErrorDetails', str)
        check(s, 'importFinish', str)
        check(s, 'importStart', str)
        check(s, 'importStatus', str)
        check(s, 'initiator', dict)
        check(s['initiator'], 'firstname', str)
        check(s['initiator'], 'id', str)
        check(s['initiator'], 'lastname', str)
        check(s['initiator'], 'username', str)
        check(s, 'jobID', str)
        check(s, 'name', str)
        check(s, 'owner', dict)
        check(s['owner'], 'firstname', str)
        check(s['owner'], 'id', str)
        check(s['owner'], 'lastname', str)
        check(s['owner'], 'username', str)
        check(s, 'ownerGroup', str)
        check(s['ownerGroup'], 'description', str)
        check(s['ownerGroup'], 'id', str)
        check(s['ownerGroup'], 'name', str)
        check(s, 'repository', dict)
        check(s['repository'], 'description', str)
        check(s['repository'], 'id', str)
        check(s['repository'], 'name', str)
        check(s, 'resultSource', str)
        check(s, 'resultType', str)
        check(s, 'resultsSyncID', str)
        check(s, 'running', str)
        check(s, 'scan', dict)
        check(s['scan'], 'description', str)
        check(s['scan'], 'id', str)
        check(s['scan'], 'name', str)
        check(s, 'scanDuration', str)
        check(s, 'scannedIPs', str)
        check(s, 'startTime', str)
        check(s, 'status', str)
        check(s, 'totalChecks', str)
        check(s, 'totalIPs', str)

def test_scan_instances_resume_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.resume('nope')

@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
@pytest.mark.vcr()
def test_scan_instances_resume_success(sc):
    scan = sc.scans.create('Example Scan', 1,
        schedule_type='template',
        targets=['192.168.101.0/24'],
        policy_id=1000001)
    instance = sc.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        s = sc.scan_instances.pause(int(instance['scanResult']['id']))
    except APIError as error:
        pass

    time.sleep(30)
    try:
        s = sc.scan_instances.resume(int(instance['scanResult']['id']))
    except APIError as error:
        pass
    else:
        check(s, 'canManage', str)
        check(s, 'canUse', str)
        #check(s, 'completedChecks', str)
        check(s, 'createdTime', str)
        check(s, 'dataFormat', str)
        check(s, 'description', str)
        check(s, 'details', str)
        check(s, 'diagnosticAvailable', str)
        check(s, 'downloadAvailable', str)
        check(s, 'downloadFormat', str)
        check(s, 'errorDetails', str)
        check(s, 'finishTime', str)
        check(s, 'id', str)
        check(s, 'importDuration', str)
        check(s, 'importErrorDetails', str)
        check(s, 'importFinish', str)
        check(s, 'importStart', str)
        check(s, 'importStatus', str)
        check(s, 'initiator', dict)
        check(s['initiator'], 'firstname', str)
        check(s['initiator'], 'id', str)
        check(s['initiator'], 'lastname', str)
        check(s['initiator'], 'username', str)
        check(s, 'jobID', str)
        check(s, 'name', str)
        check(s, 'owner', dict)
        check(s['owner'], 'firstname', str)
        check(s['owner'], 'id', str)
        check(s['owner'], 'lastname', str)
        check(s['owner'], 'username', str)
        check(s, 'ownerGroup', str)
        check(s['ownerGroup'], 'description', str)
        check(s['ownerGroup'], 'id', str)
        check(s['ownerGroup'], 'name', str)
        check(s, 'repository', dict)
        check(s['repository'], 'description', str)
        check(s['repository'], 'id', str)
        check(s['repository'], 'name', str)
        check(s, 'resultSource', str)
        check(s, 'resultType', str)
        check(s, 'resultsSyncID', str)
        check(s, 'running', str)
        check(s, 'scan', dict)
        check(s['scan'], 'description', str)
        check(s['scan'], 'id', str)
        check(s['scan'], 'name', str)
        check(s, 'scanDuration', str)
        check(s, 'scannedIPs', str)
        check(s, 'startTime', str)
        check(s, 'status', str)
        check(s, 'totalChecks', str)
        check(s, 'totalIPs', str)

def test_scan_instances_stop_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.scan_instances.pause('nope')

@pytest.mark.skip(reason='Switching between scan states this quickly can be trixsy')
@pytest.mark.vcr()
def test_scan_instances_stop_success(sc):
    scan = sc.scans.create('Example Scan', 1,
        schedule_type='template',
        targets=['192.168.101.0/24'],
        policy_id=1000001)
    instance = sc.scans.launch(int(scan['id']))
    time.sleep(120)
    try:
        s = sc.scan_instances.stop(int(instance['scanResult']['id']))
    except APIError as error:
        pass
    else:
        check(s, 'canManage', str)
        check(s, 'canUse', str)
        #check(s, 'completedChecks', str)
        check(s, 'createdTime', str)
        check(s, 'dataFormat', str)
        check(s, 'description', str)
        check(s, 'details', str)
        check(s, 'diagnosticAvailable', str)
        check(s, 'downloadAvailable', str)
        check(s, 'downloadFormat', str)
        check(s, 'errorDetails', str)
        check(s, 'finishTime', str)
        check(s, 'id', str)
        check(s, 'importDuration', str)
        check(s, 'importErrorDetails', str)
        check(s, 'importFinish', str)
        check(s, 'importStart', str)
        check(s, 'importStatus', str)
        check(s, 'initiator', dict)
        check(s['initiator'], 'firstname', str)
        check(s['initiator'], 'id', str)
        check(s['initiator'], 'lastname', str)
        check(s['initiator'], 'username', str)
        check(s, 'jobID', str)
        check(s, 'name', str)
        check(s, 'owner', dict)
        check(s['owner'], 'firstname', str)
        check(s['owner'], 'id', str)
        check(s['owner'], 'lastname', str)
        check(s['owner'], 'username', str)
        check(s, 'ownerGroup', str)
        check(s['ownerGroup'], 'description', str)
        check(s['ownerGroup'], 'id', str)
        check(s['ownerGroup'], 'name', str)
        check(s, 'repository', dict)
        check(s['repository'], 'description', str)
        check(s['repository'], 'id', str)
        check(s['repository'], 'name', str)
        check(s, 'resultSource', str)
        check(s, 'resultType', str)
        check(s, 'resultsSyncID', str)
        check(s, 'running', str)
        check(s, 'scan', dict)
        check(s['scan'], 'description', str)
        check(s['scan'], 'id', str)
        check(s['scan'], 'name', str)
        check(s, 'scanDuration', str)
        check(s, 'scannedIPs', str)
        check(s, 'startTime', str)
        check(s, 'status', str)
        check(s, 'totalChecks', str)
        check(s, 'totalIPs', str)