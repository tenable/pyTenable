from tenable.errors import *
from ..checker import check, single
import pytest

def test_credentials_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(name=1)

def test_credentials_constructor_tags_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(tags=1)

def test_credentials_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(description=1)

def test_credentialsd_constructor_login_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(login=1)

def test_credentials_constructor_sid_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(sid=1)

def test_credentials_constructor_auth_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(auth_type=1)

def test_credentials_constructor_auth_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.credentials._constructor(auth_type='something')

def test_credentials_constructor_db_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(db_type=1)

def test_credentials_constructor_db_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.credentials._constructor(db_type='something')

def test_credentials_constructor_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(port='one')

def test_credentials_constructor_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(password=1)

def test_credentials_constructor_username_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(username=1)

def test_credentials_constructor_vaul_host_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_host=1)

def test_credentials_constructor_vault_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_port='one')

def test_credentials_constructor_vault_username_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_username=1)

def test_credentials_constructor_vault_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_password=1)

def test_credentials_constructor_cynerark_url(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_cyberark_url=1)

def test_credentials_constructor_vault_safe_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_safe=1)

def test_credentials_constructor_vault_app_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_app_id=1)

def test_credentials_constructor_vault_policy_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_policy_id=1)

def test_crddentials_constructor_vault_folder_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_folder=1)

def test_credentials_constructor_vault_use_ssl_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_use_ssl='nope')

def test_credentials_constructor_verify_ssl_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_verify_ssl='nope')

def test_credentials_constructor_vault_address_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_address=1)

def test_credentials_constructor_vault_account_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_account_name=1)

def test_credentials_constructor_vault_cyberark_client_cert_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_cyberark_client_cert=1)

def test_credentials_constructor_vault_cyberark_private_key_passphrase(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(vault_cyberark_private_key_passphrase=1)

def test_credentials_constructor_lieberman_host_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(lieberman_host=1)

def test_credentials_constructor_lieberman_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(lieberman_port='one')

def test_credentials_constructor_lieberman_pam_user_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(lieberman_pam_user=1)

def test_credentials_constructor_lieberman_pam_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(lieberman_pam_password=1)

def test_credentials_constructor_lieberman_use_ssl_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(lieberman_use_ssl='nope')

def test_credentials_constructor_lieberman_verify_ssl_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(lieberman_verify_ssl='nope')

def test_credentials_constructor_lieberman_system_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(lieberman_system_name=1)

def test_credentials_constructor_beyondtrust_host_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_host=1)

def test_credentials_constructor_beyondtrust_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_port='one')

def test_credentiald_constructor_beyondtrust_api_key_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_api_key=1)

def test_credentials_constructor_beyondtrust_duration_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_duration='one')

def test_credentials_constructor_use_ssl_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_use_ssl='nope')

def test_credentials_constructor_beyondtrust_verify_ssl_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_verify_ssl='nope')

def test_credentials_constructor_beyondtrust_use_private_key_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_use_private_key='nope')

def test_credentials_constructor_bveyondtrust_use_escalation_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(beyondtrust_use_escalation='nope')

def test_credentials_constructor_public_key_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(public_key=1)

def test_credentials_constructor_private_key_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(private_key=1)

def test_credentials_constructor_passphrase_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(passphrase=1)

def test_credentials_constructor_privilege_escalation_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(privilege_escalation=1)

def test_credentials_constructor_privilege_escalation_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.credentials._constructor(privilege_escalation='something')

def test_credentials_constructor_kdc_ip_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(kdc_ip=1)

def test_credentials_constructor_kdc_port_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(kdc_port='one')

def test_credentials_constructor_kdc_protocol_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(kdc_protocol=1)

def test_credentials_constructor_kdc_protocol_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.credentials._constructor(kdc_protocol='something')

def test_credentials_constructor_kdc_realm_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(kdc_realm=1)

def test_credentials_constructor_oracle_auth_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(oracle_auth_type=1)

def test_credentials_constructor_oracle_auth_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.credentials._constructor(oracle_auth_type='something')

def test_credentials_constructor_oracle_service_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(oracle_service_type=1)

def test_credentials_constructor_oracle_service_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.credentials._constructor(oracle_service_type='something')

def test_credentials_constructor_sql_server_auth_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(sql_server_auth_type=1)

def test_credentials_constructor_sql_server_auth_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.credentials._constructor(sql_server_auth_type='something')

def test_credentials_constructor_escalation_username_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(escalation_username=1)

def test_credentials_constructor_escalation_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(escalation_password=1)

def test_credentials_constructor_escalation_path_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(escalation_path=1)

def test_credentials_constructor_escalation_su_user_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(escalation_su_user=1)

def test_credentials_constructor_community_string_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(community_string=1)

def test_credentials_constructor_domain_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(domain=1)

def test_credentials_constructor_thycotic_secret_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_secret_name=1)

def test_credentials_constructor_thycotic_url_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_url=1)

def test_credentials_constructor_thycotic_username_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_username=1)

def test_credentials_constructor_thycotic_password_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_password=1)

def test_credentials_constructor_thycotic_organization_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_organization=1)

def test_credentials_constructor_thycotic_domain_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_domain=1)

def test_credentials_constructor_thycotic_private_key_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_private_key='nope')

def test_credentials_constructor_thycotic_ssl_verify_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials._constructor(thycotic_ssl_verify='nope')

def test_credentials_constructor_success(sc):
    cred = sc.credentials._constructor(
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
def cred(request, sc, vcr):
    with vcr.use_cassette('test_credentials_create_success'):
        c = sc.credentials.create('Example Creds', 'ssh', 'password',
            username='root',
            password='toor',
            privilege_escalation='none')
    def teardown():
        try:
            with vcr.use_cassette('test_credentials_delete_success'):
                sc.credentials.delete(int(c['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return c

@pytest.mark.vcr()
def test_credentials_create_success(sc, cred):
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
def test_credentials_delete_success(sc, cred):
    sc.credentials.delete(int(cred['id']))

@pytest.mark.vcr()
def test_credentials_edit_success(sc, cred):
    c = sc.credentials.edit(int(cred['id']), name='New Cred Name')
    assert isinstance(c, dict)
    check(c, 'id', str)
    check(c, 'type', str)
    check(c, 'name', str)
    check(c, 'description', str)
    check(c, 'tags', str)
    check(c, 'createdTime', str)
    check(c, 'modifiedTime', str)
    check(c, 'typeFields', dict)
    check(c['typeFields'], 'username', str)
    check(c['typeFields'], 'password', str)
    check(c, 'groups', list)
    check(c, 'canUse', str)
    check(c, 'canManage', str)
    check(c, 'creator', dict)
    check(c['creator'], 'id', str)
    check(c['creator'], 'username', str)
    check(c['creator'], 'firstname', str)
    check(c['creator'], 'lastname', str)
    check(c, 'owner', dict)
    check(c['owner'], 'id', str)
    check(c['owner'], 'username', str)
    check(c['owner'], 'firstname', str)
    check(c['owner'], 'lastname', str)
    check(c, 'ownerGroup', dict)
    check(c['ownerGroup'], 'id', str)
    check(c['ownerGroup'], 'name', str)
    check(c['ownerGroup'], 'description', str)
    check(c, 'targetGroup', dict)
    check(c['targetGroup'], 'id', int)
    check(c['targetGroup'], 'name', str)
    check(c['targetGroup'], 'description', str)

@pytest.mark.vcr()
def test_credentials_details_success(sc, cred):
    c = sc.credentials.details(int(cred['id']))
    assert isinstance(c, dict)
    check(c, 'id', str)
    check(c, 'type', str)
    check(c, 'name', str)
    check(c, 'description', str)
    check(c, 'tags', str)
    check(c, 'createdTime', str)
    check(c, 'modifiedTime', str)
    check(c, 'typeFields', dict)
    check(c['typeFields'], 'username', str)
    check(c['typeFields'], 'password', str)
    check(c, 'groups', list)
    check(c, 'canUse', str)
    check(c, 'canManage', str)
    check(c, 'creator', dict)
    check(c['creator'], 'id', str)
    check(c['creator'], 'username', str)
    check(c['creator'], 'firstname', str)
    check(c['creator'], 'lastname', str)
    check(c, 'owner', dict)
    check(c['owner'], 'id', str)
    check(c['owner'], 'username', str)
    check(c['owner'], 'firstname', str)
    check(c['owner'], 'lastname', str)
    check(c, 'ownerGroup', dict)
    check(c['ownerGroup'], 'id', str)
    check(c['ownerGroup'], 'name', str)
    check(c['ownerGroup'], 'description', str)
    check(c, 'targetGroup', dict)
    check(c['targetGroup'], 'id', int)
    check(c['targetGroup'], 'name', str)
    check(c['targetGroup'], 'description', str)

@pytest.mark.vcr()
def test_credentials_tags_success(sc):
    tags = sc.credentials.tags()
    for tag in tags:
        single(tag, str)

@pytest.mark.vcr()
def test_credentials_share_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials.share('one')

@pytest.mark.vcr()
def test_credentials_share_group_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.credentials.share(1, 'one')

@pytest.mark.vcr()
def test_credentials_share_success(sc, cred, group):
    c = sc.credentials.share(int(cred['id']), int(group['id']))
    assert isinstance(c, dict)
    check(c, 'id', str)
    check(c, 'type', str)
    check(c, 'name', str)
    check(c, 'description', str)
    check(c, 'tags', str)
    check(c, 'createdTime', str)
    check(c, 'modifiedTime', str)
    check(c, 'typeFields', dict)
    check(c['typeFields'], 'username', str)
    check(c['typeFields'], 'password', str)
    check(c, 'groups', list)
    check(c, 'canUse', str)
    check(c, 'canManage', str)
    check(c, 'creator', dict)
    check(c['creator'], 'id', str)
    check(c['creator'], 'username', str)
    check(c['creator'], 'firstname', str)
    check(c['creator'], 'lastname', str)
    check(c, 'owner', dict)
    check(c['owner'], 'id', str)
    check(c['owner'], 'username', str)
    check(c['owner'], 'firstname', str)
    check(c['owner'], 'lastname', str)
    check(c, 'ownerGroup', dict)
    check(c['ownerGroup'], 'id', str)
    check(c['ownerGroup'], 'name', str)
    check(c['ownerGroup'], 'description', str)
    check(c, 'targetGroup', dict)
    check(c['targetGroup'], 'id', int)
    check(c['targetGroup'], 'name', str)
    check(c['targetGroup'], 'description', str)