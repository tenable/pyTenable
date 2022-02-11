import pytest
import responses
from io import BytesIO


@responses.activate
def test_files_upload(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/file/upload',
                  json={'fileuploaded': 'example'}
                  )
    resp = nessus.files.upload(BytesIO(b'This is an example file'))
    assert resp == 'example'