'''
Testing the Users endpoints
'''
import re

import responses
from responses import matchers

USERS_BASE_URL = r'https://cloud.tenable.com/v3/users'
USERS_API_ID = r'([0-9a-fA-F\-]+)'
SAMPLE_USER = {
    'id': '60f73e4f-8983-41c2-a13c-39074cbb6229',
    'username': 'user@example.com',
    'email': 'user@example.com',
    'name': 'User One',
    'type': 'local',
    'permissions': 64,
    'roles': ['ADMIN'],
    'last_login_attempt': 1569429971576,
    'login_fail_count': 0,
    'login_fail_total': 3,
    'enabled': True,
    'undeletable': False,
    'two_factor': {
        'sms_phone': '+15551236789',
        'sms_enabled': 1,
        'email_enabled': 0,
    },
    'group_ids': [
        'f3cd0bb2-cabb-4825-9d0c-49c77fe5fba7',
        '00000000-0000-0000-0000-000000000000',
        '2d5c70da-b177-43ed-8325-a25a846c8977',
        'a507f383-3130-4c89-b202-b69ad9a75a84',
        'afed07ce-8e51-4574-a420-90057fea6a7f',
    ],
    'lockout': 0,
    'container_uuid': '270f77d7-3b5b-478c-ac06-be827c00753e',
    'last_login': 1605630009020
}



@responses.activate
def test_details(api):
    responses.add(
        responses.GET,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}'),
        json=SAMPLE_USER
    )
    details = api.v3.users.details(255)
    assert isinstance(details, dict)
    assert details['id'] == '60f73e4f-8983-41c2-a13c-39074cbb6229'


@responses.activate
def test_delete(api):
    responses.add(
        responses.DELETE,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}')
    )
    assert None is api.v3.users.delete(255)


@responses.activate
def test_edit(api):
    responses.add(
        responses.GET,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}'),
        json=SAMPLE_USER
    )
    responses.add(
        responses.PUT,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}'),
        json={
            'id': '1eddf745-7f6b-440a-90c6-df88efe2cf77',
            'username': 'user3@example.com',
            'email': 'user3@example.com',
            'name': 'Test User',
            'type': 'local',
            'container_uuid': 'f8973c82-01a7-4aee-9754-4a61e3b3e70e',
            'permissions': 32,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'enabled': False,
            'lockout': 0
        }
    )
    edit_data = api.v3.users.edit(4, name='Test User')
    assert isinstance(edit_data, dict)
    assert edit_data['id'] == '1eddf745-7f6b-440a-90c6-df88efe2cf77'


@responses.activate
def test_enabled(api):
    responses.add(
        responses.PUT,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/enabled'),
        json={'object': 'user'}
    )
    enabled_data = api.v3.users.enabled(4, True)
    assert isinstance(enabled_data, dict)
    assert enabled_data['object'] == 'user'


@responses.activate
def test_change_password(api):
    old_pass = 'old_pass'
    new_pass = 'new_pass'
    responses.add(
        responses.PUT,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/chpasswd'),
        match=[matchers.json_params_matcher({
            'password': new_pass,
            'current_password': old_pass
        })]
    )
    assert None is api.v3.users.change_password(1, old_pass, new_pass)


@responses.activate
def test_gen_api_keys(api):
    access_key = '2342sdfjsdfads86e1bc7a240ce398645cf2bb80bbbefc178f100d6f5ffc067d'  # noqa: E501
    secret_key = '876dfasdf6a87df6ad2910f1d54d23c14190a267285de4b05a481b1e6d3f0fd6'  # noqa: E501
    responses.add(
        responses.PUT,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/keys'),
        json={
            'accessKey': access_key,
            'secretKey': secret_key
        }
    )
    api_data = api.v3.users.gen_api_keys(12345)
    assert isinstance(api_data, dict)
    assert api_data['accessKey'] == access_key


@responses.activate
def test_create(api):
    responses.add(
        responses.POST,
        re.compile(f'{USERS_BASE_URL}'),
        json={
            'id': 'd748ab37-f2cf-461c-8648-a8328c0f483e',
            'username': 'user4@api.demo',
            'email': 'user2@example.com',
            'name': 'Test User',
            'type': 'local',
            'aggregate': True,
            'container_uuid': 'f8973c82-01a7-4aee-9754-4a61e3b3e70e',
            'permissions': 32,
            'login_fail_count': 0,
            'login_fail_total': 0,
            'enabled': True,
            'lockout': 0
        }
    )
    data = api.v3.users.create('user4@api.demo', 'password', 32)
    assert isinstance(data, dict)
    assert data['username'] == 'user4@api.demo'


@responses.activate
def test_list_auths(api):
    account_uuid = '6c8ffd08-53dc-493e-9823-9f99d4adeab4'
    user_uuid = '4a5e55d6-fd20-465d-9a29-0f1f166d0f49'
    responses.add(
        responses.GET,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/authorizations'),
        json={
            'account_uuid': account_uuid,
            'user_uuid': user_uuid,
            'api_permitted': True,
            'password_permitted': False,
            'saml_permitted': True
        }
    )
    auths_data = api.v3.users.list_auths(user_uuid)
    assert isinstance(auths_data, dict)
    assert auths_data['account_uuid'] == account_uuid


@responses.activate
def test_edit_auths(api):
    payload = {
        'api_permitted': True,
        'password_permitted': True,
        'saml_permitted': False
    }
    responses.add(
        responses.GET,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/authorizations'),
        json={
            'account_uuid': '6c8ffd08-53dc-493e-9823-9f99d4adeab4',
            'user_uuid': '4a5e55d6-fd20-465d-9a29-0f1f166d0f49',
            'api_permitted': True,
            'password_permitted': False,
            'saml_permitted': True
        }
    )
    responses.add(
        responses.PUT,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/authorizations'),
        match=[matchers.json_params_matcher(payload)],
        status=200
    )
    assert 200 == api.v3.users.edit_auths(
        12345, True, True, False).status_code


@responses.activate
def test_enable_two_factor(api):
    payload = {'sms_phone': '9847484848', 'password': 'password'}
    responses.add(
        responses.POST,
        re.compile(
            f'{USERS_BASE_URL}/{USERS_API_ID}/two-factor/send-verification'),
        match=[matchers.json_params_matcher(payload)]
    )
    assert api.v3.users.enable_two_factor(
        12345, payload['sms_phone'], payload['password']) is None


@responses.activate
def test_verify_two_factor(api):
    payload = {'verification_code': '9847484848'}
    responses.add(
        responses.POST,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/two-factor/verify-code'),
        match=[matchers.json_params_matcher(payload)],
    )
    assert api.v3.users.verify_two_factor(
        12345, payload['verification_code']) is None


@responses.activate
def test_two_factor(api):
    payload = {
        'email_enabled': True,
        'sms_enabled': True,
        'sms_phone': '93949494959'
    }
    responses.add(
        responses.PUT,
        re.compile(f'{USERS_BASE_URL}/{USERS_API_ID}/two-factor'),
        match=[matchers.json_params_matcher(payload)],
    )
    assert api.v3.users.two_factor(12345, True, True, '93949494959') is None
