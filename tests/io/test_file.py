"""
test for uploading the file and file with encryption
"""
import os

import pytest


@pytest.mark.vcr()
def test_files_upload(api):
    """
    test to uploads the file object
    """
    api.files.upload('ExampleDataGoesHere')


@pytest.mark.vcr()
def test_files_encryption_success(api, datafiles):
    """
    test to upload the file with encryption
    """
    file = 'test.txt'
    with open(os.path.join(str(datafiles), file), 'w+') as fobj:
        fobj.write('test')
        fobj.close()
    with open(os.path.join(str(datafiles), file), 'rb') as fobj:
        api.files.upload(fobj, encrypted=True)
