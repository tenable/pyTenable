import pytest
import responses
from responses import matchers
from io import BytesIO


@responses.activate
def test_scan_attachment(nessus):
    test_file = BytesIO(b'something to see here')
    responses.add(responses.GET,
                  'https://localhost:8834/scans/1/attachments/1?key=abcdef',
                  body=test_file.read()
                  )
    test_file.seek(0)
    with BytesIO() as example:
        nessus.scans.attachment(1, 1, 'abcdef', fobj=example)
        assert test_file.read() == example.read()
    test_file.seek(0)
    assert nessus.scans.attachment(1, 1, 'abcdef').read() == test_file.read()


@responses.activate
def test_scan_configure(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/scans/1',
                  json={'example': 'value'}
                  )
    assert nessus.scans.configure(1, settings={'1': 1}) == {'example': 'value'}


@responses.activate
def test_scan_copy(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/scans/1/copy',
                  json={'example': 'value'}
                  )
    assert nessus.scans.copy(1, name='New Name') == {'example': 'value'}


@responses.activate
def test_scan_create(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/scans',
                  json={'example': 'value'},
                  match=[
                      matchers.json_params_matcher({
                          'uuid': 'abcdef12345667890abcdef',
                          'settings': {
                              'name': 'Example Scan',
                              'enabled': False,
                              'text_targets': '192.168.1.1'
                          }
                      })
                  ]
                  )
    assert nessus.scans.create(uuid='abcdef12345667890abcdef',
                               settings={
                                   'name': 'Example Scan',
                                   'enabled': False,
                                   'text_targets': '192.168.1.1'
                               }
                               ) == {'example': 'value'}


@responses.activate
def test_scan_delete(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/scans/1'
                  )
    nessus.scans.delete(1)


@responses.activate
def test_scan_delete_many(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/scans',
                  json={'deleted': [1, 2, 3]},
                  match=[
                      matchers.json_params_matcher({'ids': [1, 2, 3]})
                  ]
                  )
    assert nessus.scans.delete_many([1, 2, 3]) == [1, 2, 3]


@responses.activate
def test_scan_delete_history(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/scans/1/history/2'
                  )
    nessus.scans.delete_history(1, 2)


@responses.activate
def test_scan_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scans/1',
                  json={'example': 'value'}
                  )
    assert nessus.scans.details(1) == {'example': 'value'}


@responses.activate
def test_scan_export_formats(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scans/1/export/formats',
                  json={'example': 'value'}
                  )
    assert nessus.scans.export_formats(1) == {'example': 'value'}


@responses.activate
def test_scan_export(nessus):
    test_file = BytesIO(b'something to see here')
    responses.add(responses.POST,
                  'https://localhost:8834/scans/1/export',
                  match=[
                      matchers.json_params_matcher({
                          'format': 'nessus'
                      })
                  ],
                  json={'token': 'abcdef'}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/abcdef/status',
                  json={'status': 'ready'}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/abcdef/download',
                  body=test_file.read()
                  )
    test_file.seek(0)
    assert nessus.scans.export_scan(1).read() == test_file.read()


@responses.activate
def test_scan_import(nessus):
    test_file = BytesIO(b'something to see here')
    responses.add(responses.POST,
                  'https://localhost:8834/file/upload',
                  json={'fileuploaded': 'example'}
                  )
    responses.add(responses.POST,
                  'https://localhost:8834/scans/import',
                  match=[
                      matchers.json_params_matcher({'file': 'example'})
                  ],
                  json={'example': 'value'}
                  )
    assert nessus.scans.import_scan(test_file) == {'example': 'value'}


@responses.activate
def test_scan_kill(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/scans/1/kill'
                  )
    nessus.scans.kill(1)


@responses.activate
def test_scan_launch(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/scans/1/launch',
                  json={'scan_uuid': 'abcdef'}
                  )
    assert nessus.scans.launch(1) == 'abcdef'


@responses.activate
def test_scan_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scans',
                  json={'folders': [],
                        'scans': [],
                        'timestamp': 0
                        }
                  )
    assert nessus.scans.list() == {'folders': [], 'scans': [], 'timestamp': 0}


@responses.activate
def test_scan_pause(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/scans/1/pause'
                  )
    nessus.scans.pause(1)


@responses.activate
def test_scan_plugin_output(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scans/1/hosts/1/plugins/1',
                  json={'example': 'value'}
                  )
    assert nessus.scans.plugin_output(1, 1, 1) == {'example': 'value'}


@responses.activate
def test_scan_read_status(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/scans/1/status?read=true',
                  )
    nessus.scans.read_status(1, True)


@responses.activate
def test_scan_resume(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/scans/1/resume'
                  )
    nessus.scans.resume(1)


@responses.activate
def test_scan_schedule(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/scans/1/schedule?enabled=true'
                  )
    nessus.scans.schedule(1, True)


@responses.activate
def test_scan_stop(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/scans/1/stop'
                  )
    nessus.scans.stop(1)


@responses.activate
def test_scan_timezones(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scans/timezones',
                  json={'timezones': [{'example': 'value'}]}
                  )
    assert nessus.scans.timezones() == [{'example': 'value'}]
