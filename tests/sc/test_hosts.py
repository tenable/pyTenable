import pytest
import responses
from responses.matchers import json_params_matcher, query_param_matcher


@pytest.fixture
def test_resp():
    return {
        'error_code': 0,
        'error_msg': '',
        'warnings': [],
        'response': [
            {
                'id': '154',
                'uuid': '12345678-1234-1234-123456789012',
                'tenableUUID': '1234abcd-abcd-abcd-1234567890abcd',
                'name': 'test1',
                'ipAddress': '1.2.3.4',
                'os': 'Linux',
                'firstSeen': '1770789',
                'lastSeen': '1779789',
            }
        ],
    }


@responses.activate
def test_host_list(tsc, test_resp):
    responses.get(
        'https://nourl/rest/hosts',
        match=[
            query_param_matcher(
                {
                    'fields': (
                        'id,uuid,tenableUUID,name,ipAddress,os,firstSeen,lastSeen,'
                        'macAddress,source,repID,netBios,netBiosWorkgroup,createdTime,'
                        'modifiedTime,acr,aes'
                    ),
                    'endOffset': 10000,
                    'startOffset': 0,
                    'limit': 10000,
                    'pagination': 'true',
                }
            )
        ],
        json=test_resp,
    )
    resp = tsc.hosts.list()
    item = next(resp)
    assert item == test_resp['response'][0]


@responses.activate
def test_host_search(tsc, test_resp):
    responses.post(
        'https://nourl/rest/hosts/search',
        json=test_resp,
        match=[
            query_param_matcher(
                {
                    'fields': (
                        'id,uuid,tenableUUID,name,ipAddress,os,firstSeen,lastSeen,'
                        'macAddress,source,repID,netBios,netBiosWorkgroup,createdTime,'
                        'modifiedTime,acr,aes'
                    ),
                    'endOffset': 10000,
                    'startOffset': 0,
                    'limit': 10000,
                    'pagination': 'true',
                }
            ),
            json_params_matcher(
                {
                    'filters': {
                        'and': [
                            {'property': 'ip', 'operator': 'eq', 'value': '1.2.3.4'}
                        ]
                    }
                }
            ),
        ],
    )
    resp = tsc.hosts.search(('ip', 'eq', '1.2.3.4'))
    item = next(resp)
    assert item == test_resp['response'][0]


@responses.activate
def test_hosts_update_acr(tsc):
    test_obj = {
        'id': '123',
        'uuid': '12345678-1234-1234-123456789012',
    }
    responses.patch(
        'https://nourl/rest/hosts/12345678-1234-1234-123456789012/acr',
        match=[
            json_params_matcher(
                {
                    'overwrittenScore': 7,
                    'reasoning': [{'id': 1}],
                    'notes': 'Example notes',
                    'overwritten': 'true',
                }
            )
        ],
        json={
            'type': 'regular',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'response': test_obj,
        },
    )
    assert test_obj == tsc.hosts.update_acr(
        '12345678-1234-1234-123456789012', score=7, reasoning=[1], notes='Example notes'
    )
