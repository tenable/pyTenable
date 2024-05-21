'''
test file for testing various scenarios in file functionality
'''
from io import BytesIO
import responses
from responses.matchers import json_params_matcher
import pytest


@responses.activate
def test_files_upload(tsc):
    fake = BytesIO(b'Test File')
    responses.post('https://nourl/rest/file/upload',
                   json={
                       'error_code': 0,
                       'response': {'filename': 'something'}
                   },
                   )

    assert 'something' == tsc.files.upload(fake)

@responses.activate
def test_files_clear(tsc):
    responses.post('https://nourl/rest/file/clear',
                   match=[
                       json_params_matcher({'filename': 'testfile'})
                   ],
                   json={
                       'error_code': 0,
                       'response': {'filename': 'testfile'}
                   }
                   )
    assert 'testfile' == tsc.files.clear('testfile')
