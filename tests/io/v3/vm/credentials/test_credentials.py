'''
Testing for credentials API
'''

import os

import responses

CREDENTIALS_BASE_URL = r'https://cloud.tenable.com/api/v3/credentials'
TYPES_RESPONSE = {
    'credentials': [
        {
            'id': 'API Gateway',
            'category': 'API Gateway',
            'default_expand': False,
            'types': [
                {
                    'id': 'IBM DataPower Gateway',
                    'name': 'IBM DataPower Gateway',
                    'max': 1,
                    'configuration': [
                        {
                            'type': 'file',
                            'name': 'Client Certificate',
                            'hint': 'PEM formatted certificate.',
                            'id': 'datapower_client_cert',
                        },
                        {
                            'type': 'file',
                            'name': 'Client Certificate Private Key',
                            'hint': 'PEM formatted certificate.',
                            'id': 'datapower_private_key',
                        },
                        {
                            'type': 'password',
                            'name': 'Client Certificate '
                                    'Private Key Passphrase',
                            'id': 'datapower_private_key_passphrase',
                        },
                        {
                            'type': 'text',
                            'name': 'Custom Header Key',
                            'id': 'datapower_custom_header_key',
                        },
                        {
                            'type': 'text',
                            'name': 'Custom Header Value',
                            'id': 'datapower_custom_header_value',
                        },
                        {
                            'type': 'checkbox',
                            'name': 'Enable for Hashicorp Vault',
                            'required': True,
                            'default': 'yes',
                            'id': 'datapower_enable_hashicorp',
                        },
                    ],
                }
            ],
        }
    ]
}
DETAILS_RESPONSE = {
    'name': 'Windows devices (Headquarters)',
    'description': 'Use for scans of Windows devices located at headquarters.',
    'category': {
        'id': 'Host',
        'name': 'Host',
    },
    'type': {
        'id': 'Windows',
        'name': 'Windows',
    },
    'ad_hoc': False,
    'user_permissions': 64,
    'settings': {
        'domain': "",
        'username': 'user@example.com',
        'auth_method': 'Password',
    },
    'permissions': [
        {
            'grantee_id': '59042c90-5379-43a2-8cf4-87d97f7cb68f',
            'type': 'user',
            'permissions': 64,
            'name': 'user1@tenable.com',
        }
    ],
}


@responses.activate
def test_delete(api):
    '''
    Test the credentials delete endpoint
    '''
    cred_id = '00000000-0000-0000-0000-000000000000'
    responses.add(
        responses.DELETE,
        url=f'{CREDENTIALS_BASE_URL}/{cred_id}',
        json={'deleted': True},
    )

    data = api.v3.vm.credentials.delete(cred_id)
    assert data


@responses.activate
def test_create(api):
    '''
    Test the credentials create endpoint
    '''
    cred_id = '00000000-0000-0000-0000-000000000000'

    responses.add(
        responses.POST,
        url=f'{CREDENTIALS_BASE_URL}',
        json={'id': '00000000-0000-0000-0000-000000000000'},
    )

    data = api.v3.vm.credentials.create(
        'test5',
        'SSH',
        permissions=[('group', 64, '00000000-0000-0000-0000-000000000000')],
        auth_method='password',
        username='user1',
        password='sekretsquirrel',
        escalation_account='root',
        escalation_password='sudopassword',
        elevate_privileges_with='sudo',
        bin_directory='/usr/bin',
        custom_password_prompt='',
    )
    assert data == cred_id


@responses.activate
def test_edit(api):
    '''
    Test the credentials edit endpoint
    '''
    cred_id = '00000000-0000-0000-0000-000000000000'
    responses.add(
        responses.GET,
        url=f'{CREDENTIALS_BASE_URL}/{cred_id}',
        json=DETAILS_RESPONSE
    )
    responses.add(
            responses.PUT,
            url=f'{CREDENTIALS_BASE_URL}/{cred_id}',
            json={
                'updated': True
            }
        )

    data = api.v3.vm.credentials.edit(
        cred_id, cred_name='test2', description='test', ad_hoc=False
    )
    assert data


@responses.activate
def test_details(api):
    '''
    Test the credentials details endpoint
    '''
    cred_id = '00000000-0000-0000-0000-000000000000'
    responses.add(
        responses.GET,
        url=f'{CREDENTIALS_BASE_URL}/{cred_id}',
        json=DETAILS_RESPONSE
    )

    data = api.v3.vm.credentials.details(cred_id)
    assert data == DETAILS_RESPONSE
    assert isinstance(data, dict)


@responses.activate
def test_types(api):
    '''
    Test the credentials types endpoint
    '''

    responses.add(
        responses.GET,
        url=f'{CREDENTIALS_BASE_URL}/types',
        json=TYPES_RESPONSE
    )

    data = api.v3.vm.credentials.types()
    assert data == TYPES_RESPONSE['credentials']
    assert isinstance(data, list)


@responses.activate
def test_upload(api):
    '''
    Test the credentials upload endpoint
    '''
    responses.add(
        responses.POST,
        f'{CREDENTIALS_BASE_URL}/files',
        json={'fileuploaded': 'credentials_test.txt'},
    )

    dummy_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'credentials_test.txt'
    )
    with open(dummy_file_path, 'w+') as fobj:
        resp = api.v3.vm.credentials.upload(fobj)

    assert resp == 'credentials_test.txt'
