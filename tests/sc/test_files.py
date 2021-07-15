'''
test file for testing various scenarios in file functionality
'''
import os

import pytest


@pytest.mark.vcr()
def test_files_upload_clear_success(security_center):
    '''
    test files upload and clear for success
    '''
    with open('1000003.xml', 'w+') as file:
        response = security_center.files.upload(fobj=file)
        filename = security_center.files.clear(response)
        assert filename == 'filename'
    os.remove('1000003.xml')
