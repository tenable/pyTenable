'''
test file for testing various scenarios in credentials
'''
import os

import pytest

from contextlib import nullcontext as does_not_raise
from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception
from ..checker import check, single


def test_credentials_constructor_name_typeerror(security_center):
    '''
    test credentials constructor for name type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(name=1)


def test_credentials_constructor_tags_typeerror(security_center):
    '''
    test credentials constructor for tags type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(tags=1)


def test_credentials_constructor_description_typeerror(security_center):
    '''
    test credentials constructor for description type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(description=1)


def test_credentials_constructor_login_typeerror(security_center):
    '''
    test credentials constructor for login type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(login=1)


def test_credentials_constructor_sid_typeerror(security_center):
    '''
    test credentials constructor for sid type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(sid=1)


def test_credentials_constructor_auth_type_typeerror(security_center):
    '''
    test credentials constructor for 'auth type' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(auth_type=1)


def test_credentials_constructor_auth_type_unexpectedvalueerror(security_center):
    '''
    test credentials constructor for 'auth type' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.credentials._constructor(auth_type='something')


def test_credentials_constructor_db_type_typeerror(security_center):
    '''
    test credentials constructor for 'db type' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(db_type=1)


def test_credentials_constructor_db_type_unexpectedvalueerror(security_center):
    '''
    test credentials constructor for 'db type' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.credentials._constructor(db_type='something')


def test_credentials_constructor_port_typeerror(security_center):
    '''
    test credentials constructor for port type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(port='one')


def test_credentials_constructor_password_typeerror(security_center):
    '''
    test credentials constructor for password type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(password=1)


def test_credentials_constructor_username_typeerror(security_center):
    '''
    test credentials constructor for username type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(username=1)


def test_credentials_constructor_vault_host_typeerror(security_center):
    '''
    test credentials constructor for 'vault host' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_host=1)


def test_credentials_constructor_vault_port_typeerror(security_center):
    '''
    test credentials constructor for 'vault port' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_port='one')


def test_credentials_constructor_vault_username_typeerror(security_center):
    '''
    test credentials constructor for 'vault username' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_username=1)


def test_credentials_constructor_vault_password_typeerror(security_center):
    '''
    test credentials constructor for 'vault password' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_password=1)


def test_credentials_constructor_cyberark_url_typeerror(security_center):
    '''
    test credentials constructor for 'cyberark url' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_cyberark_url=1)


def test_credentials_constructor_vault_safe_typeerror(security_center):
    '''
    test credentials constructor for 'vault safe' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_safe=1)


def test_credentials_constructor_vault_app_id_typeerror(security_center):
    '''
    test credentials constructor for 'vault app id' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_app_id=1)


def test_credentials_constructor_vault_policy_id_typeerror(security_center):
    '''
    test credentials constructor for 'vault policy id' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_policy_id=1)


def test_crddentials_constructor_vault_folder_typeerror(security_center):
    '''
    test credentials constructor for 'vault folder' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_folder=1)


def test_credentials_constructor_vault_use_ssl_typeerror(security_center):
    '''
    test credentials constructor for 'vault use ssl' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_use_ssl='nope')


def test_credentials_constructor_verify_ssl_typeerror(security_center):
    '''
    test credentials constructor for 'verify ssl' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_verify_ssl='nope')


def test_credentials_constructor_vault_address_typeerror(security_center):
    '''
    test credentials constructor for 'vault address' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_address=1)


def test_credentials_constructor_vault_account_name_typeerror(security_center):
    '''
    test credentials constructor for 'vault account name' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_account_name=1)


def test_credentials_constructor_vault_cyberark_client_cert_typeerror(security_center):
    '''
    test credentials constructor for 'vault cyberark client cert' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_cyberark_client_cert=1)


def test_credentials_constructor_vault_cyberark_private_key_passphrase(security_center):
    '''
    test credentials constructor for 'vault cyberark private key passphrase' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(vault_cyberark_private_key_passphrase=1)


def test_credentials_constructor_lieberman_host_typeerror(security_center):
    '''
    test credentials constructor for 'lieberman host' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(lieberman_host=1)


def test_credentials_constructor_lieberman_port_typeerror(security_center):
    '''
    test credentials constructor for 'lieberman port' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(lieberman_port='one')


def test_credentials_constructor_lieberman_pam_user_typeerror(security_center):
    '''
    test credentials constructor for 'lieberman pam user' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(lieberman_pam_user=1)


def test_credentials_constructor_lieberman_pam_password_typeerror(security_center):
    '''
    test credentials constructor for 'lieberman pam password' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(lieberman_pam_password=1)


def test_credentials_constructor_lieberman_use_ssl_typeerror(security_center):
    '''
    test credentials constructor for 'lieberman use ssl' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(lieberman_use_ssl='nope')


def test_credentials_constructor_lieberman_verify_ssl_typeerror(security_center):
    '''
    test credentials constructor for 'lieberman verify ssl' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(lieberman_verify_ssl='nope')


def test_credentials_constructor_lieberman_system_name_typeerror(security_center):
    '''
    test credentials constructor for 'lieberman system name' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(lieberman_system_name=1)


def test_credentials_constructor_beyondtrust_host_typeerror(security_center):
    '''
    test credentials constructor for 'beyond trust host' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_host=1)


def test_credentials_constructor_beyondtrust_port_typeerror(security_center):
    '''
    test credentials constructor for 'beyond trust port' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_port='one')


def test_credentiald_constructor_beyondtrust_api_key_typeerror(security_center):
    '''
    test credentials constructor for 'beyond trust api key' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_api_key=1)


def test_credentials_constructor_beyondtrust_duration_typeerror(security_center):
    '''
    test credentials constructor for 'beyond trust duration' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_duration='one')


def test_credentials_constructor_use_ssl_typeerror(security_center):
    '''
    test credentials constructor for 'use ssl' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_use_ssl='nope')


def test_credentials_constructor_beyondtrust_verify_ssl_typeerror(security_center):
    '''
    test credentials constructor for 'beyond trust verify ssl' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_verify_ssl='nope')


def test_credentials_constructor_beyondtrust_use_private_key_typeerror(security_center):
    '''
    test credentials constructor for 'beyond trust use private key' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_use_private_key='nope')


def test_credentials_constructor_bveyondtrust_use_escalation_typeerror(security_center):
    '''
    test credentials constructor for 'beyond trust use escalation' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(beyondtrust_use_escalation='nope')


def test_credentials_constructor_public_key_typeerror(security_center):
    '''
    test credentials constructor for 'public key' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(public_key=1)


def test_credentials_constructor_private_key_typeerror(security_center):
    '''
    test credentials constructor for 'private key' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(private_key=1)


def test_credentials_constructor_passphrase_typeerror(security_center):
    '''
    test credentials constructor for 'passphrase' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(passphrase=1)


@pytest.mark.parametrize(
    "data, expectation",
    [
        ("Cisco 'enable'", does_not_raise()),
        (1, pytest.raises(TypeError)),
        ("something", pytest.raises(UnexpectedValueError)),
    ],
)
def test_credentials_constructor_privilege_escalation(data, expectation, security_center):
    """test case scenarios when value is valid as well as when TypeError and UnexpectedValueError exceptions are
    raised. """
    with expectation:
        assert (security_center.credentials._constructor(privilege_escalation=data)) is not None


def test_credentials_constructor_kdc_ip_typeerror(security_center):
    '''
    test credentials constructor for 'kdc ip' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(kdc_ip=1)


def test_credentials_constructor_kdc_port_typeerror(security_center):
    '''
    test credentials constructor for 'kdc port' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(kdc_port='one')


def test_credentials_constructor_kdc_protocol_typeerror(security_center):
    '''
    test credentials constructor for 'kdc protocol' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(kdc_protocol=1)


def test_credentials_constructor_kdc_protocol_unexpectedvalueerror(security_center):
    '''
    test credentials constructor for 'kdc protocol' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.credentials._constructor(kdc_protocol='something')


def test_credentials_constructor_kdc_realm_typeerror(security_center):
    '''
    test credentials constructor for 'kdc realm' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(kdc_realm=1)


def test_credentials_constructor_oracle_auth_type_typeerror(security_center):
    '''
    test credentials constructor for 'oracle auth type' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(oracle_auth_type=1)


def test_credentials_constructor_oracle_auth_type_unexpectedvalueerror(security_center):
    '''
    test credentials constructor for 'oracle auth type' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.credentials._constructor(oracle_auth_type='something')


def test_credentials_constructor_oracle_service_type_typeerror(security_center):
    '''
    test credentials constructor for 'oracle service type' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(oracle_service_type=1)


def test_credentials_constructor_oracle_service_type_unexpectedvalueerror(security_center):
    '''
    test credentials constructor for 'oracle service type' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.credentials._constructor(oracle_service_type='something')


def test_credentials_constructor_sql_server_auth_type_typeerror(security_center):
    '''
    test credentials constructor for 'sql server auth type' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(sql_server_auth_type=1)


def test_credentials_constructor_sql_server_auth_type_unexpectedvalueerror(security_center):
    '''
    test credentials constructor for 'sql server auth type' unexpected value error
    '''
    with pytest.raises(UnexpectedValueError):
        security_center.credentials._constructor(sql_server_auth_type='something')


def test_credentials_constructor_escalation_username_typeerror(security_center):
    '''
    test credentials constructor for 'escalation username' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(escalation_username=1)


def test_credentials_constructor_escalation_password_typeerror(security_center):
    '''
    test credentials constructor for 'escalation password' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(escalation_password=1)


def test_credentials_constructor_escalation_path_typeerror(security_center):
    '''
    test credentials constructor for 'escalation path' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(escalation_path=1)


def test_credentials_constructor_escalation_su_user_typeerror(security_center):
    '''
    test credentials constructor for 'escalation su user' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(escalation_su_user=1)


def test_credentials_constructor_community_string_typeerror(security_center):
    '''
    test credentials constructor for 'community string' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(community_string=1)


def test_credentials_constructor_domain_typeerror(security_center):
    '''
    test credentials constructor for 'domain' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(domain=1)


def test_credentials_constructor_thycotic_secret_name_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic secret name' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_secret_name=1)


def test_credentials_constructor_thycotic_url_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic url' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_url=1)


def test_credentials_constructor_thycotic_username_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic username' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_username=1)


def test_credentials_constructor_thycotic_password_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic password' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_password=1)


def test_credentials_constructor_thycotic_organization_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic organization' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_organization=1)


def test_credentials_constructor_thycotic_domain_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic domain' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_domain=1)


def test_credentials_constructor_thycotic_private_key_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic private key' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_private_key='nope')


def test_credentials_constructor_thycotic_ssl_verify_typeerror(security_center):
    '''
    test credentials constructor for 'thycotic ssl verify' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials._constructor(thycotic_ssl_verify='nope')


def test_credentials_constructor_success(security_center):
    '''
    test credentials constructor for success
    '''
    cred = security_center.credentials._constructor(
        name='name',
        tags='tag',
        description='description',
        type='ssh',
        login='something',
        sid='111.222.333',
        auth_type='password',
        db_type='MySQL',
        port=123,
        password='password',
        username='username',
        vault_host='vault.host',
        vault_port=1,
        vault_username='username',
        vault_password='password',
        vault_cyberark_url='http://cyberark',
        vault_safe='Safe01',
        vault_app_id='01a',
        vault_policy_id='read-only',
        vault_folder='kingdom',
        vault_use_ssl=True,
        vault_verify_ssl=False,
        vault_address='1.2.3.4',
        vault_account_name='username',
        vault_cyberark_client_cert='ABCD',
        vault_cyberark_private_key='1234',
        vault_cyberark_private_key_passphrase='sekret',
        lieberman_host='lieberman.host',
        lieberman_port=1234,
        lieberman_pam_user='user',
        lieberman_pam_password='password',
        lieberman_use_ssl=True,
        lieberman_verify_ssl=False,
        lieberman_system_name='name',
        beyondtrust_host='beyondtrust.host',
        beyondtrust_port=1234,
        beyondtrust_api_key='1234567890abcdef',
        beyondtrust_duration=60,
        beyondtrust_use_ssl=True,
        beyondtrust_verify_ssl=False,
        beyondtrust_use_private_key=False,
        beyondtrust_use_escalation=False,
        thycotic_secret_name='sekret',
        thycotic_url='http://thycotic',
        thycotic_username='username',
        thycotic_password='password',
        thycotic_organization='orgname',
        thycotic_domain='dom',
        thycotic_private_key=False,
        thycotic_ssl_verify=False,
        public_key='ABCD',
        private_key='1234',
        privilege_escalation='none',
        kdc_ip='1.2.3.4',
        kdc_port=1234,
        kdc_protocol='tcp',
        kdc_realm='something',
        oracle_auth_type='normal',
        oracle_service_type='service_name',
        sql_server_auth_type='Windows',
        escalation_username='root',
        escalation_password='password',
        escalation_path='/usr/bin',
        escalation_su_user='root',
        community_string='public',
        domain='AD'
    )
    assert isinstance(cred, dict)
    assert cred == {
        'name': 'name',
        'tags': 'tag',
        'description': 'description',
        'type': 'ssh',
        'login': 'something',
        'sid': '111.222.333',
        'authType': 'password',
        'dbType': 'MySQL',
        'port': '123',
        'password': 'password',
        'username': 'username',
        'vault_host': 'vault.host',
        'vault_port': '1',
        'vault_username': 'username',
        'vault_password': 'password',
        'vault_cyberark_url': 'http://cyberark',
        'vault_safe': 'Safe01',
        'vault_app_id': '01a',
        'vault_policy_id': 'read-only',
        'vault_folder': 'kingdom',
        'vault_use_ssl': 'true',
        'vault_verify_ssl': 'false',
        'vault_address': '1.2.3.4',
        'vault_account_name': 'username',
        'vault_cyberark_client_cert': 'ABCD',
        'vault_cyberark_private_key': '1234',
        'vault_cyberark_private_key_passphrase': 'sekret',
        'lieberman_host': 'lieberman.host',
        'lieberman_port': '1234',
        'lieberman_pam_user': 'user',
        'lieberman_pam_password': 'password',
        'lieberman_use_ssl': 'true',
        'lieberman_verify_ssl': 'false',
        'lieberman_system_name': 'name',
        'beyondtrust_host': 'beyondtrust.host',
        'beyondtrust_port': '1234',
        'beyondtrust_api_key': '1234567890abcdef',
        'beyondtrust_duration': '60',
        'beyondtrust_use_ssl': 'yes',
        'beyondtrust_verify_ssl': 'no',
        'beyondtrust_use_private_key': 'no',
        'beyondtrust_use_escalation': 'no',
        'thycotic_secret_name': 'sekret',
        'thycotic_url': 'http://thycotic',
        'thycotic_username': 'username',
        'thycotic_password': 'password',
        'thycotic_organization': 'orgname',
        'thycotic_domain': 'dom',
        'thycotic_private_key': 'no',
        'thycotic_ssl_verify': 'no',
        'publicKey': 'ABCD',
        'privateKey': '1234',
        'privilegeEscalation': 'none',
        'kdc_ip': '1.2.3.4',
        'kdc_port': '1234',
        'kdc_protocol': 'TCP',
        'kdc_realm': 'something',
        'oracleAuthType': 'NORMAL',
        'oracle_service_type': 'SERVICE_NAME',
        'SQLServerAuthType': 'Windows',
        'escalationUsername': 'root',
        'escalationPassword': 'password',
        'escalationPath': '/usr/bin',
        'escalationSuUser': 'root',
        'communityString': 'public',
        'domain': 'AD'
    }


@pytest.fixture
def cred(request, security_center, vcr):
    '''
    test fixture for credentials
    '''
    with vcr.use_cassette('test_credentials_create_success'):
        credential = security_center.credentials.create('Example Creds', 'ssh', 'password',
                                                        username='root',
                                                        password='toor',
                                                        privilege_escalation='none')

    def teardown():
        try:
            with vcr.use_cassette('test_credentials_delete_success'):
                security_center.credentials.delete(int(credential['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return credential


@pytest.mark.vcr()
def test_credentials_create_success(security_center, cred):
    '''
    test credentials create for success
    '''
    assert isinstance(cred, dict)
    check(cred, 'id', str)
    check(cred, 'type', str)
    check(cred, 'name', str)
    check(cred, 'description', str)
    check(cred, 'tags', str)
    check(cred, 'createdTime', str)
    check(cred, 'modifiedTime', str)
    check(cred, 'typeFields', dict)
    check(cred['typeFields'], 'username', str)
    check(cred['typeFields'], 'password', str)
    check(cred, 'groups', list)
    check(cred, 'canUse', str)
    check(cred, 'canManage', str)
    check(cred, 'creator', dict)
    check(cred['creator'], 'id', str)
    check(cred['creator'], 'username', str)
    check(cred['creator'], 'firstname', str)
    check(cred['creator'], 'lastname', str)
    check(cred, 'owner', dict)
    check(cred['owner'], 'id', str)
    check(cred['owner'], 'username', str)
    check(cred['owner'], 'firstname', str)
    check(cred['owner'], 'lastname', str)
    check(cred, 'ownerGroup', dict)
    check(cred['ownerGroup'], 'id', str)
    check(cred['ownerGroup'], 'name', str)
    check(cred['ownerGroup'], 'description', str)
    check(cred, 'targetGroup', dict)
    check(cred['targetGroup'], 'id', int)
    check(cred['targetGroup'], 'name', str)
    check(cred['targetGroup'], 'description', str)


@pytest.mark.vcr()
def test_credentials_delete_success(security_center, cred):
    '''
    test credentials delete for success
    '''
    security_center.credentials.delete(int(cred['id']))


def test_credentials_create_failures(security_center):
    '''
    test credentials create for failures
    '''
    with pytest.raises(TypeError):
        security_center.credentials.create('Example Creds', 'ssh', 'cyberark',
                                           username='root',
                                           password='toor',
                                           privilege_escalation='none',
                                           db_type=1)
    with pytest.raises(TypeError):
        security_center.credentials.create('Example Creds', 'ssh', 'lieberman',
                                           username='root',
                                           password='toor',
                                           privilege_escalation='none',
                                           db_type=1)
    with pytest.raises(TypeError):
        security_center.credentials.create('Example Creds', 'ssh', 'beyondtrust',
                                           username='root',
                                           password='toor',
                                           privilege_escalation='none',
                                           db_type=1)
    with pytest.raises(TypeError):
        security_center.credentials.create('Example Creds', 'ssh', 'thycotic',
                                           username='root',
                                           password='toor',
                                           privilege_escalation='none',
                                           db_type=1)
    with pytest.raises(TypeError):
        security_center.credentials.create('Example Creds', 'ssh', 'kerberos',
                                           username='root',
                                           password='toor',
                                           privilege_escalation='none',
                                           db_type=1)
    with pytest.raises(TypeError):
        security_center.credentials.create('Example Creds', 'ssh', 'kerberos',
                                           username='root',
                                           password=12323,
                                           privilege_escalation='none',
                                           db_type='Oracle')


@pytest.mark.vcr()
def test_credentials_edit_success(security_center, cred):
    '''
    test credentials edit for success
    '''
    with open("public_key.xml", "w+") as public_key:
        credential = security_center.credentials.edit(int(cred['id']), name='New Cred Name', public_key=public_key)
        assert isinstance(credential, dict)
        check(credential, 'id', str)
        check(credential, 'type', str)
        check(credential, 'name', str)
        check(credential, 'description', str)
        check(credential, 'tags', str)
        check(credential, 'createdTime', str)
        check(credential, 'modifiedTime', str)
        check(credential, 'typeFields', dict)
        check(credential['typeFields'], 'username', str)
        check(credential['typeFields'], 'password', str)
        check(credential, 'groups', list)
        check(credential, 'canUse', str)
        check(credential, 'canManage', str)
        check(credential, 'creator', dict)
        check(credential['creator'], 'id', str)
        check(credential['creator'], 'username', str)
        check(credential['creator'], 'firstname', str)
        check(credential['creator'], 'lastname', str)
        check(credential, 'owner', dict)
        check(credential['owner'], 'id', str)
        check(credential['owner'], 'username', str)
        check(credential['owner'], 'firstname', str)
        check(credential['owner'], 'lastname', str)
        check(credential, 'ownerGroup', dict)
        check(credential['ownerGroup'], 'id', str)
        check(credential['ownerGroup'], 'name', str)
        check(credential['ownerGroup'], 'description', str)
        check(credential, 'targetGroup', dict)
        check(credential['targetGroup'], 'id', int)
        check(credential['targetGroup'], 'name', str)
        check(credential['targetGroup'], 'description', str)
    os.remove("public_key.xml")


@pytest.mark.vcr()
def test_credentials_details_success(security_center, cred):
    '''
    test credentials details for success
    '''
    credential = security_center.credentials.details(int(cred['id']))
    assert isinstance(credential, dict)
    check(credential, 'id', str)
    check(credential, 'type', str)
    check(credential, 'name', str)
    check(credential, 'description', str)
    check(credential, 'tags', str)
    check(credential, 'createdTime', str)
    check(credential, 'modifiedTime', str)
    check(credential, 'typeFields', dict)
    check(credential['typeFields'], 'username', str)
    check(credential['typeFields'], 'password', str)
    check(credential, 'groups', list)
    check(credential, 'canUse', str)
    check(credential, 'canManage', str)
    check(credential, 'creator', dict)
    check(credential['creator'], 'id', str)
    check(credential['creator'], 'username', str)
    check(credential['creator'], 'firstname', str)
    check(credential['creator'], 'lastname', str)
    check(credential, 'owner', dict)
    check(credential['owner'], 'id', str)
    check(credential['owner'], 'username', str)
    check(credential['owner'], 'firstname', str)
    check(credential['owner'], 'lastname', str)
    check(credential, 'ownerGroup', dict)
    check(credential['ownerGroup'], 'id', str)
    check(credential['ownerGroup'], 'name', str)
    check(credential['ownerGroup'], 'description', str)
    check(credential, 'targetGroup', dict)
    check(credential['targetGroup'], 'id', int)
    check(credential['targetGroup'], 'name', str)
    check(credential['targetGroup'], 'description', str)


@pytest.mark.vcr()
def test_credentials_details_success_for_fields(security_center, cred):
    '''
    test credentials details success for fields
    '''
    credential = security_center.credentials.details(int(cred['id']), fields=['id', 'type', 'name', 'description'])
    assert isinstance(credential, dict)
    check(credential, 'id', str)
    check(credential, 'type', str)
    check(credential, 'name', str)
    check(credential, 'description', str)


@pytest.mark.vcr()
def test_credentials_tags_success(security_center):
    '''
    test credentials tag for success
    '''
    tags = security_center.credentials.tags()
    for tag in tags:
        single(tag, str)


@pytest.mark.vcr()
def test_credentials_share_id_typeerror(security_center):
    '''
    test credentials share for id type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials.share('one')


@pytest.mark.vcr()
def test_credentials_share_group_id_typeerror(security_center):
    '''
    test credentials share for 'group id' type error
    '''
    with pytest.raises(TypeError):
        security_center.credentials.share(1, 'one')


@pytest.mark.vcr()
def test_credentials_share_success(security_center, cred, group):
    '''
    test credentials share for success
    '''
    credential = security_center.credentials.share(int(cred['id']), int(group['id']))
    assert isinstance(credential, dict)
    check(credential, 'id', str)
    check(credential, 'type', str)
    check(credential, 'name', str)
    check(credential, 'description', str)
    check(credential, 'tags', str)
    check(credential, 'createdTime', str)
    check(credential, 'modifiedTime', str)
    check(credential, 'typeFields', dict)
    check(credential['typeFields'], 'username', str)
    check(credential['typeFields'], 'password', str)
    check(credential, 'groups', list)
    check(credential, 'canUse', str)
    check(credential, 'canManage', str)
    check(credential, 'creator', dict)
    check(credential['creator'], 'id', str)
    check(credential['creator'], 'username', str)
    check(credential['creator'], 'firstname', str)
    check(credential['creator'], 'lastname', str)
    check(credential, 'owner', dict)
    check(credential['owner'], 'id', str)
    check(credential['owner'], 'username', str)
    check(credential['owner'], 'firstname', str)
    check(credential['owner'], 'lastname', str)
    check(credential, 'ownerGroup', dict)
    check(credential['ownerGroup'], 'id', str)
    check(credential['ownerGroup'], 'name', str)
    check(credential['ownerGroup'], 'description', str)
    check(credential, 'targetGroup', dict)
    check(credential['targetGroup'], 'id', int)
    check(credential['targetGroup'], 'name', str)
    check(credential['targetGroup'], 'description', str)


@pytest.mark.vcr()
def test_credentials_list_success(security_center):
    '''
    test credentials list for success
    '''
    credentials = security_center.credentials.list(fields=['id', 'type', 'name', 'description'])
    assert isinstance(credentials, list)
    for credential in credentials:
        check(credential, 'id', str)
        check(credential, 'type', str)
        check(credential, 'name', str)
        check(credential, 'description', str)
