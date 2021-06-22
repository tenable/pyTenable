'''
Remediation Scans
=================

The following methods allow for interaction into the Tenable.io
:devportal:`scans <Create Remediation Scans>` API endpoints.
:devportal:`scans <List Remediation Scans>` API endpoints.
Methods available on ``tio.remediation_scans``:

.. rst-class:: hide-signature
.. autoclass:: RemediationScansAPI

.. automethod:: create_remediation_scans
.. automethod:: list_remediation_scans
'''


from tenable.constants import IOConstants
from tenable.errors import UnexpectedValueError
from tenable.io.base import TIOEndpoint, TIOIterator
from tenable.utils import dict_merge


class RemediationScansIteratorV2(TIOIterator):
    '''
The Remediation scans iterator provides a scalable way to work through
scan history result sets of any size. The iterator will walk through
each page of data, returning one record at a time.  If it reaches the
end of a page of records, then it will request the next page of
information and then continue to return records from the next page
(and the next, and the next) until the counter reaches the total number
of records that the API has reported.

Attributes:
    count (int): The current number of records that have been returned
    page (list):
        The current page of data being walked through.  pages will be
        cycled through as the iterator requests more information from the
        API.
    page_count (int): The number of record returned from the current page.
    total (int):
        The total number of records that exist for the current request.
'''
pass


class RemediationScansAPI(TIOEndpoint):
    '''
    This will contain all methods related to Remediation scans
    '''
    schedule_const = IOConstants.ScanScheduleConst
    case_const = IOConstants.CaseConst

    def list_remediation_scan(self, limit=50, offset=0, sortval='scan_creation_date:desc'):
        '''
        Retrieve the list of Remediation scans.

        :devportal:`scans/remediation: list <remediationscans-list>`

        Args:
            limit (int): This value needs to be between 0 and 200

            offset (int): This value needs to be > 0

            sort (str): scan_creation_date:desc/scan_creation_date:asc
                        Returns the remediation scan list with the ascending
            or descending order with offset and limit

        Returns:
            :obj:`list`:
                A list containing the list of remediation scan records.

        Examples:
            >>> for remediation_scan in tio.scans.list():
            ...     pprint(remediation_scan)

            For further information on credentials, what settings to use, etc,
            refer to
            `this doc <https://developer.tenable.com/reference#io-scans-remediation-list>`_
            on the developer portal.

            '''
        params = dict()
        pages = None
        if limit>0 and limit < 200:
            params['limit'] = self._check('limit', limit, int)
        if offset >= 0:
            params['offset'] = self._check('offset', offset, int)
        if 'scan_creation_date:asc' or 'scan_creation_date:desc' in sortval:
            params['sort'] = self._check('sort', sortval, str)

        return RemediationScansIteratorV2(self._api,
        _limit=limit,
        _offset=offset,
        _pages_total=pages,
        _query=params,
        _path='scans/remediation',
        _resource='scans')

    def create_remediation_scan(self, **kwargs):
        '''
        Create a new remediation scan.
        :devportal:`scans/remediation: create <remediationscans-create>`
        Args:

            uuid (str): UUID of Remediation scan template

            Settings Object Parameters :
            These are parameters passed through the keywords

            name (str): The name of the remediation scan to create.

            description (str): The name of the scan to create.

            policy (int, optional):
                The id or title of the scan policy to use (if not using one of
                the pre-defined templates).  Specifying a a policy id will
                override the the template parameter.

            scanner_id (str): The unique id of the scanner to use.
                Use the GET /scanners endpoint to find the scanner ID.
                You can use the special value AUTO-ROUTED to assign scan
                targets to scanner groups based on the groups' configured
                scan routes.

            target_network_uuid (str): For remediation scans, enter a valid target
             network UUID from a previous scan you wish to remediate.

            scan_time_window (int32): The time frame, in minutes, during which agents
            must transmit scan results to Tenable.io in order to be included in
            dashboards and reports. If your request omits this parameter,
            the default value is 180 minutes.
            For non-agent scans, this attribute is null.

            text_targets (str): The List of targets to scan

            targets (list, optional):
                If defined, then a list of targets can be specified and will
                be formatted to an appropriate text_target attribute.
                A list of targets to scan

            target_groups (int[]):
            For remediation scans, enter a valid target group ID from a previous scan you wish to remediate.

            file_targets (string):
            The name of a file containing the list of targets to scan.

            tag_targets (str[])
            The list of asset tag identifiers that the scan uses to determine which assets it evaluates

            agent_group_id (str[])
            An array of agent group UUIDs to scan.

            emails (str)
            A comma-separated list of accounts that receive the email summary report.

            acls (obj[])

            credentials (dict, optional):
                A list of credentials to use.

            enabled plugins (dict, optional):
                A list of plugins enabled to use.

            **kw (dict, optional):
                The various parameters that can be passed to the scan creation
                API.  Examples would be `name`, `email`, `scanner_id`, etc.  For
                more detailed information, please refer to the API documentation
                linked above.  Further, any keyword arguments passed that are
                not explicitly documented will be automatically appended to the
                settings document.  There is no need to pass settings directly.

        Returns:
            :obj:`dict`:
                The scan resource record of the newly created remediation scan.

        Examples:
            Create remediation scan:


        >>> scan = tio.remediationscans.create_remediation_scan(
        ... uuid='76d67790-2969-411e-a9d0-667f05e8d49e',
        ... name='Create Remediation Scan',
        ... description='Remediation scan created',
        ... scanner_id='10167769',
        ... scan_time_window=10,
        ... targets=['127.0.0.1:3000'],
        ... template='advanced')

            For further information on credentials, what settings to use, etc,
            refer to
            `this doc <https://developer.tenable.com/reference#io-scans-remediation-create>`_
            on the developer portal.

        '''

        if 'template' not in kwargs:
            kwargs['template'] = 'advanced'


        scan = self._create_scan_document(kwargs)

        # Run the API call and return the result to the caller.
        return  self._api.post('scans/remediation', json=scan).json()['scan']

    def _create_scan_document(self, kwargs):
        '''

        Takes the key-worded arguments and will provide a scan settings document
        based on the values inputted.

        Args:
            kwargs (dict): The keyword dict passed from the user
        Returns:
            :obj:`dict`:
                The resulting scan document based on the kwargs provided.

        '''
        scan = {
            'settings': dict(),
        }

        # If a template is specified, then we will pull the listing of available
        # templates and set the policy UUID to match the template name given.
        if 'template' in kwargs:

            templates = self._api.policies.templates()
            scan['uuid'] = templates[self._check(
                'template', kwargs['template'], str,
                default='advanced',
                choices=list(templates.keys())
            )]
            del kwargs['template']

        # If a policy UUID is sent, then we will set the scan template UUID to
        # be the UUID that was specified.

        if 'policy' in kwargs:
            policies = self._api.policies.list()
            match = False

            # Here we are going to iterate over each policy in the list, looking
            # to see if we see a match in either the name or the id.  If we do
            # find a match, then we will use the first one that matches, pull
            # the editor config, and then use the policy id and scan policy
            # template uuid.
            for item in policies:
                if kwargs['policy'] in [item['name'], item['id']] and not match:
                    policy_tmpl = self._api.editor.details('scan/policy', item['id'])
                    scan['uuid'] = policy_tmpl['uuid']
                    scan['settings']['policy_id'] = item['id']
                    match = True

            # if no match was discovered, then raise an invalid warning.
            if not match:
                raise UnexpectedValueError('policy setting is invalid.')
            del kwargs['policy']

        # if the scanner attribute was set, then we will attempt to figure out
        # what scanner to use.
        if 'scanner' in kwargs:
            scanners = self._api.scanners.allowed_scanners()

            # We will want to attempt to enumerate the scanner list and if
            # we see a name match, replace the scanner name with the UUID
            # of the scanner instead.
            for item in scanners:
                if item['name'] == kwargs['scanner']:
                    kwargs['scanner'] = item['id']

            # we will always want to attempt to use the UUID first as it's
            # the cheapest check that we can run.
            scan['settings']['scanner_id'] = self._check(
                'scanner', kwargs['scanner'], 'scanner-uuid',
                choices=[s['id'] for s in scanners])
            del kwargs['scanner']

        # If the targets parameter is specified, then we will need to convert
        # the list of targets to a comma-delimited string and then set the
        # text_targets parameter with the result.
        if 'targets' in kwargs:

            scan['settings']['text_targets'] = ','.join(self._check(
                'targets', kwargs['targets'], list))
            del kwargs['targets']

        # For credentials, we will simply push the dictionary as-is into the
        # the credentials.add sub-document.
        if 'credentials' in kwargs:
            scan['credentials'] = {'add': dict()}
            scan['credentials']['add'] = self._check(
                'credentials', kwargs['credentials'], dict)
            del kwargs['credentials']

        # Just like with credentials, we will push the dictionary as-is into the
        # correct sub-document of the scan definition.
        if 'compliance' in kwargs:
            scan['audits'] = self._check('compliance', kwargs['compliance'], dict)
            del kwargs['compliance']

        if 'plugins' in kwargs:
            scan['plugins'] = self._check('plugins', kwargs['plugins'], dict)
            del kwargs['plugins']


        # any other remaining keyword arguments will be passed into the settings
        # sub-document.  The bulk of the data should go here...

        scan['settings'] = dict_merge(scan['settings'], kwargs)

        return scan
