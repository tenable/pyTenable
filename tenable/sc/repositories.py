'''
repositories
============

The following methods allow for interaction with the Tenable.sc
:sc-api:`Repository <Repository.html>` API.  These items are typically seen
under the **Repositories** section of Tenable.sc.

Methods available on ``sc.repositories``:

.. rst-class:: hide-signature
.. autoclass:: RepositoryAPI

    .. automethod:: accept_risk_rules
    .. automethod:: asset_intersections
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: device_info
    .. automethod:: edit
    .. automethod:: export_repository
    .. automethod:: import_repository
    .. automethod:: recast_risk_rules
    .. automethod:: remote_authorize
    .. automethod:: remote_fetch
    .. automethod:: remote_sync
'''
from .base import SCEndpoint
from tenable.utils import dict_merge, policy_settings
from io import BytesIO
import json, semver

class RepositoryAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Repository document constructor
        '''
        if 'nessus_sched' in kw:
            kw['nessusSchedule'] = self._schedule_constructor(kw['nessus_sched'])
            del(kw['nessus_sched'])
        if 'mobile_sched' in kw:
            kw['mobileSchedule'] = self._schedule_constructor(kw['mobile_sched'])
            del(kw['mobile_sched'])
        if 'remote_sched' in kw:
            kw['remoteSchedule'] = self._schedule_constructor(kw['remote_sched'])
            del(kw['remote_sched'])

        if 'name' in kw:
            # Validate the name is a string
            self._check('name', kw['name'], str)

        if 'description' in kw:
            # Verify that the description is a string
            self._check('description', kw['description'], str)

        if 'format' in kw:
            # The data format for the repository.
            kw['dataFormat'] = self._check('format', kw['format'], str,
                choices=['agent', 'IPv4', 'IPv6', 'mobile'])
            del(kw['format'])

        if 'repo_type' in kw:
            # The type of repository
            kw['type'] = self._check('repo_type', kw['repo_type'], str,
                choices=['Local', 'Remote', 'Offline'])
            del(kw['repo_type'])

        if 'orgs' in kw:
            # Validate all of the organizational sub-documents.
            kw['organizations'] = [{'id': self._check('org_id', o, int)}
                for o in self._check('orgs', kw['orgs'], list)]
            del(kw['orgs'])

        if 'trending' in kw:
            # Trending should be between 0 and 365.
            kw['trendingDays'] = self._check('trending', kw['trending'], int,
                choices=list(range(366)))
            del(kw['trending'])

        if 'fulltext_search' in kw:
            # trendWithRaw is the backend paramater name for "Full Text Search"
            # within the UI.  We will be calling it fulltest_search to more
            # closely align with what the frontend calls this feature.
            kw['trendWithRaw'] = str(self._check('fulltext_search',
                kw['fulltext_search'], bool)).lower()
            del(kw['fulltext_search'])

        if 'lce_correlation' in kw:
            # The correlation parameter isn't well named here, we will call it
            # out as LCE correlation to specifically note what it is for.
            kw['correlation'] = [{'id': self._check('lce_id', l, int)}
                for l in self._check('lce_correlation', kw['lce_correlation'], list)]
            del(kw['lce_correlation'])

        if 'allowed_ips' in kw:
            # Using valid IPs here instead of ipRange to again more closely
            # align to the frontend and to more explicitly call out the
            # function of this paramater
            kw['ipRange'] = ','.join([self._check('ip', i, str)
                for i in self._check('allowed_ips', kw['allowed_ips'], list)])
            del(kw['allowed_ips'])

        if 'remote_ip' in kw:
            kw['remoteIP'] = self._check('remote_ip', kw['remote_ip'], str)
            del(kw['remote_ip'])

        if 'remote_repo' in kw:
            kw['remoteID'] = self._check('remote_repo', kw['remote_repo'], int)
            del(kw['remote_repo'])

        if 'preferences' in kw:
            # Validate that all of the preferences are K:V pairs of strings.
            for key in self._check('preferences', kw['preferences'], dict):
                self._check('preference:{}'.format(key), key, str)
                self._check('preference:{}:value'.format(key),
                    kw['preferences'][key], str)

        if 'mdm_id' in kw:
            kw['mdm'] = {'id': self._check('mdm_id', kw['mdm_id'], int)}
            del(kw['mdm_id'])

        if 'scanner_id' in kw:
            kw['scanner'] = {'id': self._check(
                'scanner_id', kw['scanner_id'], int)}
            del(kw['scanner_id'])

        return kw

    def _rules_constructor(self, **kw):
        '''
        Accept/Recast Rule Query Creator
        '''
        if 'plugin_id' in kw:
            # Convert the snake_cased variant to the camelCased variant.
            kw['pluginID'] = self._check('plugin_id', kw['plugin_id'], int)
            del(kw['plugin_id'])
        if 'port' in kw:
            # validate port is a integer
            self._check('port', kw['port'], int)
        if 'orgs' in kw:
            # convert the list of organization IDs into the comma-separated
            # string that the API expects.
            kw['organizationIDs'] = ','.join([str(self._check('org:id', o, int))
                for o in self._check('orgs', kw['orgs'], list)])
            del(kw['orgs'])
        if 'fields' in kw:
            # convert the list of field names into the comma-separated string
            # that the API expects.
            kw['fields'] = ','.join([self._check('field', f, str)
                for f in kw['fields']])
        return kw

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

    def create(self, **kw):
        '''
        Creates a new repository

        :sc-api:`repository: create <Repository.html#repository_POST>`

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
                For more information refer to `Schedule Dictionaries`_
            mobile_sched (dict, optional):
                When using the mobile repository format, this option will inform
                Tenable.sc how often to perform the MDM synchronization into the
                repository.  If left unspecified, it will default to
                ``{'type': 'never'}``.  For more information refer to
                `Schedule Dictionaries`_
            orgs (list, optional):
                A list of Organization IDs used to assign the repository to 1 or
                many organizations.
            preferences (dict, optional):
                When using a mobile repository type, this dictionary details
                the required preferences to inject into the backend scan needed
                to communicate to the MDM solution.
            remote_ip (str, optional):
                When the Remote repository type is used, this is the IP
                address of the Tenable.sc instance that the repository will be
                pulled from.
            remote_repo (int, optional):
                When the Remote repository type is used, this is the numeric ID
                of the repository on the remote host that will be pulled.
            remote_sched (dict, optional):
                When the Remote repository type is used, this is the schedule
                dictionary that will inform Tenable.sc how often to synchronize
                with the downstream Tenable.sc instance.  If left unspecified
                then we will default to ``{'type': 'never'}``.  For more
                information refer to `Schedule Dictionaries`_
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

            Creating a new repository to remotely sync the downstream Tenable.sc
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
        kw = self._constructor(**kw)
        kw['dataFormat'] = kw.get('dataFormat', 'IPv4')
        kw['type'] = kw.get('type', 'Local')

        if kw['dataFormat'] in ['IPv4', 'IPv6', 'agent']:
            kw['trendingDays'] = kw.get('trendingDays', 0)
            kw['trendWithRaw'] = kw.get('trendWithRaw', 'false')

        if kw['dataFormat'] in ['IPv4', 'IPv6']:
            kw['nessusSchedule'] = kw.get('nessusSchedule', {'type': 'never'})

        if kw['dataFormat'] == 'IPv4':
            kw['ipRange'] = kw.get('ipRange', '0.0.0.0/0')

        if kw['dataFormat'] == 'IPv6':
            kw['ipRange'] = kw.get('ipRange', '::/0')

        if kw['dataFormat'] == 'mobile':
            kw['mobileSchedule'] = kw.get('mobileSchedule', {'type': 'never'})

        if kw['type'] == 'remote':
            kw['remoteSchedule'] = kw.get('remoteSchedule', {'type': 'never'})

        return self._api.post('repository', json=kw).json()['response']

    def details(self, id, fields=None):
        '''
        Retrieves the details for the specified repository.

        :sc-api:`repository: details <Repository.html#repository_id_GET>`

        Args:
            id (int): The numeric id of the repository.
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
            self._check('id', id, int)), params=params).json()['response']

    def delete(self, id):
        '''
        Remove the specified repository from Tenable.sc

        :sc-api:`repository: delete <Repository.html#repository_id_DELETE>`

        Args:
            id (int): The numeric id of the repository to delete.

        Returns:
            :obj:`str`:
                Empty response string

        Examples:
            >>> sc.repositories.delete(1)
        '''
        return self._api.delete('repository/{}'.format(
            self._check('id', id, int))).json()['response']

    def edit(self, id, **kw):
        '''
        Updates an existing repository

        :sc-api:`repository: edit <Repository.html#repository_id_PATCH>`

        Args:
            id (int): The numeric id of the repository to edit.
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
                For more information refer to `Schedule Dictionaries`_
            mobile_sched (dict, optional):
                When using the mobile repository format, this option will inform
                Tenable.sc how often to perform the MDM synchronization into the
                repository.  For more information refer to
                `Schedule Dictionaries`_
            orgs (list, optional):
                A list of Organization IDs used to assign the repository to 1 or
                many organizations.
            preferences (dict, optional):
                When using a mobile repository type, this dictionary details
                the required preferences to inject into the backend scan needed
                to communicate to the MDM solution.
            remote_ip (str, optional):
                When the Remote repository type is used, this is the IP
                address of the Tenable.sc instance that the repository will be
                pulled from.
            remote_repo (int, optional):
                When the Remote repository type is used, this is the numeric ID
                of the repository on the remote host that will be pulled.
            remote_sched (dict, optional):
                When the Remote repository type is used, this is the schedule
                dictionary that will inform Tenable.sc how often to synchronize
                with the downstream Tenable.sc instance.  For more
                information refer to `Schedule Dictionaries`_
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
        kw = self._constructor(**kw)
        return self._api.patch('repository/{}'.format(
            self._check('id', id, int)), json=kw).json()['response']

    def accept_risk_rules(self, id, **kw):
        '''
        Retrieves the accepted risk rules associated with the specified
        repository.

        :sc-api:`repository: accept rules <Repository.html#RepositoryRESTReference-/repository/{id}/acceptRiskRule>`

        Args:
            id (int): The numeric id of the repository.
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
        params = self._rules_constructor(**kw)
        return self._api.get('repository/{}/acceptRiskRule'.format(
            self._check('id', id, int)), params=params).json()['response']

    def recast_risk_rules(self, id, **kw):
        '''
        Retrieves the recast risk rules associated with the specified
        repository.

        :sc-api:`repository: recast rules <Repository.html#RepositoryRESTReference-/repository/{id}/recastRiskRule>`

        Args:
            id (int): The numeric id of the repository.
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
        params = self._rules_constructor(**kw)
        return self._api.get('repository/{}/recastRiskRule'.format(
            self._check('id', id, int)), params=params).json()['response']

    def asset_intersections(self, id, uuid=None, ip=None, dns=None):
        '''
        Retrieves the asset lists that a UUID, DNS address, or IP exists in.

        :sc-api:`repository: asst intersections <Repository.html#RepositoryRESTReference-/repository/{id}/assetIntersections>`

        Args:
            id (int): The numeric identifier of the repository to query.
            dns (str): The DNS name to query
            ip (str): The IP address to query
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
        if ip:
            params['ip'] = self._check('ip', ip, str)
        if uuid:
            params['uuid'] = self._check('uuid', uuid, 'uuid')
        return self._api.get('repository/{}/assetIntersections'.format(
            self._check('id', id, int)),
            params=params).json()['response'].get('assets')

    def import_repository(self, id, fobj):
        '''
        Imports the repository archive for an offline repository.

        :sc-api:`repository: import <Repository.html#RepositoryRESTReference-/repository/{id}/import>`

        Args:
            id (int): The numeric id associated to the offline repository.
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
            self._check('id', id, int)), json={
                'file': self._api.files.upload(fobj)
            }).json()['response']

    def export_repository(self, id, fobj):
        '''
        Exports the repository and writes the archive tarball into the file
        object passed.

        :sc-api:`repository: export <Repository.html#RepositoryRESTReference-/repository/{id}/export>`

        Args:
            id (int): The numeric id associated to the repository.
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
            self._check('id', id, int)), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()
        return fobj

    def remote_sync(self, id):
        '''
        Initiates a remote synchronization with a downstream Tenable.sc
        instance.  This action can only be performed on an offline repository.

        :sc-api:`repository: sync <Repository.html#RepositoryRESTReference-/repository/{id}/sync>`

        Args:
            id (int): The numeric id for the remote repository.

        Returns:
            :obj:`dict`:
                The sync response record.

        Examples:
            >>> sc.repositories.remote_sync(1)
        '''
        return self._api.post('repository/{}/sync'.format(
            self._check('id', id, int)), json={}).json()['response']

    def mobile_sync(self, id):
        '''
        Initiates a MDM synchronization with the configured MDM source on the
        mobile repository specified.

        :sc-api:`repository: update mobile data <Repository.html#RepositoryRESTReference-/repository/{id}/updateMobileData>`

        Args:
            id (int): The numeric id for the mobile repository to run the sync.

        Returns:
            :obj:`dict`:
                The sync response record.

        Examples:
            >>> sc.repositories.mobile_sync(1)
        '''
        return self._api.post('repository/{}/updateMobileData'.format(
            self._check('id', id, int)), json={}).json()['response']

    def device_info(self, id, dns=None, ip=None, uuid=None, fields=None):
        '''
        Retrieves the device information for the requested device on the
        associated repository.

        :sc-api:`repository: device info <Repository.html#RepositoryRESTReference-/repository/{id}/deviceInfo>`

        `repository: ip info <Repository.html#RepositoryRESTReference-/repository/{id}/ipInfo>`

        Args:
            id (int): The numeric id for the repository to query.
            dns (str): The DNS name to query
            fields (list, optional):
                The list of fields that are desired to be returned.  For details
                on what fields are available, please refer to the details on the
                request within the repository device info API doc.
            ip (str): The IP address to query
            uuid (str): The UUID to query.

        Returns:
            :obj:`dict`:
                The device resource.

        Examples:
            >>> host = sc.repositories.device_info(1, ip='192.168.0.1')
        '''
        # We will generally want to query the deviceInfo action, however if we
        # happen to be on a Tenable.sc instance version thats less than 5.7, we
        # have to instead query ipInfo.
        method = 'deviceInfo'
        if semver.match(self._api.version, '<5.7.0'):
            method = 'ipInfo'

        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])
        if dns:
            params['dnsName'] = self._check('dns', dns, str)
        if ip:
            params['ip'] = self._check('ip', ip, str)
        if uuid:
            params['uuid'] = self._check('uuid', uuid, 'uuid')

        return self._api.get('repository/{}/{}'.format(
            self._check('id', id, int), method), params=params).json()['response']

    def remote_authorize(self, host, username, password):
        '''
        Authorized communication to a downstream Tenable.sc instance with the
        provided username and password.

        :sc-api:`repository: authorize <Repository.html#RepositoryRESTReference-/repository/authorize>`

        Args:
            host (str): The downstream Tenable.sc instance ip address.
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
        Tenable.sc instance.

        :sc-api:`repository: fetch remote <Repository.html#RepositoryRESTReference-/repository/fetchRemote>`

        Args:
            host (str): The downstream Tenable.sc instance ip address.

        Returns:
            :obj:`list`:
                The list of repositories on the downstream Tenable.sc instance.
        '''
        return self._api.get('repository/fetchRemote', params={
            'host': self._check('host', host, str)}).json()['response']


