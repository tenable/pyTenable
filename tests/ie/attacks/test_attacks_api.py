import pytest
import responses
from marshmallow import ValidationError

from tests.ie.conftest import RE_BASE


@responses.activate
def test_attack_list_default(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/attacks'
                  f'?resourceType=infrastructure&resourceValue=1',
                  json=[{
                      'attackTypeId': 1,
                      'date': '2022-01-14T07:24:50.424Z',
                      'dc': 'dc',
                      'destination': {
                          'hostname': 'test',
                          'ip': '192.168.1.1',
                          'type': 'computer'
                      },
                      'directoryId': 1,
                      'id': 1,
                      'isClosed': False,
                      'source': {
                          'hostname': 'Unknown',
                          'ip': '127.0.0.1',
                          'type': 'computer'
                      },
                      'vector': {
                          'attributes': [{
                              'name': 'source_hostname',
                              'value': 'Unknown',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      }
                  }]
                  )
    resp = api.attacks.list(
        profile_id=1,
        resource_type='infrastructure',
        resource_value='1'
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['directory_id'] == 1
    assert resp[0]['attack_type_id'] == 1


@responses.activate
def test_attack_list_parameterized(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/attacks'
                  f'?resourceValue=1'
                  f'&includeClosed=false'
                  f'&dateEnd=2022-12-31T18%3A30%3A00%2B00%3A00'
                  f'&limit=10'
                  f'&search=Something'
                  f'&attackTypeIds=1'
                  f'&attackTypeIds=2'
                  f'&dateStart=2021-12-31T18%3A30%3A00%2B00%3A00'
                  f'&resourceType=infrastructure'
                  f'&order=desc',
                  json=[{
                      'attackTypeId': 1,
                      'date': '2022-01-14T07:24:50.424Z',
                      'dc': 'dc',
                      'destination': {
                          'hostname': 'test',
                          'ip': '192.168.1.1',
                          'type': 'computer'
                      },
                      'directoryId': 1,
                      'id': 1,
                      'isClosed': False,
                      'source': {
                          'hostname': 'Unknown',
                          'ip': '127.0.0.1',
                          'type': 'computer'
                      },
                      'vector': {
                          'attributes': [{
                              'name': 'source_hostname',
                              'value': 'Unknown',
                              'valueType': 'string'
                          }],
                          'template': 'template'
                      }
                  }]
                  )
    resp = api.attacks.list(
        profile_id=1,
        resource_type='infrastructure',
        resource_value='1',
        attack_type_ids=[1, 2],
        include_closed='false',
        limit='10',
        order='desc',
        search='Something',
        date_end='2022-12-31T18:30:00.000Z',
        date_start='2021-12-31T18:30:00.000Z'
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['directory_id'] == 1
    assert resp[0]['attack_type_id'] == 1
    assert resp[0]['is_closed'] is False


def test_attack_list_resource_type_validationerror(api):
    '''
    test to raise validation error when resource type does not match
    the expected list of values
    '''
    with pytest.raises(ValidationError):
        api.attacks.list(
            profile_id=1,
            resource_type='something',
            resource_value='resource type value'
        )
