"""
test for uploading the file and file with encryption
"""
import os
import pytest
import responses
from io import BytesIO
from responses import matchers


@responses.activate
def test_files_upload(api):
    """
    test to uploads the file object
    """
    responses.post('https://cloud.tenable.com/file/upload',
                   match=[
                    matchers.multipart_matcher({
                        'Filedata': b'ExampleFileData'
                    }),
                   ],
                   json={'fileuploaded': 'test.txt'}
                   )
    fobj = BytesIO(b'ExampleFileData')
    assert api.files.upload(fobj) == 'test.txt'


@responses.activate
def test_files_encryption_success(api, datafiles):
    """
    test to upload the file with encryption
    """
    responses.post('https://cloud.tenable.com/file/upload',
                   match=[
                    matchers.multipart_matcher({
                        'Filedata': b'ExampleFileData'
                    }),
                    matchers.query_param_matcher({'no_enc': 1})
                   ],
                   json={'fileuploaded': 'test.txt'}
                   )
    fobj = BytesIO(b'ExampleFileData')
    assert api.files.upload(fobj, encrypted=True) == 'test.txt'
