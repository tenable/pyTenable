'''
Testing the ScanBridge utility for pyTenable
'''

import os

import pytest
import responses

from tenable.io import TenableIO
from tenable.sc import TenableSC
from tenable.utilities.scan_bridge import ScanBridge
from tests.pytenable_log_handler import setup_logging_to_file

# from responses import matchers


dir_name = os.path.dirname(os.path.abspath(__file__))

TXT_ATTACHMENT_FILE = 'test_file.txt'
TXT_ATTACHMENT_FILE_PATH = os.path.join(dir_name, TXT_ATTACHMENT_FILE)

SC_BASE_URL = r'https://cloud.tenablesc.com:443'
# SCAN_BASE_URL = r'https://cloud.tenable.com/api/v3/scans'
SCAN_BASE_URL = r'https://cloud.tenable.com/scans'
BASE_URL = r'https://cloud.tenable.com'


@pytest.fixture
def text_contents():
    '''
    Fixture to read the contents of text file.
    '''
    with open(TXT_ATTACHMENT_FILE_PATH, 'rb') as txt_file:
        text_data = txt_file.read()

    return text_data


@pytest.fixture
def api():
    '''api keys fixture'''
    setup_logging_to_file()
    tio = TenableIO(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')
    tsc = TenableSC(
        os.getenv('SC_TEST_HOST', 'cloud.tenablesc.com'),
        vendor='pytest',
        product='pytenable-automated-testing')
    return tio, tsc


@responses.activate
def test_bridge(api, text_contents):
    scan_id = 9
    file_id = 778874546
    scan_filters_resp_data = {'filters': [
        {
            'name': 'host.id',
            'readable_name': 'Asset ID',
            'control': {
                'type': 'entry',
                'regex': '[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12} \
                    (,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*',
                'readable_regex': '01234567-abcd-ef01-2345-6789abcdef01'
            },
            'operators': [
                'eq',
                'neq',
                'match',
                'nmatch'
            ],
            'group_name': 'None'
        },
        {
            'name': 'tracking.state',
            'readable_name': 'Vulnerability State',
            'control': {
                'type': 'dropdown',
                'list': [
                    'New',
                    'Fixed',
                    'Active',
                    'Resurfaced'
                ]
            },
            'operators': [
                'eq',
                'neq'
            ],
            'group_name': 'None'
        }
    ]}
    export_resp_data = {
        'file': file_id,
        'temp_token':
            '995bdb656fc6dc5d76e18ccafe7fbd390618fcd0257e0e1aa121f4412a6f7ecc'
    }
    sc_file_upload_resp = {
        'type': 'regular',
        'response': {
                'filename': 'R9Hial',
                'originalFilename': f'{scan_id}.nessus',
                'content': '',
                'context': ''
        },
        'error_code': 0,
        'error_msg': '',
        'warnings': [],
        'timestamp': '2021-12-31T20:50:23.635Z'
    }
    scan_result_import_resp = {
        'type': 'regular',
        'response': '',
        'error_code': 0,
        'error_msg': '',
        'warnings': [],
        'timestamp': '2021-12-31T20:50:30.635Z'
    }

    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{scan_id}/export',
        json=export_resp_data
    )
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/scans/{scan_id}/export/{file_id}/status',
        json={'status': 'ready'}
    )
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{scan_id}/export/{file_id}/download',
        body=text_contents
    )
    responses.add(
        responses.GET,
        url=f'{BASE_URL}/filters/scans/reports',
        json=scan_filters_resp_data
    )
    responses.add(
        responses.POST,
        url=f'{SC_BASE_URL}/rest/file/upload',
        json=sc_file_upload_resp
    )
    responses.add(
        responses.POST,
        url=f'{SC_BASE_URL}/rest/scanResult/import',
        json=scan_result_import_resp
    )
    tio, tsc = api
    sb = ScanBridge(tsc, tio)
    assert sb.bridge(scan_id, 8) is None
