'''
credentials
===========

The following methods allow for interaction into the Tenable.sc
:sc-api:`Scan Credentials <Credential.html>` API.  These
items are typically seen under the **Scan Credentials** section of Tenable.sc.

Methods available on ``sc.credentials``:

.. rst-class:: hide-signature
.. autoclass:: CredentialAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import SCEndpoint

class CredentialAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a credential definition document
        '''
        yn = {False: 'no', True: 'yes'}

        if 'name' in kw:
            # Validate that the name parameter is a string.
            self._check('name', kw['name'], str)

        if 'tags' in kw:
            # Validate that the tags parameter is a string.
            self._check('tags', kw['tags'], str)

        if 'description' in kw:
            # Validate that the description parameter is a string.
            self._check('description', kw['description'], str)

        if 'type' in kw:
            # Validate that the type parameter is a string and falls within the
            # expected types.
            self._check('type', kw['type'], str,
                choices=['database', 'windows', 'snmp', 'ssh'])

        if 'login' in kw:
            # Validate that the login paramater is a string.
            self._check('login', kw['login'], str)

        if 'sid' in kw:
            # Validate that the sid parameter is a string.
            self._check('sid', kw['sid'], str)

        if 'auth_type' in kw:
            # Validate that the auth_type paramater is a string of the expected
            # values and then convert it to the camelCase equiv.
            kw['authType'] = self._check('auth_type', kw['auth_type'], str,
                choices=['cyberark', 'lieberman', 'password', 'BeyondTrust',
                         'certificate', 'kerberos', 'publicKey', 'thycotic',
                         'lm', 'ntlm'])
            del(kw['auth_type'])

        if 'db_type' in kw:
            # Validate that the db_type parameter is a string of one of the
            # expected values and then convert it to the camelCase equiv.
            kw['dbType'] = self._check('db_type', kw['db_type'], str,
                choices=['Oracle', 'SQL Server', 'DB2', 'MySQL', 'PostgreSQL',
                         'Informix/DRDA'])
            del (kw['db_type'])

        if 'port' in kw:
            # Validate that the port parameter is a integer and then store the
            # resulting value as a string.
            kw['port'] = str(self._check('port', kw['port'], int))

        if 'password' in kw:
            # Validate that the password parameter is a string type.
            self._check('password', kw['password'], str)

        if 'username' in kw:
            # validate that the username parameter is a string type.
            self._check('username', kw['username'], str)

        ## CYBERARK AUTH TYPE
        if 'vault_host' in kw:
            # Validate that the vault_host parameter is a string type.
            self._check('vault_host', kw['vault_host'], str)

        if 'vault_port' in kw:
            # Validate that the vault_port parameter was passed as an integer
            # and then store it as a string.
            kw['vault_port'] = str(self._check(
                'vault_port', kw['vault_port'], int))

        if 'vault_username' in kw:
            # Validate that vault_username is a string.
            self._check('vault_username', kw['vault_username'], str)

        if 'vault_password' in kw:
            # validate that the vault_password is a string.
            self._check('vault_password', kw['vault_password'], str)

        if 'vault_cyberark_url' in kw:
            # Validate that the vault_cyberark_url parameter is a string.
            self._check('vault_cyberark_url', kw['vault_cyberark_url'], str)

        if 'vault_safe' in kw:
            # Validate that the vault_safe parameter is a string.
            self._check('vault_safe', kw['vault_safe'], str)

        if 'vault_app_id' in kw:
            # Validate that the vault_app_id parameter is a string.
            self._check('vault_app_id', kw['vault_app_id'], str)

        if 'vault_policy_id' in kw:
            # Validate that the vault_policy_id parameter is a string.
            self._check('vault_policy_id', kw['vault_policy_id'], str)

        if 'vault_folder' in kw:
            # Validate that the vault_folder parameter is a string.
            self._check('vault_folder', kw['vault_folder'], str)

        if 'vault_use_ssl' in kw:
            # Validate that the vault_ssl parameter is a boolean value and then
            # store it as a lowercased string.
            kw['vault_use_ssl'] = str(self._check(
                'vault_use_ssl', kw['vault_use_ssl'], bool)).lower()

        if 'vault_verify_ssl' in kw:
            # Validate that the vault_verify_ssl parameter is a boolean value and
            # then store is as a lowercased string.
            kw['vault_verify_ssl'] = str(self._check(
                'vault_verify_ssl', kw['vault_verify_ssl'], bool)).lower()

        if 'vault_address' in kw:
            # Validate that the vault_address parameter is a string.
            self._check('vault_address', kw['vault_address'], str)

        if 'vault_account_name' in kw:
            # Verify that the vault_account_name parameter is a string.
            self._check('vault_account_name', kw['vault_account_name'], str)

        if 'vault_cyberark_client_cert' in kw:
            # verify that the vault_cyberark_client_cert is a string.
            self._check('vault_cyberark_client_cert',
                kw['vault_cyberark_client_cert'], str)

        if 'vault_cyberark_private_key' in kw:
            # verify that the vault_cyberark_private_key param is a string.
            self._check('vault_cyberark_private_key',
                        kw['vault_cyberark_private_key'], str)

        if 'vault_cyberark_private_key_passphrase' in kw:
            # Validate that the private key passphrase param is a string.
            self._check('vault_cyberark_private_key_passphrase',
                        kw['vault_cyberark_private_key_passphrase'], str)

        ### LIEBERMAN AUTH TYPE
        if 'lieberman_host' in kw:
            # validate that the lieberman_host param is a string.
            self._check('lieberman_host', kw['lieberman_host'], str)

        if 'lieberman_port' in kw:
            # Validate that the lieberman port param is an integer and then
            # store it as a string.
            kw['lieberman_port'] = str(
                self._check('lieberman_port', kw['lieberman_port'], int))

        if 'lieberman_pam_user' in kw:
            # Validate that the lieberman_pam_user param is a string.
            self._check('lieberman_pam_user', kw['lieberman_pam_user'], str)

        if 'lieberman_pam_password' in kw:
            # Validate that the lieberman_pam_password param is a string.
            self._check('lieberman_pam_password',
                kw['lieberman_pam_password'], str)

        if 'lieberman_use_ssl' in kw:
            # Validate that the SSL flag is a boolean value and store it as a
            # lower-cased string.
            kw['lieberman_use_ssl'] = str(
                self._check('lieberman_use_ssl',
                    kw['lieberman_use_ssl'], bool)).lower()

        if 'lieberman_verify_ssl' in kw:
            # Validate that the verify SSL flag is a boolean value and store
            # it as a lower-cased string.
            kw['lieberman_verify_ssl'] = str(
                self._check('lieberman_verify_ssl',
                    kw['lieberman_verify_ssl'], bool)).lower()

        if 'lieberman_system_name' in kw:
            # Validate that the system name is a string.
            self._check('lieberman_system_name',
                kw['lieberman_system_name'], str)

        ### BEYONDTRUST AUTH TYPE
        if 'beyondtrust_host' in kw:
            # Validate that the beyondtrust_host param is a string.
            self._check('beyondtrust_host', kw['beyondtrust_host'], str)

        if 'beyondtrust_port' in kw:
            # Validate that the beyondtrust_port is an integer and store it as
            # a string.
            kw['beyondtrust_port'] = str(self._check(
                'beyondtrust_port', kw['beyondtrust_port'], int))

        if 'beyondtrust_api_key' in kw:
            # Validate that the beyondtrust_api_key is a string.
            self._check('beyondtrust_api_key', kw['beyondtrust_api_key'], str)

        if 'beyondtrust_duration' in kw:
            # Validate that the beyondtrust_duration is an integer value and
            # store it as a string.
            kw['beyondtrust_duration'] = str(self._check(
                'beyondtrust_duration', kw['beyondtrust_duration'], int))

        if 'beyondtrust_use_ssl' in kw:
            # Validate that the use_ssl toggle is a boolean value and then store
            # it as a yes/no string response.
            kw['beyondtrust_use_ssl'] = yn[self._check(
                'beyondtrust_use_ssl', kw['beyondtrust_use_ssl'], bool)]

        if 'beyondtrust_verify_ssl' in kw:
            # Validate that the verify_ssl toggle is a boolean value and then
            # store it as a yes/no string response.
            kw['beyondtrust_verify_ssl'] = yn[self._check(
                'beyondtrust_verify_ssl', kw['beyondtrust_verify_ssl'], bool)]

        if 'beyondtrust_use_private_key' in kw:
            # Validate that the use_private_key toggle is a boolean value and
            # then store it as a yes/no string response.
            kw['beyondtrust_use_private_key'] = yn[self._check(
                'beyondtrust_use_private_key',
                kw['beyondtrust_use_private_key'], bool)]

        if 'beyondtrust_use_escalation' in kw:
            # Validate that the use_escalation toggle is a boolean value and
            # then store it as a yes/no string response.
            kw['beyondtrust_use_escalation'] = yn[self._check(
                'beyondtrust_use_escalation',
                kw['beyondtrust_use_escalation'], bool)]

        ### AUTHTYPE THYCOTIC
        if 'thycotic_secret_name' in kw:
            # Validate that the secret name param is a string.
            self._check('thycotic_secret_name', kw['thycotic_secret_name'], str)

        if 'thycotic_url' in kw:
            # Validate that the url is a string.
            self._check('thycotic_url', kw['thycotic_url'], str)

        if 'thycotic_username' in kw:
            # Validate that the username is a string.
            self._check('thycotic_username', kw['thycotic_username'], str)

        if 'thycotic_password' in kw:
            # Validate that the password is a string.
            self._check('thycotic_password', kw['thycotic_password'], str)

        if 'thycotic_organization' in kw:
            # Validate that the organization is a string.
            self._check('thycotic_organization',
                kw['thycotic_organization'], str)

        if 'thycotic_domain' in kw:
            # Validate that the domain is a string.
            self._check('thycotic_domain', kw['thycotic_domain'], str)

        if 'thycotic_private_key' in kw:
            # Validate that the private key flag is a boolean value and then
            # store it as a yes/no string equiv.
            kw['thycotic_private_key'] = yn[self._check('thycotic_private_key',
                kw['thycotic_private_key'], bool)]

        if 'thycotic_ssl_verify' in kw:
            # Validate that the ssl verification flag is a boolean value and
            # then store it as a yes/no string equiv.
            kw['thycotic_ssl_verify'] = yn[self._check('thycotic_ssl_verify',
                kw['thycotic_ssl_verify'], bool)]

        ### AUTHTYPE CERTIFICATE
        if 'public_key' in kw:
            # Validate that the public_key param is a string and then store in
            # the camelCase equiv.
            kw['publicKey'] = self._check('public_key', kw['public_key'], str)
            del(kw['public_key'])

        if 'private_key' in kw:
            # Validate that the private_key param is a string and then store it
            # in the camelCase equiv.
            kw['privateKey'] = self._check('private_key', kw['private_key'], str)
            del(kw['private_key'])

        if 'passphrase' in kw:
            # validate that the passphrase param is a string.
            self._check('passphrase', kw['passphrase'], str)

        if 'privilege_escalation' in kw:
            # validate that privilege_escalation is a string value of one of the
            # expected types and store it in the camelCase equiv.
            kw['privilegeEscalation'] = self._check('privilege_escalation',
                kw['privilege_escalation'], str, choices=[
                    'none', 'su', 'sudo', 'su+sudo',
                    'dzdo', 'pbrun', 'cisco', '.k5login'])
            del(kw['privilege_escalation'])

        ### KERBEROS AUTHTYPE
        if 'kdc_ip' in kw:
            # validate that the ip value is a string.
            self._check('kdc_ip', kw['kdc_ip'], str)

        if 'kdc_port' in kw:
            # validate that the port value is an integer and store it as a str.
            kw['kdc_port'] = str(self._check('kdc_port', kw['kdc_port'], int))

        if 'kdc_protocol' in kw:
            # validate that the protocol value is a string.
            kw['kdc_protocol'] = self._check(
                'kdc_protocol', kw['kdc_protocol'], str, case='upper',
                choices=['UDP', 'TCP'])

        if 'kdc_realm' in kw:
            # validate that the realm value is a string.
            self._check('kdc_realm', kw['kdc_realm'], str)

        ### ORACLE DB TYPE
        if 'oracle_auth_type' in kw:
            # Validate that the oracle_auth_type var is a string and then store
            # it in the camelCased equiv.
            kw['oracleAuthType'] = self._check(
                'oracle_auth_type', kw['oracle_auth_type'], str, case='upper',
                choices=['SYSDBA', 'SYSOPER', 'NORMAL'])
            del(kw['oracle_auth_type'])

        if 'oracle_service_type' in kw:
            # Validate that the oracle_service_type var is a string.
            kw['oracle_service_type'] = self._check(
                'oracle_service_type', kw['oracle_service_type'], str,
                case='upper', choices=['SID', 'SERVICE_NAME'])

        ### SQL SERVER DB TYPE
        if 'sql_server_auth_type' in kw:
            # Validate that the sql_server_auth_type var is a string and store
            # it in the camelCased variant expected,
            kw['SQLServerAuthType'] = self._check(
                'sql_server_auth_type', kw['sql_server_auth_type'], str,
                choices=['SQL', 'Windows'])
            del(kw['sql_server_auth_type'])

        ### PRIV ESCALATION PARAMS
        if 'escalation_username' in kw:
            # Verify that the escalation username is a string and store it in
            # the camelCase equiv.
            kw['escalationUsername'] = self._check('escalation_username',
                kw['escalation_username'], str)
            del(kw['escalation_username'])

        if 'escalation_password' in kw:
            # Validate that the escalation password is a string and store it in
            # the camelCase equiv.
            kw['escalationPassword'] = self._check('escalation_password',
                kw['escalation_password'], str)
            del(kw['escalation_password'])

        if 'escalation_path' in kw:
            # Validate that the escalation path is a string and store it in the
            # camelCase equiv.
            kw['escalationPath'] = self._check('escalation_path',
                kw['escalation_path'], str)
            del(kw['escalation_path'])

        if 'escalation_su_user' in kw:
            # Validate that the escalation SU user is a string and store it in
            # the camelCase equiv.
            kw['escalationSuUser'] = self._check('escalation_su_user',
                kw['escalation_su_user'], str)
            del(kw['escalation_su_user'])

        if 'community_string' in kw:
            # Validate that the community string is a string value and store it
            # in the camelCase equiv.
            kw['communityString'] = self._check(
                'community_string', kw['community_string'], str)
            del(kw['community_string'])

        ### WINDOWS AUTH TYPE STUFF
        if 'domain' in kw:
            # Validate that the domain param is a string.
            self._check('domain', kw['domain'], str)

        return kw

    def _upload_files(self, **kw):
        '''
        Uploads the file objects specified and returns the filename attributes
        associated to each keyword.
        '''
        uploadable_keys = [
            'vault_cyberark_client_cert', 'vault_cyberark_private_key',
            'public_key', 'private_key',
        ]

        for key in uploadable_keys:
            if key in kw:
                kw[key] = self._api.files.upload(kw[key])
        return kw

    def create(self, name, cred_type, auth_type, **kw):
        '''
        Creates a credential.

        :sc-api:`credential: create <Credential.html#credential_POST>`

        Args:
            name (str): The name for the credential.
            cred_type (str):
                The type of credential to store.  Valid types are ``database``,
                ``snmp``, ``ssh``, and ``windows``.
            auth_type (str):
                The type of authentication for the credential.  Valid types are
                ``beyondtrust``, ``certificate``, cyberark``, ``kerberos``,
                ``lieberman``, ``lm``, ``ntlm``, ``password``, ``publickey``,
                ``thycotic``.
            beyondtrust_api_key (str, optional):
                The API key to use for authenticating to Beyondtrust.
            beyondtrust_duration (int, optional):
                The length of time to cache the checked-out credentials from
                Beyondtrust.  This value should be less than the password change
                interval within Beyondtrust.
            beyondtrust_host (str, optional):
                The host address for the Beyondtrust application.
            beyondtrust_port (int, optional):
                The port number associated with the Beyondtrust application.
            beyondtrust_use_escalation (bool, optional):
                If enabled, informs the scanners to use Beyondtrust for
                privilege escalation.
            beyondtrust_use_private_key (bool, optional):
                If enabled, informs the scanners to use key-based auth for SSH
                connections instead of password auth.
            beyondtrust_use_ssl (bool, optional):
                Should the scanners communicate to Beyondtrust over SSL for
                credential retrieval?  If left unspecified, the default is set
                to ``True``.
            beyondtrust_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                Beyondtrust?  If left unspecified, the default is ``False``.
            community_string (str, optional):
                The SNMP community string to use for authentication.
            db_type (str, optional):
                The type of database connection that will be performed.  Valid
                types are ``DB2``, ``Informix/DRDA``, ``MySQL``, ``Oracle``,
                ``PostgreSQL``, ``SQL Server``.
            description (str, optional):
                A description to associate to the credential.
            domain (str, optional):
                The Active Directory domain to use if the user is a member of a
                domain.
            escalation_path (str, optional):
                The path in which to run the escalation commands.
            escalation_password (str, optional):
                The password to use for the escalation.
            escalation_su_use (str, optional):
                If performing an SU escalation, this is the user to escalate to.
            escalation_username (str, optional):
                The username to escalate to.
            kdc_ip (str, optional):
                The kerberos host supplying the session tickets.
            kdc_port (int, optional):
                The port to use for kerberos connections.  If left unspecified
                the default is ``88``.
            kdc_protocol (str, optional):
                The protocol to use for kerberos connections.  Valid options are
                ``tcp`` and ``udp``.  If left unspecified then the default is
                ``tcp``.
            kdc_realm (str, optional):
                The Kerberos realm to use for authentication.
            lieberman_host (str, optional):
                The address for the Lieberman vault.
            lieberman_port (int, optional):
                The port number where the Lieberman service is listening.
            lieberman_pam_password (str, optional):
                The password to authenticate to the Lieberman RED API.
            lieberman_pam_user (str, optional):
                The username to authenticate to the Lieberman RED API.
            lieberman_system_name (str, optional):
                The name for the credentials in Lieberman.
            lieberman_use_ssl (bool, optional):
                Should the scanners communicate to Lieberman over SSL for
                credential retrieval?  If left unspecified, the default is set
                to ``True``.
            lieberman_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                Lieberman?  If left unspecified, the default is ``False``.
            password (str, optional):
                The password for the credential.
            port (int, optional):
                A valid port number for a database credential.
            privilege_escalation (str, optional):
                The type of privilege escalation to perform once authenticated.
                Valid values are ``.k5login``, ``cisco``, ``dzdo``, ``none``,
                ``pbrun``, ``su``, ``su+sudo``, ``sudo``.  If left unspecified,
                the default is ``none``.
            oracle_auth_type (str, optional):
                The type of authentication to use when communicating to an
                Oracle database server.  Supported values are ``sysdba``,
                ``sysoper``, and ``normal``.  If left unspecified, the default
                option is ``normal``.
            oracle_service_type (str, optional):
                The type of service identifier specified in the ``sid``
                parameter.  Valid values are either ``sid`` or ``service_name``.
                If left unspecified, the default is ``sid``.
            sid (str, optional):
                The service identifier or name for a database credential.
            sql_server_auth_type (str, optional):
                The type of authentication to perform to the SQL Server
                instance.  Valid values are ``SQL`` and ``Windows``.  The default
                value if left unspecified is ``SQL``.
            tags (str, optional):
                A tag to associate to the credential.
            username (str, optional):
                The username for the OS credential.
            thycotic_domain (str, optional):
                The domain, if set, within Thycotic.
            thycotic_organization (str, optional):
                The organization to use if using a cloud instance of Thycotic.
            thycotic_password (str, optional):
                The password to use when authenticating to Thycotic.
            thycotic_private_key (bool, optional):
                If enabled, informs the scanners to use key-based auth for SSH
                connections instead of password auth.
            thycotic_secret_name (str, optional):
                The secret name value on the Tycotic server.
            thycotic_url (str, optional):
                The absolute URL path pointing to the Thycotic secret server.
            thycotic_username (str, optional):
                The username to use to authenticate to Thycotic.
            thycotic_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                Thycotic?  If left unspecified, the default is ``False``.
            vault_account_name (str, optional):
                The unique name of the credential to retrieve from CyberArk.
                Generally referred to as the *name* paramater within CyberArk.
            vault_address (str, optional):
                The domain for the CyberArk account.  SSL must be configured
                through IIS on the CCP before using.
            vault_app_id (str, optional):
                The AppID to use with CyberArk.
            vault_cyberark_client_cert (file, optional):
                The fileobject containing the CyberArk client certificate.
            vault_cyberark_url (str, optional):
                The URL for the CyberArk AIM web service. If left unspecified,
                the default URL path of ``/AIMWebservice/v1.1/AIM.asmx`` will be
                used..
            vault_cyberark_private_key (file, optional):
                The fileobject containing the CyberArk client private key.
            vault_cyberark_private_key_passphrase (str, optional):
                The passhrase for the private key.
            vault_folder (str, optional):
                The folder to use within CyberArk for credential retrieval.
            vault_host (str, optional):
                The CyberArk Vault host.
            vault_password (str, optional):
                The password to use for authentication to the vault if
                the CyberArk Central Credential Provider is configured for
                basic auth.
            vault_policy_id (int, optional):
                The CyberArk PolicyID assigned to the credentials to retrieve.
            vault_port (int, optional):
                The port in which the CyberArk Vault resides.
            vault_safe (str, optional):
                The CyberArk safe that contains the credentials to retrive.
            vault_use_ssl (bool, optional):
                Should the scanners communicate to CyberArk over SSL for
                credential retrieval?  If left unspecified, the default is set
                to ``True``.
            vault_username (str, optional):
                The username to use for authentication to the vault if
                the CyberArk Central Credential Provider is configured for
                basic auth.
            vault_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                the vault?  If left unspecified, the default is ``False``.

        Returns:
            :obj:`dict`:
                The newly created credential.

        Examples:
            Creating a Windows AD credential:

            >>> cred = sc.credentials.create(
            ...     'Example AD User', 'windows', 'ntlm',
            ...     username='scanneruser',
            ...     password='sekretpassword',
            ...     domain='Company.com')

            Creating a root user SSH credential:

            >>> cred = sc.credentials.create(
            ...     'Example SSH Cred', 'ssh', 'password',
            ...     username='root',
            ...     password='sekretpassword')

            Creating a root user SSH cred with a private key:

            >>> with open('privatekeyfile', 'rb') as keyfile:
            ...     cred = sc.credentials.create(
            ...         'Example SSH Keys', 'ssh', 'publicKey',
            ...         username='root',
            ...         private_key=keyfile)

            Creating a normal user SSH cred with sudo for privilege escalation:

            >>> cred = sc.credentials.create(
            ...     'Example SSH Sudo', 'ssh', 'password',
            ...     username='user',
            ...     password='sekretpassword',
            ...     privilege_escalation='sudo',
            ...     escalation_password='sekretpassword')

            Creating a SQL Server cred set:

            >>> cred = sc.credentials.create(
            ...     'Example SQL Server', 'database', 'SQL Server',
            ...     username='sa',
            ...     password='sekretpassword',
            ...     sql_server_auth_type='SQL',
            ...     sid='database_name')
        '''
        kw['name'] = name
        kw['type'] = cred_type
        kw['auth_type'] = auth_type

        # Setting some default values depending on whats passed.  Generally
        # speaking we want to default to using SSL, however by default not
        # verify the SSL certificate (as generally these are on-prem systems
        # with a self-signed cert)
        if auth_type == 'cyberark':
            kw['vault_use_ssl'] = kw.get('vault_use_ssl', True)
            kw['vault_verify_ssl'] = kw.get('vault_verify_ssl', False)
        elif auth_type == 'lieberman':
            kw['lieberman_use_ssl'] = kw.get('lieberman_use_ssl', True)
            kw['lieberman_verify_ssl'] = kw.get('lieberman_verify_ssl', False)
        elif auth_type == 'beyondtrust':
            kw['auth_type'] = 'BeyondTrust'
            kw['beyondtrust_use_ssl'] = kw.get('beyondtrust_use_ssl', True)
            kw['beyondtrust_verify_ssl'] = kw.get(
                'beyondtrust_verify_ssl', False)
            kw['beyondtrust_use_private_key'] = kw.get(
                'beyondtrust_use_private_key', False)
            kw['beyondtrust_use_escalation'] = kw.get(
                'beyondtrust_use_escalation', False)
        elif auth_type == 'thycotic':
            kw['thycotic_ssl_verify'] = kw.get('thycotic_ssl_verify', False)
            if cred_type == 'ssh':
                kw['thycotic_private_key'] = kw.get(
                    'thycotic_private_key', False)
        elif auth_type == 'kerberos':
            kw['kdc_port'] = kw.get('kdc_port', 88)
            kw['kdc_protocol'] = kw.get('kdc_protocol', 'tcp')

        # If the credential type is ssh, then we'd like to make sure that
        # the escalation is set to "none" unless overridden.
        if (cred_type == 'ssh'
          and auth_type in ['password', 'publicKey', 'certificate']):
            kw['privilege_escalation'] = kw.get('privilege_escalation', 'none')

        if kw.get('db_type') == 'Oracle':
            kw['oracle_auth_type'] = kw.get('oracle_auth_type', 'NORMAL')
            kw['oracle_service_type'] = kw.get('oracle_service_type', 'SID')

        # Uploading files as necessary
        kw = self._upload_files(**kw)

        # Constructing the payload
        payload = self._constructor(**kw)

        # Making the call.
        return self._api.post('credential', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific credential.

        :sc-api:`credential: details <Credential.html#CredentialRESTReference-/credential/{id}>`

        Args:
            id (int): The identifier for the credential.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The credential resource record.

        Examples:
            >>> cred = sc.credentials.details(1)
            >>> pprint(cred)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('credential/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits a credential.

        :sc-api:`credential: edit <Credential.html#credential_id_PATCH>`

        Args:
            auth_type (str, optional):
                The type of authentication for the credential.  Valid types are
                ``beyondtrust``, ``certificate``, cyberark``, ``kerberos``,
                ``lieberman``, ``lm``, ``ntlm``, ``password``, ``publickey``,
                ``thycotic``.
            beyondtrust_api_key (str, optional):
                The API key to use for authenticating to Beyondtrust.
            beyondtrust_duration (int, optional):
                The length of time to cache the checked-out credentials from
                Beyondtrust.  This value should be less than the password change
                interval within Beyondtrust.
            beyondtrust_host (str, optional):
                The host address for the Beyondtrust application.
            beyondtrust_port (int, optional):
                The port number associated with the Beyondtrust application.
            beyondtrust_use_escalation (bool, optional):
                If enabled, informs the scanners to use Beyondtrust for
                privilege escalation.
            beyondtrust_use_private_key (bool, optional):
                If enabled, informs the scanners to use key-based auth for SSH
                connections instead of password auth.
            beyondtrust_use_ssl (bool, optional):
                Should the scanners communicate to Beyondtrust over SSL for
                credential retrieval?  If left unspecified, the default is set
                to ``True``.
            beyondtrust_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                Beyondtrust?  If left unspecified, the default is ``False``.
            community_string (str, optional):
                The SNMP community string to use for authentication.
            db_type (str, optional):
                The type of database connection that will be performed.  Valid
                types are ``DB2``, ``Informix/DRDA``, ``MySQL``, ``Oracle``,
                ``PostgreSQL``, ``SQL Server``.
            description (str, optional):
                A description to associate to the credential.
            domain (str, optional):
                The Active Directory domain to use if the user is a member of a
                domain.
            escalation_path (str, optional):
                The path in which to run the escalation commands.
            escalation_password (str, optional):
                The password to use for the escalation.
            escalation_su_use (str, optional):
                If performing an SU escalation, this is the user to escalate to.
            escalation_username (str, optional):
                The username to escalate to.
            kdc_ip (str, optional):
                The kerberos host supplying the session tickets.
            kdc_port (int, optional):
                The port to use for kerberos connections.  If left unspecified
                the default is ``88``.
            kdc_protocol (str, optional):
                The protocol to use for kerberos connections.  Valid options are
                ``tcp`` and ``udp``.  If left unspecified then the default is
                ``tcp``.
            kdc_realm (str, optional):
                The Kerberos realm to use for authentication.
            lieberman_host (str, optional):
                The address for the Lieberman vault.
            lieberman_port (int, optional):
                The port number where the Lieberman service is listening.
            lieberman_pam_password (str, optional):
                The password to authenticate to the Lieberman RED API.
            lieberman_pam_user (str, optional):
                The username to authenticate to the Lieberman RED API.
            lieberman_system_name (str, optional):
                The name for the credentials in Lieberman.
            lieberman_use_ssl (bool, optional):
                Should the scanners communicate to Lieberman over SSL for
                credential retrieval?  If left unspecified, the default is set
                to ``True``.
            lieberman_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                Lieberman?  If left unspecified, the default is ``False``.
            name (str, optional):
                The name for the credential.
            password (str, optional):
                The password for the credential.
            port (int, optional):
                A valid port number for a database credential.
            privilege_escalation (str, optional):
                The type of privilege escalation to perform once authenticated.
                Valid values are ``.k5login``, ``cisco``, ``dzdo``, ``none``,
                ``pbrun``, ``su``, ``su+sudo``, ``sudo``.  If left unspecified,
                the default is ``none``.
            oracle_auth_type (str, optional):
                The type of authentication to use when communicating to an
                Oracle database server.  Supported values are ``sysdba``,
                ``sysoper``, and ``normal``.  If left unspecified, the default
                option is ``normal``.
            oracle_service_type (str, optional):
                The type of service identifier specified in the ``sid``
                parameter.  Valid values are either ``sid`` or ``service_name``.
                If left unspecified, the default is ``sid``.
            sid (str, optional):
                The service identifier or name for a database credential.
            sql_server_auth_type (str, optional):
                The type of authentication to perform to the SQL Server
                instance.  Valid values are ``SQL`` and ``Windows``.  The default
                value if left unspecified is ``SQL``.
            tags (str, optional):
                A tag to associate to the credential.
            type (str. optional):
                The type of credential to store.  Valid types are ``database``,
                ``snmp``, ``ssh``, and ``windows``.
            username (str, optional):
                The username for the OS credential.
            thycotic_domain (str, optional):
                The domain, if set, within Thycotic.
            thycotic_organization (str, optional):
                The organization to use if using a cloud instance of Thycotic.
            thycotic_password (str, optional):
                The password to use when authenticating to Thycotic.
            thycotic_private_key (bool, optional):
                If enabled, informs the scanners to use key-based auth for SSH
                connections instead of password auth.
            thycotic_secret_name (str, optional):
                The secret name value on the Tycotic server.
            thycotic_url (str, optional):
                The absolute URL path pointing to the Thycotic secret server.
            thycotic_username (str, optional):
                The username to use to authenticate to Thycotic.
            thycotic_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                Thycotic?  If left unspecified, the default is ``False``.
            vault_account_name (str, optional):
                The unique name of the credential to retrieve from CyberArk.
                Generally referred to as the *name* paramater within CyberArk.
            vault_address (str, optional):
                The domain for the CyberArk account.  SSL must be configured
                through IIS on the CCP before using.
            vault_app_id (str, optional):
                The AppID to use with CyberArk.
            vault_cyberark_client_cert (file, optional):
                The fileobject containing the CyberArk client certificate.
            vault_cyberark_url (str, optional):
                The URL for the CyberArk AIM web service. If left unspecified,
                the default URL path of ``/AIMWebservice/v1.1/AIM.asmx`` will be
                used..
            vault_cyberark_private_key (file, optional):
                The fileobject containing the CyberArk client private key.
            vault_cyberark_private_key_passphrase (str, optional):
                The passhrase for the private key.
            vault_folder (str, optional):
                The folder to use within CyberArk for credential retrieval.
            vault_host (str, optional):
                The CyberArk Vault host.
            vault_password (str, optional):
                The password to use for authentication to the vault if
                the CyberArk Central Credential Provider is configured for
                basic auth.
            vault_policy_id (int, optional):
                The CyberArk PolicyID assigned to the credentials to retrieve.
            vault_port (int, optional):
                The port in which the CyberArk Vault resides.
            vault_safe (str, optional):
                The CyberArk safe that contains the credentials to retrive.
            vault_use_ssl (bool, optional):
                Should the scanners communicate to CyberArk over SSL for
                credential retrieval?  If left unspecified, the default is set
                to ``True``.
            vault_username (str, optional):
                The username to use for authentication to the vault if
                the CyberArk Central Credential Provider is configured for
                basic auth.
            vault_verify_ssl (bool, optional):
                Should the SSL certificate be validated when communicating to
                the vault?  If left unspecified, the default is ``False``.

        Returns:
            :obj:`dict`:
                The newly updated credential.

        Examples:
            >>> cred = sc.credentials.edit()
        '''
        # Uploading files as necessary
        kw = self._upload_files(**kw)

        payload = self._constructor(**kw)
        return self._api.patch('credential/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a credential.

        :sc-api:`credential: delete <Credential.html#credential_id_DELETE>`

        Args:
            id (int): The numeric identifier for the credential to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.credentials.delete(1)
        '''
        return self._api.delete('credential/{}'.format(
            self._check('id', id, int))).json()['response']

    def list(self, fields=None):
        '''
        Retrieves the list of scan zone definitions.

        + :sc-api:`credential: list <Credential.html#CredentialRESTReference-/credential>`

        Args:
            fields (list, optional):
                A list of attributes to return for each credential.

        Returns:
            :obj:`list`:
                A list of credential resources.

        Examples:
            >>> for cred in sc.credentials.list():
            ...     pprint(cred)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('credential', params=params).json()['response']

    def tags(self):
        '''
        Retrieves the list of unique tags associated to credentials.

        :sc-api:`credential: tags <Credential.html#CredentialRESTReference-/credential/tag>`

        Returns:
            :obj:`list`:
                List of tags

        Examples:
            >>> tags = sc.credentials.tags()
        '''
        return self._api.get('credential/tag').json()['response']

    def share(self, id, *groups):
        '''
        Shares the specified credential to another user group.

        :sc-api:`credential: share <Credential.html#CredentialRESTReference-/credential/{id}/share>`

        Args:
            id (int): The numeric id for the credential.
            *groups (int): The numeric id of the group(s) to share to.

        Returns:
            :obj:`dict`:
                The updated credential resource.

        Examples:
            >>> sc.credentials.share(1, group_1, group_2)
        '''
        return self._api.post('credential/{}/share'.format(
            self._check('id', id, int)), json={
                'groups': [{'id': self._check('group:id', i, int)}
                    for i in groups]}).json()['response']
