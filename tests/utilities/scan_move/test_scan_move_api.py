import responses

from tenable.io import TenableIO
from tenable.utilities.scan_move import ScanMove

from .objects import (EXPORT_RESP_DATA, FILE_ID, FILE_UPLOAD_RESP_DATA,
                      HISTORY_ID_1, HISTORY_ID_2, IMPORT_RESP_DATA, SCAN,
                      SCAN_FILTERS_RESP_DATA, SCAN_HISTORIES, SCAN_ID)

SCAN_BASE_URL = 'https://cloud.tenable.com/scans'
BASE_URL = 'https://cloud.tenable.com'


@responses.activate
def test_scan_move():
    source_tio = TenableIO()
    target_tio = TenableIO()
    scan_move = ScanMove(source_tio, target_tio)

    responses.add(
        responses.GET,
        SCAN_BASE_URL,
        json={"scans": [SCAN]}
    )

    responses.add(
        responses.GET,
        f'{SCAN_BASE_URL}/{SCAN_ID}/history',
        json=SCAN_HISTORIES
    )

    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{HISTORY_ID_1}/export',
        json=EXPORT_RESP_DATA
    )
    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/{HISTORY_ID_2}/export',
        json=EXPORT_RESP_DATA
    )

    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{HISTORY_ID_1}/export/{FILE_ID}/status',
        json={'status': 'ready'}
    )
    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{HISTORY_ID_2}/export/{FILE_ID}/status',
        json={'status': 'ready'}
    )

    with open('scan_history.txt', 'rb') as history:
        text_contents = history.read()

    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{HISTORY_ID_1}/export/{FILE_ID}/download',
        body=text_contents
    )

    responses.add(
        responses.GET,
        url=f'{SCAN_BASE_URL}/{HISTORY_ID_2}/export/{FILE_ID}/download',
        body=text_contents
    )

    responses.add(
        responses.GET,
        url=f'{BASE_URL}/filters/scans/reports',
        json=SCAN_FILTERS_RESP_DATA
    )

    responses.add(
        responses.POST,
        url=f'{SCAN_BASE_URL}/import',
        json=IMPORT_RESP_DATA
    )

    responses.add(
        responses.POST,
        url=f'{BASE_URL}/file/upload',
        json=FILE_UPLOAD_RESP_DATA
    )

    scan_move.move(1)
