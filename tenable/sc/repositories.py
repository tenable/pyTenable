'''
Repositories
============

The following methods allow for interaction with the Tenable Security Center
:sc-api:`Repository <Repository.htm>` API.  These items are typically seen
under the **Repositories** section of Tenable Security Center.

Methods available on ``sc.repositories``:

.. rst-class:: hide-signature
.. autoclass:: RepositoryAPI
    :members:
'''
from semver import VersionInfo
from .base import SCEndpoint


class RepositoryAPI(SCEndpoint):
    def _constructor(self, **kwargs):
        '''
        Repository document constructor
        '''
        if 'nessus_sched' in kwargs:
            kwargs['nessusSchedule'] = self._schedule_constructor(kwargs['nessus_sched'])
            del kwargs['nessus_sched']
        if 'mobile_sched' in kwargs:
            kwargs['mobileSchedule'] = self._schedule_constructor(kwargs['mobile_sched'])
            del kwargs['mobile_sched']
        if 'remote_sched' in kwargs:
            kwargs['remoteSchedule'] = self._schedule_constructor(kwargs['remote_sched'])
            del kwargs['remote_sched']

        if 'name' in kwargs:
            # Validate the name is a string
            self._check('name', kwargs['name'], str)

        if 'description' in kwargs:
            # Verify that the description is a string
            self._check('description', kwargs['description'], str)

        if 'format' in kwargs:
            # The data format for the repository.
            kwargs['dataFormat'] = self._check('format', kwargs['format'], str,
                                               choices=['agent', 'IPv4', 'IPv6', 'mobile'])
            del kwargs['format']

        if 'repo_type' in kwargs:
            # The type of repository
            kwargs['type'] = self._check('repo_type', kwargs['repo_type'], str,
                                         choices=['Local', 'Remote', 'Offline'])
            del kwargs['repo_type']

        if 'orgs' in kwargs:
            # Validate all of the organizational sub-documents.
            kwargs['organizations'] = [{'id': self._check('org_id', o, int)}
                                       for o in self._check('orgs', kwargs['orgs'], list)]
            del kwargs['orgs']

        if 'trending' in kwargs:
            # Trending should be between 0 and 365.
            kwargs['trendingDays'] = self._check('trending', kwargs['trending'], int,
                                                 choices=list(range(366)))
            del kwargs['trending']

        if 'fulltext_search' in kwargs:
            # trendWithRaw is the backend paramater name for "Full Text Search"
            # within the UI.  We will be calling it fulltest_search to more
            # closely align with what the frontend calls this feature.
            kwargs['trendWithRaw'] = str(self._check('fulltext_search',
                                                     kwargs['fulltext_search'], bool)).lower()
            del kwargs['fulltext_search']

        if 'lce_correlation' in kwargs:
            # The correlation parameter isn't well named here, we will call it
            # out as LCE correlation to specifically note what it is for.
            kwargs['correlation'] = [{'id': self._check('lce_id', l, int)}
                                     for l in self._check('lce_correlation', kwargs['lce_correlation'], list)]
            del kwargs['lce_correlation']

        if 'allowed_ips' in kwargs:
            # Using valid IPs here instead of ipRange to again more closely
            # align to the frontend and to more explicitly call out the
            # function of this paramater
            kwargs['ipRange'] = ','.join([self._check('ip', i, str)
                                          for i in self._check('allowed_ips', kwargs['allowed_ips'], list)])
            del kwargs['allowed_ips']

        if 'remote_ip' in kwargs:
            kwargs['remoteIP'] = self._check('remote_ip', kwargs['remote_ip'], str)
            del kwargs['remote_ip']

        if 'remote_repo' in kwargs:
            kwargs['remoteID'] = self._check('remote_repo', kwargs['remote_repo'], int)
            del kwargs['remote_repo']

        if 'preferences' in kwargs:
            # Validate that all of the preferences are K:V pairs of strings.
            for key in self._check('preferences', kwargs['preferences'], dict):
                self._check('preference:{}'.format(key), key, str)
                self._check('preference:{}:value'.format(key),
                            kwargs['preferences'][key], str)

        if 'mdm_id' in kwargs:
            kwargs['mdm'] = {'id': self._check('mdm_id', kwargs['mdm_id'], int)}
            del kwargs['mdm_id']

        if 'scanner_id' in kwargs:
            kwargs['scanner'] = {'id': self._check(
                'scanner_id', kwargs['scanner_id'], int)}
            del kwargs['scanner_id']

        return kwargs

    def _rules_constructor(self, **kwargs):
        '''
        Accept/Recast Rule Query Creator
        '''
        if 'plugin_id' in kwargs:
            # Convert the snake_cased variant to the camelCased variant.
            kwargs['pluginID'] = self._check('plugin_id', kwargs['plugin_id'], int)
            del kwargs['plugin_id']
        if 'port' in kwargs:
            # validate port is a integer
            self._check('port', kwargs['port'], int)
        if 'orgs' in kwargs:
            # convert the list of organization IDs into the comma-separated
            # string that the API expects.
            kwargs['organizationIDs'] = ','.join([str(self._check('org:id', o, int))
                                              for o in self._check('orgs', kwargs['orgs'], list)])
            del kwargs['orgs']
        if 'fields' in kwargs:
            # convert the list of field names into the comma-separated string
            # that the API expects.
            kwargs['fields'] = ','.join([self._check('field', f, str)
                                     for f in kwargs['fields']])
        return kwargs

    def list(self, fields=None, repo_type=None):
        '''
        Retrieves a list of repositories.

        :sc-api:`repository: list <Repository.htm#repository_GET>`

        Args:
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the repository list API doc.
            repo_type (str, optional):
                Restrict the response to a specific type of repository.  If not
                set, then all repository types will be returned.  Allowed types
                are ``All``, ``Local``, ``Remote``, and ``Offline``.

        Returns:
            :obj:`list`:
                List of repository definitions.

        Examples:
            Retrieve all of all of the repositories:

            >>> repos = sc.repositories.list()

            Retrieve all of the remote repositories:

            >>> repos = sc.repositories.list(repo_type='Remote')
        '''
        params = dict()
        if repo_type:
            params['type'] = self._check('repo_type', repo_type, str, choices=[
                'All', 'Local', 'Remote', 'Offline'])
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                                         for f in fields])
        return self._api.get('repository', params=params).json()['response']

    def create(self, **kwargs):
        '''
        Creates a new repository

        :sc-api:`repository: create <Repository.htm#repository_POST>`

        Args:
            name (str): The name for the respository.
            allowed_ips (list, optional):
                Allowed IPs will restrict incoming data being inserted into the
                repository to only the IPs that exist within the configured
                CIDR ranges.  Accepts a list of CIDR strings based on the
                repository format (IPv4 or IPv6).  If left unspecified, then it
                will default to the CIDR equivalent of "allow all" for that IP
                version.  IPv4=0.0.0.0/0, IPv6=::/0.
            description (str, optional):
                A description for the repository.
            format (str, optional):
                The format of the repository.  Valid choices are ``agent``,
                ``IPv4``, ``IPv6``, and ``mobile``.  The default if unspecified
                is ``IPv4``.
            fulltext_search (bool, optional):
                Should full-text searching be enabled?  This option is used for
                IPv4, IPv6, and agent repository formats and determins whether
                the plugin output is trended along with the normalized data.  If
                left unspecified, the default is set to ``False``.
            lce_correlation (list, optional):
                What Log Correlation Engines (if any) should correlate against
                this repository.  A list of configured LCE numeric IDs is
                supplied.  This option is used on IPv4, IPv6, and agent formats
                and is defaulted to nothing if left unspecified.
            nessus_sched (dict, optional):
                This is the .Nessus file generation schedule for IPv4 and IPv6
                repository formats.  This option should only be used if there
                is a need to consume the Repository in a raw Nessus XML format.
                If left unspecified, it will default to ``{'type': 'never'}``.
            mobile_sched (dict, optional):
                When using the mobile repository format, this option will inform
                Tenable Security Center how often to perform the MDM synchronization into the
                repository.  If left unspecified, it will default to
                ``{'type': 'never'}``.
            orgs (list, optional):
                A list of Organization IDs used to assign the repository to 1 or
                many organizations.
            preferences (dict, optional):
                When using a mobile repository type, this dictionary details
                the required preferences to inject into the backend scan needed
                to communicate to the MDM solution.
            remote_ip (str, optional):
                When the Remote repository type is used, this is the IP
                address of the Tenable Security Center instance that the repository will be
                pulled from.
            remote_repo (int, optional):
                When the Remote repository type is used, this is the numeric ID
                of the repository on the remote host that will be pulled.
            remote_sched (dict, optional):
                When the Remote repository type is used, this is the schedule
                dictionary that will inform Tenable Security Center how often to synchronize
                with the downstream Tenable Security Center instance.  If left unspecified
                then we will default to ``{'type': 'never'}``.
            repo_type (str, optional):
                What type of repository is this?  Valid choices are ``Local``,
                ``Remote``, and ``Offline``.  The default if unspecified is
                ``Local``.
            scanner_id (int, optional):
                When using the mobile repository format, we must specify the
                scanner from which to query the MDM source.
            trending (int, optional):
                How many days of trending snapshots should be created for this
                repository.  This value is only used for IPv4, IPv6, and agent
                repositories.  If not supplied, the default will be 0.

        Returns:
            :obj:`dict`:
                The repository resource record for the newly created Repo.

        Examples:
            Creating a new IPv4 Repository leveraging the defaults:

            >>> repo = sc.repositories.create(name='Example IPv4')

            Creating a new IPv4 Repository with 90 days of trending and linked
            to the first Organization:

            >>> repo = sc.repositories.create(
            ...     name='Example Trending', trending=90, orgs=[1])

            Creating an IPv6 repository:

            >>> repo = sc.repositories.create(
            ...     name='Example IPv6', format='IPv6')

            Creating an agent repository:

            >>> repo = sc.repositories.create(
            ...     name='Example Agent', format='agent')

            Creating an MDM repository for ActiveSync that will sync every day
            at 6am eastern:

            >>> repo = sc.repositories.create(
            ...     name='Example ActiveSync', mdm_id=1, scanner_id=1,
            ...     format='mobile', orgs=[1],
            ...     mobile_sched={
            ...         'repeatRule': 'FREQ=DAILY;INTERVAL=1',
            ...         'start': 'TZID=America/New_York:20190212T060000',
            ...         'type': 'ical',
            ...     },
            ...     preferences={
            ...         'domain': 'AD_DOMAIN',
            ...         'domain_admin': 'DA_ACCOUNT_NAME',
            ...         'domain_controller': 'dc1.company.tld',
            ...         'password': 'DA_ACCOUNT_PASSWORD'
            ... })

            Creating a new repository to remotely sync the downstream Tenable Security Center
            instance's repository 1 to this host and institute trending for 90
            days:

            >>> repo = sc.repositories.create(
            ...     name='Example Remote Repo',
            ...     repo_type='Remote',
            ...     remote_ip='192.168.0.101',
            ...     remote_repo=1,
            ...     trending=90,
            ...     orgs=[1],
            ...     remote_sched={
            ...         'type': 'ical',
            ...         'start': 'TZID=America/NewYork:20190212T060000',
            ...         'repeatRule': 'FREQ=DAILY;INTERVAL=1'
            ... })
        '''
        kwargs = self._constructor(**kwargs)
        kwargs['dataFormat'] = kwargs.get('dataFormat', 'IPv4')
        kwargs['type'] = kwargs.get('type', 'Local')

        if kwargs['dataFormat'] in ['IPv4', 'IPv6', 'agent']:
            kwargs['trendingDays'] = kwargs.get('trendingDays', 0)
            kwargs['trendWithRaw'] = kwargs.get('trendWithRaw', 'false')

        if kwargs['dataFormat'] in ['IPv4', 'IPv6']:
            kwargs['nessusSchedule'] = kwargs.get('nessusSchedule', {'type': 'never'})

        if kwargs['dataFormat'] == 'IPv4':
            kwargs['ipRange'] = kwargs.get('ipRange', '0.0.0.0/0')

        if kwargs['dataFormat'] == 'IPv6':
            kwargs['ipRange'] = kwargs.get('ipRange', '::/0')

        if kwargs['dataFormat'] == 'mobile':
            kwargs['mobileSchedule'] = kwargs.get('mobileSchedule', {'type': 'never'})

        if kwargs['type'] == 'remote':
            kwargs['remoteSchedule'] = kwargs.get('remoteSchedule', {'type': 'never'})

        return self._api.post('repository', json=kwargs).json()['response']

    def details(self, repository_id, fields=None):
        '''
        Retrieves the details for the specified repository.

        :sc-api:`repository: details <Repository.htm#repository_id_GET>`

        Args:
            repository_id (int): The numeric id of the repository.
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the repository details API doc.

        Returns:
            :obj:`dict`:
                The repository resource record.

        Examples:
            >>> repo = sc.repositories.details(1)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('repository/{}'.format(
            self._check('repository_id', repository_id, int)), params=params).json()['response']

    def delete(self, repository_id):
        '''
        Remove the specified repository from Tenable Security Center

        :sc-api:`repository: delete <Repository.htm#repository_uuid_DELETE>`

        Args:
            repository_id (int): The numeric id of the repository to delete.

        Returns:
            :obj:`str`:
                Empty response string

        Examples:
            >>> sc.repositories.delete(1)
        '''
        return self._api.delete('repository/{}'.format(
            self._check('repository_id', repository_id, int))).json()['response']

    def edit(self, repository_id, **kwargs):
        '''
        Updates an existing repository

        :sc-api:`repository: edit <Repository.htm#repository_uuid_PATCH>`

        Args:
            repository_id (int): The numeric id of the repository to edit.
            allowed_ips (list, optional):
                Allowed IPs will restrict incoming data being inserted into the
                repository to only the IPs that exist within the configured
                CIDR ranges.  Accepts a list of CIDR strings based on the
                repository format (IPv4 or IPv6).
            description (str, optional):
                A description for the repository.
            lce_correlation (list, optional):
                What Log Correlation Engines (if any) should correlate against
                this repository.  A list of configured LCE numeric IDs is
                supplied.  This option is used on IPv4, IPv6, and agent formats.
            name (str, optional): The name for the repository.
            nessus_sched (dict, optional):
                This is the .Nessus file generation schedule for IPv4 and IPv6
                repository formats.  This option should only be used if there
                is a need to consume the Repository in a raw Nessus XML format.
            mobile_sched (dict, optional):
                When using the mobile repository format, this option will inform
                Tenable Security Center how often to perform the MDM synchronization into the
                repository.
            orgs (list, optional):
                A list of Organization IDs used to assign the repository to 1 or
                many organizations.
            preferences (dict, optional):
                When using a mobile repository type, this dictionary details
                the required preferences to inject into the backend scan needed
                to communicate to the MDM solution.
            remote_ip (str, optional):
                When the Remote repository type is used, this is the IP
                address of the Tenable Security Center instance that the repository will be
                pulled from.
            remote_repo (int, optional):
                When the Remote repository type is used, this is the numeric ID
                of the repository on the remote host that will be pulled.
            remote_sched (dict, optional):
                When the Remote repository type is used, this is the schedule
                dictionary that will inform Tenable Security Center how often to synchronize
                with the downstream Tenable Security Center instance.
            scanner_id (int, optional):
                When using the mobile repository format, we must specify the
                scanner from which to query the MDM source.
            trending (int, optional):
                How many days of trending snapshots should be created for this
                repository.  This value is only used for IPv4, IPv6, and agent
                repositories.

        Returns:
            :obj:`dict`:
                The repository resource record for the newly created Repo.

        Examples:
            >>> repo = sc.repositories.edit(1, name='Example IPv4')
        '''
        kwargs = self._constructor(**kwargs)
        return self._api.patch('repository/{}'.format(
            self._check('repository_id', repository_id, int)), json=kwargs).json()['response']

    def accept_risk_rules(self, repository_id, **kwargs):
        '''
        Retrieves the accepted risk rules associated with the specified
        repository.

        :sc-api:`repository: accept rules <Repository.htm#RepositoryRESTReference-/repository/{id}/acceptRiskRule>`

        Args:
            repository_id (int): The numeric id of the repository.
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the repository accept risk rules API doc.

        Returns:
            :obj:`list`:
                List of the accepted risk rules that apply to the repo.

        Examples:
            >>> rules = sc.repositories.accept_risk_rules(1)
        '''
        params = self._rules_constructor(**kwargs)
        return self._api.get('repository/{}/acceptRiskRule'.format(
            self._check('repository_id', repository_id, int)), params=params).json()['response']

    def recast_risk_rules(self, repository_id, **kwargs):
        '''
        Retrieves the recast risk rules associated with the specified
        repository.

        :sc-api:`repository: recast rules
        <Repository.htm#repository_uuid_recastRiskRule_GET>`

        Args:
            repository_id (int): The numeric id of the repository.
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the repository recast risk rules API doc.

        Returns:
            :obj:`list`:
                List of the recast risk rules that apply to the repo.

        Examples:
            >>> rules = sc.repositories.recast_risk_rules(1)
        '''
        params = self._rules_constructor(**kwargs)
        return self._api.get('repository/{}/recastRiskRule'.format(
            self._check('repository_id', repository_id, int)), params=params).json()['response']

    def asset_intersections(self, repository_id, uuid=None, ip_address=None, dns=None):
        '''
        Retrieves the asset lists that a UUID, DNS address, or IP exists in.

        :sc-api:`repository: asst intersections
        <Repository.htm#repository_uuid_assetIntersections_GET>`

        Args:
            repository_id (int): The numeric identifier of the repository to query.
            dns (str): The DNS name to query
            ip_address (str): The IP address to query
            uuid (str): The UUID to query.

        Returns:
            :obj:`list`:
                The list of assets matching the criteria.

        Examples:
            >>> assetlists = sc.repositories.asset_intersection(1,
            ...     ip='192.168.0.1')
        '''
        params = dict()
        if dns:
            params['dnsName'] = self._check('dns', dns, str)
        if ip_address:
            params['ip'] = self._check('ip_address', ip_address, str)
        if uuid:
            params['uuid'] = self._check('uuid', uuid, 'uuid')
        return self._api.get('repository/{}/assetIntersections'.format(
            self._check('repository_id', repository_id, int)),
            params=params).json()['response'].get('assets')

    def import_repository(self, repository_id, fobj):
        '''
        Imports the repository archive for an offline repository.

        :sc-api:`repository: import <Repository.htm#repository_uuid_import_POST>`

        Args:
            repository_id (int): The numeric id associated to the offline repository.
            fobj (FileObject):
                The file-like object containing the repository archive.

        Returns:
            :obj:`dict`:
                The import response record.

        Example:
            >>> with open('repo.tar.gz', 'rb') as archive:
            ...     sc.repositories.import_repository(1, archive)
        '''
        return self._api.post('repository/{}/import'.format(
            self._check('repository_id', repository_id, int)), json={
            'file': self._api.files.upload(fobj)
        }).json()['response']

    def export_repository(self, repository_id, fobj):
        '''
        Exports the repository and writes the archive tarball into the file
        object passed.

        :sc-api:`repository: export <Repository.htm#repository_uuid_export_GET>`

        Args:
            repository_id (int): The numeric id associated to the repository.
            fobj (FileObject):
                The file-like object for the repository archive.

        Returns:
            :obj:`dict`:
                The export response record.

        Example:
            >>> with open('repo.tar.gz', 'wb') as archive:
            ...     sc.repositories.export_repository(1, archive)
        '''
        resp = self._api.get('repository/{}/export'.format(
            self._check('repository_id', repository_id, int)), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()
        return fobj

    def remote_sync(self, repository_id):
        '''
        Initiates a remote synchronization with a downstream Tenable Security Center
        instance.  This action can only be performed on an offline repository.

        :sc-api:`repository: sync <Repository.htm#repository_uuid_sync_POST>`

        Args:
            repository_id (int): The numeric id for the remote repository.

        Returns:
            :obj:`dict`:
                The sync response record.

        Examples:
            >>> sc.repositories.remote_sync(1)
        '''
        return self._api.post('repository/{}/sync'.format(
            self._check('repository_id', repository_id, int)), json={}).json()['response']

    def mobile_sync(self, repository_id):
        '''
        Initiates a MDM synchronization with the configured MDM source on the
        mobile repository specified.

        :sc-api:`repository: update mobile data
        <Repository.htm#repository_uuid_updateMobileData_POST>`

        Args:
            repository_id (int): The numeric id for the mobile repository to run the sync.

        Returns:
            :obj:`dict`:
                The sync response record.

        Examples:
            >>> sc.repositories.mobile_sync(1)
        '''
        return self._api.post('repository/{}/updateMobileData'.format(
            self._check('repository_id', repository_id, int)), json={}).json()['response']

    def device_info(self, repository_id, dns=None, ip_address=None, uuid=None, fields=None):
        '''
        Retrieves the device information for the requested device on the
        associated repository.

        :sc-api:`repository: device info
        <Repository.htm#repository_uuid_deviceInfo_GET>`

        :sc-api:`repository: ip info <Repository.htm#RepositoryRESTReference-/repository/{id}/ipInfo>`

        Args:
            repository_id (int): The numeric id for the repository to query.
            dns (str): The DNS name to query
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the repository device info API doc.
            ip_address (str): The IP address to query
            uuid (str): The UUID to query.

        Returns:
            :obj:`dict`:
                The device resource.

        Examples:
            >>> host = sc.repositories.device_info(1, ip_address='192.168.0.1')
        '''
        # We will generally want to query the deviceInfo action, however if we
        # happen to be on a Tenable Security Center instance version that's less than 5.7, we
        # have to instead query ipInfo.
        method = 'deviceInfo'
        if VersionInfo.parse(self._api.version).match('<5.7.0'):
            method = 'ipInfo'

        params = dict()
        if fields:
            params['fields'] = ','.join(
                [self._check('field', f, str) for f in fields]
            )
        if dns:
            params['dnsName'] = self._check('dns', dns, str)
        if ip_address:
            params['ip'] = self._check('ip_address', ip_address, str)
        if uuid:
            params['uuid'] = self._check('uuid', uuid, 'uuid')

        self._check('repository_id', repository_id, int)
        return self._api.get(f'repository/{repository_id}/{method}',
                             params=params
                             ).json()['response']

    def remote_authorize(self, host, username, password):
        '''
        Authorized communication to a downstream Tenable Security Center instance with the
        provided username and password.

        :sc-api:`repository: authorize <Repository.htm#RepositoryRESTReference-/repository/authorize>`

        Args:
            host (str): The downstream Tenable Security Center instance ip address.
            username (str): The username to authenticate with.
            password (str); The password to authenticate with.

        Returns:
            :obj:`str`:
                Empty response object

        Examples:
            >>> sc.repositories.remote_authorize(
            ...     '192.168.0.101', 'admin', 'password')
        '''
        return self._api.post('repository/authorize', json={
            'host': self._check('host', host, str),
            'username': self._check('username', username, str),
            'password': self._check('password', password, str)
        }).json()['response']

    def remote_fetch(self, host):
        '''
        Retrieves the list of repositories from the specified downstream
        Tenable Security Center instance.

        :sc-api:`repository: fetch remote <Repository.htm#RepositoryRESTReference-/repository/fetchRemote>`

        Args:
            host (str): The downstream Tenable Security Center instance ip address.

        Returns:
            :obj:`list`:
                The list of repositories on the downstream Tenable Security Center instance.
        '''
        return self._api.get('repository/fetchRemote', params={
            'host': self._check('host', host, str)}).json()['response']
