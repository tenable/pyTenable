import pytest
import responses
from responses.matchers import multipart_matcher
from io import BytesIO


@responses.activate
def test_files_upload(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/file/upload',
                  json={'fileuploaded': 'example'},
                  match=[multipart_matcher({
                        'Filedata': b'This is an example file'
                      },
                      data={'no_enc': 0}
                  )])
    resp = nessus.files.upload(BytesIO(b'This is an example file'))
    assert resp == 'example'


@responses.activate
def test_files_download_priv(nessus):
    test_file = BytesIO(b'this is a test')
    responses.add(responses.GET,
                  'https://localhost:8834/example_file',
                  body=test_file.read()
                  )
    test_file.seek(0)

    # Test Defaults
    resp = nessus.get('example_file', stream=True)
    fobj = nessus.files._download(resp)
    assert test_file.read() == fobj.read()

    # Test with presented BytesIO object
    with BytesIO() as fobj:
        test_file.seek(0)
        resp = nessus.get('example_file', stream=True)
        nessus.files._download(resp, fobj=fobj)
        assert test_file.read() == fobj.read()

    # Test with custom stream hook
    test_file.seek(0)
    resp = nessus.get('example_file', stream=True)
    def hook(resp, fobj, size):
        for chunk in resp.iter_content(chunk_size=size):
            if chunk:
                fobj.write(chunk)
    fobj = nessus.files._download(resp, stream_hook=hook)
    assert test_file.read() == fobj.read()
