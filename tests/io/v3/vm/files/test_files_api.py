"""
Testing the File endpoint
"""
import os

import responses

FILE_BASE_URL = 'https://cloud.tenable.com/api/v3/file'
BASE_URL = 'https://cloud.tenable.com'


@responses.activate
def test_upload(api):
    '''
    Test the file upload endpoint
    '''
    responses.add(
        responses.POST,
        f'{FILE_BASE_URL}/upload',
        json={
            'fileuploaded': 'scan_targets_test.txt'
        }
    )

    dummy_file_path = os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
            ), 'scan_targets_test.txt'
        )
    with open(dummy_file_path, "r") as fobj:
        resp = api.v3.vm.files.upload(fobj, True)

    assert resp == 'scan_targets_test.txt'
