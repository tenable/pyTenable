'''
test audit-log
'''
import pytest
import responses
from responses.matchers import query_param_matcher
from copy import copy


@pytest.fixture
def event():
    return {
        'id': '8ca42afc7d4f42c19a731bc7bdac1efd',
        'action': 'user.authenticate.password',
        'cud': 'u',
        'actor': {
            'id': '84bba2d4-42a8-4fee-a259-15cd4b7dbddc',
            'name': 'user@company.com'
        },
        'target': {
            'id': '84bba2d4-42a8-4fee-a259-15cd4b7dbddc',
            'name': 'user@company.com',
            'type': 'User'
        },
        'description': None,
        'is_anonymous': None,
        'is_failure': False,
        'fields': [
            {
                'key': 'X-Forwarded-For',
                'value': '104.12.225.249, 104.12.225.249'
            }, {
                'key': 'X-Request-Uuid',
                'value': 'abc123:abc123:abc123:abc123'
            }
        ],
        'received': '2022-05-24T19:09:47.982Z'
    }


@responses.activate
def test_audit_log_json(api, event):
    resp = {
        'pagination': {
            'offset': 0,
            'limit': 1000,
            'count': 100,
            'total': 100,
        },
        'events': [event for _ in range(100)]
    }
    responses.get('https://cloud.tenable.com/audit-log/v1/events',
                  json=resp
                  )
    assert resp == api.audit_log.events(return_json=True)


@responses.activate
def test_audit_log_iter(api, event):
    with responses.RequestsMock() as rsps:
        rsps.get('https://cloud.tenable.com/audit-log/v1/events',
                 json={
                     'pagination': {
                         'offset': 0,
                         'limit': 1000,
                         'count': 1000,
                         'total': 2000,
                         'next': 'abc123',
                     },
                     'events': [event for _ in range(1000)]
                 },
                 match=[query_param_matcher({
                    'next': '0',
                    'ft': 'and',
                    'limit': 1000
                 })]
                 )
        rsps.get('https://cloud.tenable.com/audit-log/v1/events',
                 json={
                      'pagination': {
                          'offset': 0,
                          'limit': 1000,
                          'count': 1000,
                          'total': 2000,
                      },
                      'events': [event for _ in range(1000)]
                  },
                 match=[query_param_matcher({
                    'next': 'abc123',
                    'ft': 'and',
                    'limit': 1000
                 })]
                 )
        events = api.audit_log.events()
        for e in events:
            assert e == event
        assert events.total == 2000
        assert events.count == 2000
