import pytest
import responses
from marshmallow import ValidationError

from tests.ie.conftest import RE_BASE


@responses.activate
def test_attack_type_option_list(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/attack-types/1/attack-type-options'
                  f'?staged=0',
                  json=[{
                      'id': 1,
                      'codename': 'codename',
                      'profileId': 1,
                      'attackTypeId': 1,
                      'directoryId': None,
                      'value': '[]',
                      'valueType': 'array/string',
                      'name': 'attack type option',
                      'description': 'description',
                      'translations': ['some translation'],
                      'staged': False
                  }]
                  )
    resp = api.attack_type_options.list(
        profile_id='1',
        attack_type_id='1',
        staged=False
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['profile_id'] == 1
    assert resp[0]['attack_type_id'] == 1
    assert resp[0]['value'] == '[]'
    assert resp[0]['value_type'] == 'array/string'


@responses.activate
def test_attack_type_option_create(api):
    responses.add(responses.POST,
                  f'{RE_BASE}/profiles/1/attack-types/1/attack-type-options',
                  json=[{
                      'id': 1,
                      'codename': 'codename',
                      'profileId': 1,
                      'attackTypeId': 1,
                      'directoryId': None,
                      'value': '[]',
                      'valueType': 'array/string',
                      'name': 'attack type option',
                      'description': 'description',
                      'translations': ['some translation'],
                      'staged': False
                  }]
                  )
    resp = api.attack_type_options.create(
        profile_id='1',
        attack_type_id='1',
        codename='codename',
        value='[]',
        value_type='array/string',
        directory_id=None
    )
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['profile_id'] == 1
    assert resp[0]['attack_type_id'] == 1
    assert resp[0]['value'] == '[]'
    assert resp[0]['value_type'] == 'array/string'


def test_attack_type_option_value_type_validationerror(api):
    '''
    test to raise exception when value_type doesn't match the expected value
    '''
    with pytest.raises(ValidationError):
        api.attack_type_options.create(
            profile_id='1',
            attack_type_id='1',
            codename='attack type option codename',
            value='something',
            value_type='something',
        )
