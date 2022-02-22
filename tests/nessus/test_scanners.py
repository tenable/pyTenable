import pytest
import responses


@responses.activate
def test_control_scan(nessus):
    responses.add(responses.POST,
                  ('https://localhost:8834/scanners/1/scans/'
                   '00000000-0000-0000-0000-000000000000/control'),
                  )
    nessus.scanners.control_scan(1,
                                 '00000000-0000-0000-0000-000000000000',
                                 'pause'
                                 )


@responses.activate
def test_delete(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/scanners/1'
                  )
    nessus.scanners.delete(1)


@responses.activate
def test_delete_many(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/scanners'
                  )
    nessus.scanners.delete_many([1, 2, 3])


@responses.activate
def test_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scanners/1',
                  json={'id': 1, 'name': 'Example Scanner'}
                  )
    resp = nessus.scanners.details(1)
    assert resp == {'id': 1, 'name': 'Example Scanner'}


@responses.activate
def test_update(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/scanners/1'
                  )
    nessus.scanners.update(1, 
                           force_plugin_update=True,
                           force_ui_update=True,
                           finish_update=True
                           )


@responses.activate
def test_aws_targets(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scanners/1/aws-targets',
                  json={'targets': [{'id': 1} for _ in range(20)]}
                  )
    resp = nessus.scanners.aws_targets(1)
    assert isinstance(resp, list)
    for item in resp:
        assert item == {'id': 1}


@responses.activate
def test_scanner_key(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scanners/1/key',
                  json={'key': '1234567890abcdef1234567890'}
                  )
    resp = nessus.scanners.scanner_key(1)
    assert resp == '1234567890abcdef1234567890'


@responses.activate
def test_running_scans(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scanners/1/scans',
                  json={'scans': [{'id': 1} for _ in range(20)]}
                  )
    resp = nessus.scanners.running_scans(1)
    assert isinstance(resp, list)
    for item in resp:
        assert item == {'id': 1}
    
    responses.add(responses.GET,
                  'https://localhost:8834/scanners/1/scans',
                  json={'scans': None}
                  )
    assert nessus.scanners.running_scans(1) == None


@responses.activate
def test_scanner_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/scanners',
                  json={'scanners': [{'id': 1} for _ in range(10)]}
                  )
    resp = nessus.scanners.list()
    assert isinstance(resp, list)
    for item in resp:
        assert item == {'id': 1}


@responses.activate
def test_scanner_link_state(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/scanners/1/link'
                  )
    nessus.scanners.link_state(1, True)