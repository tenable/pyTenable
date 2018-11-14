'''
scans
=====

The following methods allow for interaction into the SecurityCenter 
`Scan <https://docs.tenable.com/sccv/api/Scan.html>`_ API.

Methods available on ``sc.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScanAPI

    .. automethod:: copy
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: launch
    .. automethod:: list
    .. automethod:: update

.. iCal Date-Time:
    https://tools.ietf.org/html/rfc5545#section-3.3.5
.. iCal Recurrance Rule:
    https://tools.ietf.org/html/rfc5545#section-3.3.10
'''
from .base import SCEndpoint
from tenable.utils import dict_merge

class ScanAPI(SCEndpoint):
    def _scan_creator(self, **kw):
        '''
        Handles parsing the keywords and returns a scan definition document
        '''
        pass

    def list(self, fields=None):
        '''
        Retreives the list of scan definitions.

        + `SC Scan List <https://docs.tenable.com/sccv/api/Scan.html#scan_GET>`_

        Args:
            fields (list, optional): 
                A list of attributed to return for each scan.

        Returns:
            list: A list of scan resources.

        Examples:
            >>> for scan in sc.scans.list():
            ...     pprint(scan)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('scan', params=params).json()['response']

    def create(self, **kw):
        '''
        Creates a scan definition.

        + `SC Scan Create <https://docs.tenable.com/sccv/api/Scan.html#scan_POST>`_

        Args:
            name (str): The name of the scan.
            repository (int):
                The repository id for the scan.
            auto_mitigation (int, optional):
                How long to hold on to data before mitigating it?  The default
                value is 0.
            assets (list, optional):
                A list of asset list ids to run the scan against.  A logical OR
                will be performed to comupute what hosts to scan against.
            credentials (list, optional):
                A list of credential ids to use for tue purposes of this scan.
                This list should be treated as an un-ordered list of credentials.
            description (str, optional): A description for the scan.
            email_complete (bool, optional):
                Should we notify the owner upon completion of the scan?  The
                default is ``False``.
            email_launch (bool, optional):
                Should we notify the owner upon launching the scan?  The default
                is ``False``.
            host_tracking (bool, optional):
                Should DHCP host tracking be enabled?  The default is False.
            max_time (int, optional):
                The maximum amount of time that the scan may run in seconds.
                The default is ``3600`` seconds.
            policy (int, optional): 
                The policy id to use for a policy-based scan.
            plugin (int, optional):
                The plugin id to use for a plugin-based scan.
            reports (list, optional):
                What reports should be run upon completion of the scan?  Each
                report dictionary requires an id for the report definition and
                the source for which to run the report against.  Example:
                ``{'id': 1, 'reportSource': 'individual'}``.
            rollover (str, optional):
                How should rollover scans be created (assuming the scan is 
                configured to create a rollover scan with the timeout action).
                The available actions are to automatically start the ``nextDay``
                at the same time the scan was originally configured to run, and
                to generate a rollover ``template``.  The default action is to
                generate a ``template``.
            schedule_type (str, optional):
                What type of scan schedule shall this be?  Available supported
                values are ``dependent``, ``ical``, ``never``, ``rollover``, and
                ``template``.  The default value if unspecified is ``never``.
            schedule_start (str, optional):
                The time in which the trigger should start firing.  This value
                must conform to the `iCal Date-Time`_ standard.  Further this
                parameter is only required when specifying the schedule_type as
                ``ical``.
            schedule_repeat (str, optional):
                The rule that dictates the frequency and timing that the alert
                will run.  This value must conform to the `iCal Recurrance Rule`_
                format.  Further this parameter is only required when specifying
                the schedule_type as ``ical``.
            targets (list, optional):
                A list of valid targets.  These targets could be IPs, FQDNs,
                CIDRs, or IP ranges.
            timeout (str, optional):
                How should an incomplete scan be handled?  The available actions
                are ``discard``, ``import``, and ``rollover``.  The default
                action is ``import``.
            vhosts (bool, optional):
                Should virtual host logic be enabled for the scan?  The default
                is ``False``.
            zone (int, optional):
                The zone identifier to use for the scan.  If non is selected
                then the default of "0" or "All Zones" is selected.
        
        Returns:
            dict: The scan resource for the created scan.

        Examples:
            Creating a scan for a single host:

            >>> sc.scans.create(name='Example scan', policy=1001,
            ...     targets=['127.0.0.1'])
        '''
        scan = self._scan_creator(**kw)
        return self._api.post('scan', json=scan).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific scan.

        + `SC Scan Details <https://docs.tenable.com/sccv/api/Scan.html#ScanRESTReference-/scan/{id}>`_

        Args:
            id (int): The identifier for the scan.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: The alert resource record.

        Examples:
            >>> alert = sc.alerts.detail(1)
            >>> pprint(alert)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('scan/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def update(self, id, **kw):
        '''
        Updates an existing scan definition.

        + `SC Scan Update <https://docs.tenable.com/sccv/api/Scan.html#scan_id_PATCH>`_

        Args:
            id (int): The identifier for the scan.
            auto_mitigation (int, optional):
                How long to hold on to data before mitigating it?  The default
                value is 0.
            assets (list, optional):
                A list of asset list ids to run the scan against.  A logical OR
                will be performed to comupute what hosts to scan against.
            credentials (list, optional):
                A list of credential ids to use for tue purposes of this scan.
                This list should be treated as an un-ordered list of credentials.
            description (str, optional): A description for the scan.
            email_complete (bool, optional):
                Should we notify the owner upon completion of the scan?  The
                default is ``False``.
            email_launch (bool, optional):
                Should we notify the owner upon launching the scan?  The default
                is ``False``.
            host_tracking (bool, optional):
                Should DHCP host tracking be enabled?  The default is False.
            max_time (int, optional):
                The maximum amount of time that the scan may run in seconds.
                The default is ``3600`` seconds.
            name (str, optional): The name of the scan.
            policy (int, optional): 
                The policy id to use for a policy-based scan.
            plugin (int, optional):
                The plugin id to use for a plugin-based scan.
            reports (list, optional):
                What reports should be run upon completion of the scan?  Each
                report dictionary requires an id for the report definition and
                the source for which to run the report against.  Example:
                ``{'id': 1, 'reportSource': 'individual'}``.
            repository (int, optional):
                The repository id for the scan.
            rollover (str, optional):
                How should rollover scans be created (assuming the scan is 
                configured to create a rollover scan with the timeout action).
                The available actions are to automatically start the ``nextDay``
                at the same time the scan was originally configured to run, and
                to generate a rollover ``template``.  The default action is to
                generate a ``template``.
            schedule_type (str, optional):
                What type of scan schedule shall this be?  Available supported
                values are ``dependent``, ``ical``, ``never``, ``rollover``, and
                ``template``.  The default value if unspecified is ``never``.
            schedule_start (str, optional):
                The time in which the trigger should start firing.  This value
                must conform to the `iCal Date-Time`_ standard.  Further this
                parameter is only required when specifying the schedule_type as
                ``ical``.
            schedule_repeat (str, optional):
                The rule that dictates the frequency and timing that the alert
                will run.  This value must conform to the `iCal Recurrance Rule`_
                format.  Further this parameter is only required when specifying
                the schedule_type as ``ical``.
            targets (list, optional):
                A list of valid targets.  These targets could be IPs, FQDNs,
                CIDRs, or IP ranges.
            timeout (str, optional):
                How should an incomplete scan be handled?  The available actions
                are ``discard``, ``import``, and ``rollover``.  The default
                action is ``import``.
            vhosts (bool, optional):
                Should virtual host logic be enabled for the scan?  The default
                is ``False``.
            zone (int, optional):
                The zone identifier to use for the scan.  If non is selected
                then the default of "0" or "All Zones" is selected.
        
        Returns:
            dict: The scan resource for the created scan.

        Examples:
            Creating a scan for a single host:

            >>> sc.scans.update(1, name='Example scan')
        '''
        scan = self._scan_creator(**kw)
        return self._api.patch('scan/{}'.format(self._check('id', id, int)), 
            json=scan).json()['response']

    def delete(self, id):
        '''
        Removes the specified scan from SecurityCenter.

        + `SC Scan Delete <https://docs.tenable.com/sccv/api/Scan.html#scan_id_DELETE>`_

        Args:
            id (int): The identifier for the scan to delete.

        Returns:
            list: The list of scan id removed.

        Examples:
            >>> sc.scans.delete(1)
        '''
        return self._api.delete('scan/{}'.format(self._check('id', id, int))
            ).json()['response']['scans']

    def copy(self, id, name=None, user_id=None):
        '''
        Copies an existing scan definition.

        + `SC Scan Copy <https://docs.tenable.com/sccv/api/Scan.html#ScanRESTReference-/scan/{id}/copyScanCopyPOST1>`_

        Args:
            id (int): The scan definition identifier to copy.
            name (str, optional): The name of the copy thats created.
            user_id (int, optional): 
                The user id to assign as the owner of the new scan definition.

        Returns:
            dict: Scan definition resource.

        Examples:
            >>> sc.scans.copy(1, name='Cloned Scan')
        '''
        payload = dict()
        if name:
            payload['name'] = self._check('name', name, str)
        if user_id:
            payload['targetUser'] = {'id': self._check('user_id', user_id, int)}

        return self._api.post('scan/{}/copy'.format(
            self._check('id', id, int)), json=payload).json()['response']['scan']

    def launch(self, id, diagnostic_target=None, diagnostic_password=None):
        '''
        Launches a scan definition.

        + `SC Scan <https://docs.tenable.com/sccv/api/Scan.html#ScanRESTReference-/scan/{id}/launch>`_

        Args:
            id (int): The scan definition identifier to launch.
            diagnostic_target (str, optional):
                A valid IP or hostname to launch a diagnostic scan against.  The
                ``diagnostic_password`` must also be specified or else this
                parameter will be ignored.
            diagnostic_password (str, optional):
                A password to use for the diagnostic scan.  The
                ``diagnostic_target`` must also be specified or else this
                parameter will be ignored.

        Returns:
            dict: A scan result resource for the newly launched scan.

        Examples:
            >>> running = sc.scans.launch(1)
            >>> print('The Scan Result ID is {}'.format(
            ...     running['scanResult']['id']))
        '''
        payload = dict()
        if diagnostic_target and diagnostic_passwsord:
            payload['diagnosticTarget'] = self._check(
                'diagnostic_target', diagnostic_target, str)
            payload['diagnosticPassword'] = self._check(
                'diagnostic_password', diagnostic_password, str)

        return self._api.post('scan/{}/launch'.format(
            self._check('id', id, int)), json=payload).json()['response']