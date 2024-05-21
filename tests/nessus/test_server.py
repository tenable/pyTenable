import pytest
import responses


@responses.activate
def test_server_properties(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/server/properties',
                  json={'id': 1}
                  )
    resp = nessus.server.properties()
    assert resp == {'id': 1}


@responses.activate
def test_server_status(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/server/status',
                  json={'status': 'loading', 'progress': 50}
                  )
    resp = nessus.server.status()
    assert resp == {'status': 'loading', 'progress': 50}


@responses.activate
def test_server_restart(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/server/restart'
                  )
    nessus.server.restart(reason='Example Reason',
                          soft=True,
                          unlink=True,
                          when_idle=True
                          )