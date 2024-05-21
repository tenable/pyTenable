import pytest
import responses


@responses.activate
def test_modify(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/settings/advanced',
                  json={'new': [{'name': 'new', 'id': 'id', 'category': None}]}
                  )
    resp = nessus.settings.modify([{'action': 'add',
                                    'name': 'new',
                                    'value': 'abc'
                                    }])
    assert resp == {'new': [{'name': 'new', 'id': 'id', 'category': None}]}


@responses.activate
def test_list(nessus):
    setting = {'name': 'example', 'id': 'id', 'category': None}
    responses.add(responses.GET,
                  'https://localhost:8834/settings/advanced',
                  json={'preferences': [setting for _ in range(20)]}
                  )
    resp = nessus.settings.list()
    assert isinstance(resp, list)
    for item in resp:
        assert item == setting


@responses.activate
def test_health(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/settings/health/stats',
                  json={'example': 'value'}
                  )
    assert nessus.settings.health() == {'example': 'value'}


@responses.activate
def test_alerts(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/settings/health/alerts',
                  json=[{'id': 1} for _ in range(20)]
                  )
    resp = nessus.settings.alerts()
    assert isinstance(resp, list)
    for item in resp:
        assert item == {'id': 1}
