'''
Remediation Scans
=================

The following methods allow for interaction into the Tenable.io
:devportal:`Remediation scan create <io-scans-remediation-creates>` API endpoints.  # noqa: E501

Methods available on ``tio.v3.vm.remediation_scans``:

.. rst-class:: hide-signature
.. autoclass:: RemediationScansAPI
    :members:
'''


from typing import Dict, Union

from requests import Response

from tenable.errors import UnexpectedValueError
from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.io.v3.vm.remediation_scans.schema import \
    RemScansDocumentCreateSchema
from tenable.utils import dict_merge


class RemediationScansAPI(ExploreBaseEndpoint):
    '''
    This will contains all the methods for remediation scans
    '''
    _path = 'api/v3/scans'
    _conv_json = True

    def search(self,
               **kw
               ) -> Union[SearchIterator, CSVChunkIterator, Response]:
        '''
        Retrieves the remediation scans.

         Args:
            fields (list, optional):
                The list of field names to return from the Tenable API.
                Example:
                    >>> ['field1', 'field2']
            filter (tuple, dict, optional):
                A nestable filter object detailing how to filter the results
                down to the desired subset.
                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                    ...                 ('test', 'oper', '2')
                    ...             ),
                    ...     'and', ('test', 'oper', 3)
                    ... )
                    >>> {
                    ...  'or': [{
                    ...      'and': [{
                    ...              'value': '1',
                    ...              'operator': 'oper',
                    ...              'property': '1'
                    ...          },
                    ...          {
                    ...              'value': '2',
                    ...              'operator': 'oper',
                    ...              'property': '2'
                    ...          }
                    ...      ]
                    ...  }],
                    ...  'and': [{
                    ...      'value': '3',
                    ...      'operator': 'oper',
                    ...      'property': 3
                    ...  }]
                    ... }
                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth: `tio.v3.definitions.vm.remediation_scans()`
                endpoint
                to get more details.
            sort (list[tuple], optional):
                sort is a list of tuples in the form of
                ('FIELD', 'ORDER').
                It describes how to sort the data
                that is to be returned.
                Examples:
                    >>> [('field_name_1', 'asc'),
                    ...      ('field_name_2', 'desc')]
            limit (int, optional):
                Number of objects to be returned in each request.
                Default and max_limit is 200.
            next (str, optional):
                The pagination token to use when requesting the next page of
                results. This token is presented in the previous response.
            return_resp (bool, optional):
                If set to true, will override the default behavior to return
                a requests.Response Object to the user.
            return_csv (bool, optional):
                If set to true, it will return the CSV response or
                iterable (based on return_resp flag). Iterator returns all
                rows in text/csv format for each call with row headers.
        Returns:
            Iterable:
                The iterable that handles the pagination for the job.
            requests.Response:
                If ``return_resp`` is set to ``True``, then a response
                object is returned instead of an iterable.

        Examples:
            >>> tio.v3.vm.remediation_scans.search(
            ...     filter=('name','eq','SCCM'),
            ...     fields=['name', 'field_one', 'field_two'],
            ...     limit=2,
            ...     sort=[('last_observed', 'asc')]
            ... )
        '''
        iclass = SearchIterator
        if kw.get('return_csv', False):
            iclass = CSVChunkIterator
        return super()._search(resource='scans',
                               iterator_cls=iclass,
                               api_path=f'{self._path}/search',
                               **kw
                               )

    def create_remediation_scan(self, **kwargs: Dict) -> Dict:
        '''
        Create a new remediation scan.

        :devportal:`scans: create_remediation_scan <io-scans-remediation-create>` # noqa: E501

        Args:
            id (str, optional):
                UUID of Remediation scan template
            name (str):
                The name of the remediation scan to create.
            description (str, optional):
                The name of the scan to create.
            policy (int, optional):
                The id or title of the scan policy to use (if not using one of
                the pre-defined templates).  Specifying a a policy id will
                override the the template parameter.
            scanner_id (str, optional):
                The unique id of the scanner to use.
                Use the GET /scanners endpoint to find the scanner ID.
                You can use the special value AUTO-ROUTED to assign scan
                targets to scanner groups based on the groups' configured
                scan routes.
            target_network_id (str, optional):
                For remediation scans, enter
                a valid target network UUID from a previous scan you wish to
                remediate.
            scan_time_window (int, optional):
                The time frame, in minutes,
                during which agents must transmit scan results to Tenable.io
                in order to be included in dashboards and reports. If your
                request omits this parameter, the default value is 180 minutes.
                For non-agent scans, this attribute is null.
            text_targets (str, optional):
                The List of targets to scan
            targets (list, optional):
                If defined, then a list of targets can be specified and will
                be formatted to an appropriate text_target attribute.
                A list of targets to scan
            target_groups (list[int]):
                For remediation scans, enter a valid target group ID from a
                previous scan you wish to remediate.
            file_targets (string, optional):
                The name of a file containing the list of targets to scan.
            tag_targets (list[str], optional):
                The list of asset tag identifiers that the scan uses to
                determine which assets it evaluates
            agent_group_id (list[str], optional):
                An array of agent group UUIDs to scan.
            emails (list[str], optional):
                A comma-separated list of accounts that receive the email
                summary report.
            acls (list[dict], optional):
                A list of dictionaries containing permissions to apply to the
                scan.
            credentials (dict, optional):
                A list of credentials to use.
            enabled_plugins (list, optional):
                A list of plugins IDs to add to a remediation scan.
            **kw (dict, optional):
                The various parameters that can be passed to the scan creation
                API.  Examples would be `name`, `email`, `scanner_id`, etc.
                For more detailed information, please refer to the API
                documentation linked above.  Further, any keyword arguments
                passed that are not explicitly documented will be automatically
                appended to the settings document.  There is no need to pass
                settings directly.

        Returns:
            :obj:`dict`:
                The scan resource record of the newly created remediation scan.

        Examples:
            Create remediation scan:

        >>> scan = tio.v3.vm.remediation_scans.create_remediation_scan(
        ...     id='76d67790-2969-411e-a9d0-667f05e8d49e',
        ...     name='Create Remediation Scan',
        ...     description='Remediation scan created',
        ...     scanner_id='10167769',
        ...     scan_time_window=10,
        ...     targets=['127.0.0.1:3000'],
        ...     template='advanced')

            For further information on credentials, what settings to use, etc,
            refer to
            `this doc
            <https://developer.tenable.com/reference#io-scans-remediation-create>`_  # noqa E501
            on the developer portal.

        '''

        if 'template' not in kwargs:
            kwargs['template'] = 'advanced'

        scan = self._create_scan_document(kwargs)

        # Run the API call and return the result to the caller.
        return self._post('remediation', json=scan)['scan']

    def _create_scan_document(self, kwargs: Dict) -> Dict:
        '''
        Takes the key-word arguments and will provide a scan settings document
        based on the values inputted.
        Args:
            kwargs (dict):
                The keyword dict passed from the user
        Returns:
            :obj:`dict`:
                The resulting scan document based on the kwargs provided.
        '''
        scan = {
            'settings': {},
        }
        # collection of run-time data from different APIs for schema validation
        context_data = {}

        # If template is specified, then we will pull the listing of available
        # templates and set the policy UUID to match the template name given.
        templates = {}
        if 'template' in kwargs:
            # todo migrate it to v3
            templates = self._api.policies.templates()
            templates_choices = list(templates.keys())
            context_data['templates_choices'] = templates_choices

        # If a policy UUID is sent, then we will set the scan template UUID to
        # be the UUID that was specified.
        if 'policy' in kwargs:
            self._update_policy(kwargs, scan)
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
            scanners_choices = [s['id'] for s in scanners]
            context_data['scanners_choices'] = scanners_choices

        schema = RemScansDocumentCreateSchema(context=context_data)
        kwargs = schema.dump(schema.load(kwargs))

        if 'template' in kwargs:
            scan['id'] = templates[kwargs['template']]
            del kwargs['template']

        self._update_sub_doc_data(kwargs, scan)

        # any remaining keyword arguments will be passed into the settings
        # sub-document. The bulk of the data should go here...
        scan['settings'] = dict_merge(scan['settings'], kwargs)
        return scan

    def _update_policy(self, kwargs, scan):
        policies = self._api.policies.list()
        match = False

        # Here we iterate over each policy in the list, looking
        # to see if we see a match in either the name or the id.  If we do
        # find a match, then we will use the first one that matches, pull
        # the editor config, and then use the policy id and scan policy
        # template uuid.
        for item in policies:
            # todo update it with v3
            if kwargs['policy'] in [item['name'],
                                    item['id']] and not match:
                policy_tmpl = self._api.editor.details(
                    'scan/policy', item['id']
                )
                scan['id'] = policy_tmpl['uuid']
                scan['settings']['policy_id'] = item['id']
                match = True

        # if no match was discovered, then raise an invalid warning.
        if not match:
            raise UnexpectedValueError('policy setting is invalid.')

    def _update_sub_doc_data(self, kwargs, scan):
        if 'scanner' in kwargs:
            scan['settings']['scanner_id'] = kwargs['scanner']
            del kwargs['scanner']

        # If the targets parameter is specified, then we will need to convert
        # the list of targets to a comma-delimited string and then set the
        # text_targets parameter with the result.
        if 'targets' in kwargs:
            scan['settings']['text_targets'] = kwargs['targets']
            del kwargs['targets']

        # For credentials, we will simply push the dictionary as-is into the
        # the credentials.add sub-document.
        if 'credentials' in kwargs:
            scan['credentials'] = {'add': {}}
            scan['credentials']['add'] = kwargs['credentials']
            del kwargs['credentials']

        # Just like with credentials, we push the dictionary as-is into the
        # correct sub-document of the scan definition.
        if 'compliance' in kwargs:
            scan['audits'] = kwargs['compliance']
            del kwargs['compliance']

        if 'enabled_plugins' in kwargs:
            scan['enabled_plugins'] = kwargs['enabled_plugins']
            del kwargs['enabled_plugins']
