import pytest
import responses
from io import BytesIO


@responses.activate
def test_tokens_status(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/1/status',
                  json={'status': 'pending', 'message': 'something'}
                  )
    resp = nessus.tokens.status('1')
    assert resp['status'] == 'pending'
    assert resp['message'] == 'something'


@responses.activate
def test_tokens_download(nessus):
    test_file = BytesIO(b'something to see here')
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/1/download',
                  body=test_file.read()
                  )
    test_file.seek(0)
    fobj = nessus.tokens.download('1')
    assert fobj.read() == test_file.read()