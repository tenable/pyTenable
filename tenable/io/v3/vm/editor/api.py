'''
Editor
======

The following methods allow for interaction into the Tenable.io
:devportal:`Editor <editor>` API endpoint.

Methods available on ``tio.v3.vm.editor``:

.. rst-class:: hide-signature
.. autoclass:: EditorAPI
    :members:
'''
from io import BytesIO
from typing import Dict, List, Optional
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.base.iterators.explore_iterator import (CSVChunkIterator,
                                                           SearchIterator)
from tenable.utils import (UnexpectedValueError, dict_clean, dict_merge,
                           policy_settings)


class EditorAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Editor API
    '''

    _path = 'api/v3/editor'
    _conv_json = True

    def audits(self,
               etype: str,
               object_id: int,
               file_id: int,
               fobj: Optional[BytesIO] = None,
               ) -> BytesIO:
        '''
        Retrieves an audit file from Tenable.io

        :devportal:`editor: audits <editor-audits>`

        Args:
            etype (str):
                The type of template to retrieve.  Must be either ``scan`` or
                ``policy``.
            object_id (int):
                The unique identifier of the object.
            file_id (int):
                The unique identifier of the file to export.
            fobj (FileObject):
                An optional File-like object to write the file to.  If none is
                provided a BytesIO object will be returned.

        Returns:
            :obj:`file`:
                A File-like object of of the audit file.

        Examples:
            >>> with open('audit_001.txt', 'wb') as report:
            ...     tio.v3.vm.editor.audits(
            ...         fobj=report,
            ...         etype='scan',
            ...         object_id=23,
            ...         file_id=12,
            ...     )
        '''
        etype_choices = {'scan', 'policy'}
        if etype not in etype_choices:
            raise UnexpectedValueError((
                f'etype has value of {etype}.  Expected one of '
                ','.join([str(i) for i in etype_choices])
            ))

        if not fobj:
            fobj = BytesIO()

        headers = {'Accept': 'application/octet-stream'}

        resp = self._get(
            f'{etype}/{object_id}/audits/{file_id}',
            headers=headers,
            stream=True,
        )

        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)

        fobj.seek(0)
        resp.close()

        return fobj

    def details(self, etype: str, id: int) -> Dict:  # noqa C901
        '''
        Constructs a valid scan document from the specified item.

        .. important::
            Please note that the details method is reverse-engineered from the
            responses from the editor API, and while we are reasonably sure
            that the response should align almost exactly to what the API
            expects to be pushed to it, this method by very nature of what it's
            doing isn't guaranteed to always work.

        Args:
            etype (str): The type of object to request.
            scan_id (int): The unique identifier for the scan.

        Returns:
            :obj:`dict`:
                The constructed scan configuration resource.

        Examples:
            >>> policy = tio.editor.details('scan', 1)
            >>> pprint(scan)
        '''

        # Get the editor object
        editor = self.obj_details(etype, id)

        # define the initial skeleton of the scan object
        obj = {
            'settings': policy_settings(editor['settings']),
            'id': editor['id'],
        }

        # graft on the basic settings that aren't stored in any input sections.
        for item in editor['settings']['basic']['groups']:
            for setting in item.keys():
                if setting not in ['name', 'title', 'inputs', 'sections']:
                    obj['settings'][setting] = item[setting]

        if 'credentials' in editor:
            # if the credentials sub-document exists, then lets walk down the
            # credentials dataset
            obj['credentials'] = {
                'current': self.parse_creds(editor['credentials']['data'])
            }

            # We also need to gather the settings from the various credential
            # settings that are unique to the scan.
            for ctype in editor['credentials']['data']:
                for citem in ctype['types']:
                    if 'settings' in citem and citem['settings']:
                        obj['settings'] = dict_merge(
                            obj['settings'], policy_settings(citem['settings'])
                        )

        if 'compliance' in editor:
            # if the audits sub-document exists, then lets walk down the
            # audits dataset.
            obj['compliance'] = {
                'current': self.parse_audits(editor['compliance']['data'])
            }

            # We also need to add in the 'compliance' settings into the scan
            # settings.
            for item in editor['compliance']['data']:
                obj['settings'] = dict_merge(
                    obj['settings'],
                    policy_settings(item.get('settings', {}))
                )

        if 'plugins' in editor:
            # if the plugins sub-document exists, then lets walk down the
            # plugins dataset.
            obj['plugins'] = self.parse_plugins(
                etype,
                editor['plugins']['families'],
                id
            )

        # We next need to do a little post-parsing of the ACLs to find the
        # owner and put owner_id attribute into the appropriate location.
        for acl in obj.get('settings', {}).get('acls', []):
            if acl['owner'] == 1:
                obj['settings']['owner_id'] = acl['id']

        # Clean out the empty attributes for templates:
        if etype == 'scan/policy':
            dict_clean(obj['settings'])

        # return the scan document to the caller.
        return obj

    def obj_details(self, etype: str, id: int) -> Dict:
        '''
        Retrieves details about a specific object.

        :devportal:`editor: template-details <editor-template-details>`

        Args:
            etype (str):
                The type of object to retrieve.  Must be either ``scan`` or
                ``policy``.
            id (int):
                The unique identifier of the object.

        Returns:
            :obj:`dict`:
                Details of the requested object

        Examples:
            >>> configuration_details = tio.v3.vm.editor.details(
            ...     etype='scan',
            ...     id=1
            ... )
            >>> pprint(configuration_details)
        '''
        etype_choices = {'scan', 'policy'}
        if etype not in etype_choices:
            raise UnexpectedValueError((
                f'etype has value of {etype}.  Expected one of '
                ','.join([str(i) for i in etype_choices])
            ))

        return self._get(f'{etype}/{id}')

    def parse_audits(self, data: List) -> Dict:
        '''
        Walks through the compliance data list and returns the configured
        settings for a given policy/scan
        '''
        resp = {'custom': list(), 'feed': dict()}

        for atype in data:
            for audit in atype['audits']:
                if audit['free'] == 0:
                    if audit['type'] == 'custom':
                        # if the audit is a custom-uploaded file, then we
                        # need to return the data using the format below,
                        # which appears to be how the UI sends the data.
                        fn = audit['summary'].split('File: ')[1]
                        resp['custom'].append(
                            {
                                'id': audit['id'],
                                'category': atype['name'],
                                'file': fn,
                                'variables': {
                                    'file': fn,
                                },
                            }
                        )
                    else:
                        # if we're using a audit file from the feed, then
                        # we will want to pull all of the parameterized
                        # variables with the set values and store them in
                        # the variables dictionary.
                        if atype['name'] not in resp['feed']:
                            resp['feed'][atype['name']] = list()
                        resp['feed'][atype['name']].append(
                            {
                                'id': audit['id'],
                                'variables': policy_settings(audit),
                            }
                        )
        return resp

    def parse_creds(self, data: List) -> Dict:
        '''
        Walks through the credential data list and returns the configured
        settings for a given scan policy/scan
        '''
        resp = dict()
        for dtype in data:
            for item in dtype['types']:
                if len(item['instances']) > 0:
                    for i in item['instances']:
                        # Get the settings from the inputs.
                        settings = policy_settings(i)
                        settings['id'] = i['id']
                        settings['summary'] = i['summary']

                        if dtype['name'] not in resp:
                            # if the Datatype doesn't exist yet, create it.
                            resp[dtype['name']] = dict()

                        if item['name'] not in resp[dtype['name']]:
                            # if the data subtype doesn't exist yet,
                            # create it.
                            resp[dtype['name']][item['name']] = list()

                        # Add the configured settings to the key-value
                        # dictionary
                        resp[dtype['name']][item['name']].append(settings)
        return resp

    def parse_plugins(self,
                      etype: str,
                      families: List,
                      id: int,
                      callfmt='editor/{etype}/{id}/families/{fam}'
                      ):
        '''
        Walks through the plugin settings and will return the the configured
        settings for a given scan/policy
        '''
        resp = dict()

        for family in families:
            if families[family]['status'] != 'mixed':
                # if the plugin family is wholly enabled or disabled, then
                # all we need to set is the status.
                resp[family] = {'status': families[family]['status']}
            else:
                # if the plugin family is set to mixed, we will need to get
                # the currently enabled status of every plugin within the
                # mixed families.  To do so, we will need to query the
                # scan editor for each mixed family, getting the plugin
                # listing w/ status an interpreting that into a simple
                # dictionary of plugin_id:status.
                plugins = dict()
                plugs = self._get(callfmt.format(
                    etype=etype, id=id, fam=families[family]['id'])
                )['plugins']
                for plugin in plugs:
                    plugins[plugin['id']] = plugin['status']
                resp[family] = {
                    'mixedDefault': 'enabled',
                    'status': 'mixed',
                    'individual': plugins,
                }
        return resp

    def plugin_details(self,
                       policy_id: int,
                       family_id: int,
                       plugin_id: int
                       ) -> List:
        '''
        Gets the details of the plugin associated with the scan or policy.

        :devportal:`editor: get plugin details <editor-plugin-description>`

        Args:
            policy_id (int): The ID of the policy to look up.
            family_id (int): The ID of the family to lookup within the policy.
            plugin_id (int): The ID of the plugin to lookup within the family.

        Returns:
            :obj:`list`:
                Resource record of the plugin.

        Examples:
            >>> plugin = tio.v3.vm.editor.plugin_details()
            >>> pprint(plugin)
        '''
        return self._get(
            f'policy/{policy_id}/families/{family_id}/plugins/{plugin_id}'
        )['plugindescription']

    def search_templates(self, etype: str, **kwargs) -> List:
        '''
        Lists Tenable-provided scan templates. Tenable provides a number of
        scan templates to facilitate the creation of scans and scan policies.
        For a full description of these scan templates, see the Tenable.io
        Vulnerability Management Guide.

        :devportal:`editor: search templates <editor-list-templates>`

        Args:
            etype (str):
                The type of templates to retrieve (scan, policy, or
                remediation).
            fields (list):
                The list of field names to return from the Tenable API.

                Example:
                    - ``['field1', 'field2']``
            filter (tuple, Dict):
                A nestable filter object detailing how to filter the results
                down to the desired subset.

                Examples:
                    >>> ('or', ('and', ('test', 'oper', '1'),
                                   ('test', 'oper', '2')
                            ),
                    'and', ('test', 'oper', 3)
                   )
                    >>> {'or': [
                    {'and': [
                        {'value': '1', 'operator': 'oper', 'property': '1'},
                        {'value': '2', 'operator': 'oper', 'property': '2'}
                        ]
                    }],
                    'and': [
                        {'value': '3', 'operator': 'oper', 'property': 3}
                        ]
                    }

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.v3.vm.filters.asset_filters()`
                endpoint to get more details.
            sort list(tuple, Dict):
                A list of dictionaries describing how to sort the data
                that is to be returned.

                Examples:
                    - ``[('field_name_1', 'asc'),
                             ('field_name_2', 'desc')]``
                    - ``[{'property': 'last_observed', 'order': 'desc'}]``
            limit (int):
                Number of objects to be returned in each request.
                Default is 1000.
            next (str):
                The pagination token to use when requesting the next page of
                results.  This token is presented in the previous response.
            return_resp (bool):
                If set to true, will override the default behavior to return
                an iterable and will instead return the results for the
                specific page of data.
            return_csv (bool):
                If set to true, It wil return the CSV Iterable. Returns all
                data in text/csv format on each next call with row headers
                on each page.

        Returns:
            Returns:
                Iterable:
                    The iterable that handles the pagination and potentially
                    async requests for the job.
                requests.Response:
                    If ``return_json`` was set to ``True``, then a response
                    object is instead returned instead of an iterable.

        Examples:
            >>> tio.v3.vm.editor.search(
            ...     etype='scan',
            ...     filter=('unsupported', 'eq', True),
            ...     fields=['title', 'id', 'desc'],
            ...     limit=2,
            ...     sort=[('container_name', 'asc')]
            ... )
        '''
        etype_choices = {'scan', 'policy', 'remediation'}
        if etype not in etype_choices:
            raise UnexpectedValueError((
                f'etype has value of {etype}.  Expected one of '
                ','.join([str(i) for i in etype_choices])
            ))
        iclass = SearchIterator
        if kwargs.get('return_csv', False):
            iclass = CSVChunkIterator
        return super().search(
            resource='templates',
            iterator_cls=iclass,
            is_sort_with_prop=False,
            api_path=f'{self._path}/{etype}/templates/search',
            **kwargs
        )

    def template_details(self, etype: str, id: UUID) -> List:
        '''
        Retrieves details about a specific template.

        :devportal:`editor: template-details <editor-template-details>`

        Args:
            etype (str):
                The type of template to retrieve.  Must be either ``scan`` or
                ``policy``.
            id (str):
                The UUID (unique identifier) for the template.

        Returns:
            :obj:`dict`:
                Details on the requested template

        Examples:
            >>> template = tio.v3.vm.editor.template_details(,
            >>> pprint(template)
        '''
        etype_choices = {'scan', 'policy', 'remediation'}
        if etype not in etype_choices:
            raise UnexpectedValueError((
                f'etype has value of {etype}.  Expected one of '
                ','.join([str(i) for i in etype_choices])
            ))
        return self._get(f'{etype}/templates/{id}')
