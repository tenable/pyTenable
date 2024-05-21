'''conftest'''
import os
import uuid
import pytest
import responses
from tenable.errors import NotFoundError
from tenable.io import TenableIO
from tests.pytenable_log_handler import setup_logging_to_file, log_exception

SCAN_ID_WITH_RESULTS = 6799


@pytest.fixture
@responses.activate
def tvm():
    return TenableIO(url='https://nourl',
                     access_key='ACCESS_KEY',
                     secret_key='SECRET_KEY'
                     )


@pytest.fixture(scope='module')
def vcr_config():
    '''vcr config fixture'''
    return {
        'filter_headers': [
            ('X-APIKeys', 'accessKey=TIO_ACCESS_KEY;secretKey=TIO_SECRET_KEY'),
            ('x-request-uuid', 'ffffffffffffffffffffffffffffffff'),
        ],
    }


@pytest.fixture
def api():
    '''api keys fixture'''
    setup_logging_to_file()
    return TenableIO(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')


@pytest.fixture
def stdapi():
    '''std api keys fixture'''
    return TenableIO(
        os.getenv('TIO_TEST_STD_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_STD_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')


@pytest.fixture
def agent(api):
    '''agent fixture'''
    return api.agents.list().next()


@pytest.fixture
def folder(request, api):
    '''fixture to create a folder'''
    folder = api.folders.create(str(uuid.uuid4())[:20])

    def teardown():
        '''function to clear the folder'''
        try:
            api.folders.delete(folder)
        except NotFoundError as notfound:
            log_exception(notfound)

    request.addfinalizer(teardown)
    return folder


@pytest.fixture
def policy(request, api):
    '''fixture to create a policy'''
    policy = api.policies.create({
        'credentials': {'add': {}, 'delete': [], 'edit': {}},
        'settings': {
            'name': str(uuid.uuid4()),
        },
        'uuid': '731a8e52-3ea6-a291-ec0a-d2ff0619c19d7bd788d6be818b65'
    })

    def teardown():
        '''function to clear policy'''
        try:
            api.policies.delete(policy['policy_id'])
        except NotFoundError as notfound:
            log_exception(notfound)

    request.addfinalizer(teardown)
    return policy


@pytest.fixture
def user(request, api):
    '''fixture to create an user'''
    user = api.users.create(
        '{}@tenable.com'.format(uuid.uuid4()),
        '{}Tt!'.format(uuid.uuid4()),
        64)

    def teardown():
        '''function to clear the user'''
        try:
            api.users.delete(user['id'])
        except NotFoundError as notfound:
            log_exception(notfound)

    request.addfinalizer(teardown)
    return user


@pytest.fixture
def scanner(api):
    '''fixture to filter scanner which has owner permission'''
    scanners = api.scanners.list()
    for scanner in scanners:
        if scanner['user_permissions'] == 128 and not scanner['pool']:
            return scanner


@pytest.fixture
def scannergroup(request, api):
    '''
    fixture to create a scanner_group
    '''
    scannergroup = api.scanner_groups.create(str(uuid.uuid4()))

    def teardown():
        '''function to clear the scanner_group'''
        try:
            api.scanner_groups.delete(scannergroup['id'])
        except NotFoundError as notfound:
            log_exception(notfound)

    request.addfinalizer(teardown)
    return scannergroup


@pytest.fixture
def scan(request, api):
    '''
    fixture to create a scan
    '''
    scan = api.scans.create(
        name='pytest: {}'.format(uuid.uuid4()),
        template='basic',
        targets=['127.0.0.1'])

    def teardown():
        '''
        function to clear the scan
        '''
        try:
            api.scans.delete(scan['id'])
        except NotFoundError as notfound:
            log_exception(notfound)

    request.addfinalizer(teardown)
    return scan


@pytest.fixture
def remediationscan(request, api):
    '''
    remediation scan fixture
    '''
    scan = api.remediationscans.create_remediation_scan(
        uuid='76d67790-2969-411e-a9d0-667f05e8d49e',
        name='RemedyScan',
        description='RemediationScan Creation',
        scan_time_window=10,
        targets=['http://127.0.0.1'],
        template='advanced')

    def teardown():
        '''
        function to delete the scan
        '''
        try:
            api.scans.delete(scan['id'])
        except NotFoundError as notfound:
            log_exception(notfound)

    request.addfinalizer(teardown)
    return scan


@pytest.fixture
def scan_results(api):
    '''fixture to get the scan results'''
    scan_list = [id['id'] for id in list(filter(lambda value: value['status'] == 'completed', api.scans.list()))]
    if scan_list:
        return {'results': api.scans.results(scan_list[0]), 'id': scan_list[0]}
    raise NotFoundError("Scan not found")


@pytest.fixture
def target_file(request, api):
    lines = ['scan create document with fileUpload ', 'only file name in file target']
    with open('file.txt', 'w') as targetFile:
        for line in lines:
            targetFile.write(line)
            targetFile.write('\n')
    targetFile.close()
    api.files.upload(targetFile.name)

    def teardown():
        os.remove(targetFile.name)

    request.addfinalizer(teardown)
    return targetFile
