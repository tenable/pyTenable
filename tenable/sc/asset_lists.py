'''
asset_lists
===========

The following methods allow for interaction into the Tenable.sc
:sc-api:`Assets <Asset.html>` API.  These items are typically seen
under the **Assets** section of Tenable.sc.

Methods available on ``sc.asset_lists``:

.. rst-class:: hide-signature
.. autoclass:: AssetListAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
'''
from .base import SCEndpoint
from tenable.errors import UnexpectedValueError
from io import BytesIO

class AssetListAPI(SCEndpoint):
    def _dynamic_rules_constructor(self, rule, sub=False):
        '''
        Handles expanding the tuple format into the JSON formatted request.
        '''
        if isinstance(rule, dict):
            # if the rule is a dictionary, then simply pass it through as-is.
            return rule
        elif isinstance(rule, tuple):
            # if the rule is a tuple, then we will want to convert it into the
            # expected dictionary format.
            if rule[0] in ['all', 'any']:
                # if the first parameter in the tuple is either "any" or "all",
                # we will then assume that this is a group of rules, and call
                # the rule constructor for every subsequent parameter in the
                # tuple.
                resp = {
                    'operator': rule[0],
                    'children': [self._dynamic_rules_constructor(r, sub=True)
                        for r in rule[1:]]
                }
                if sub:
                    resp['type'] = 'group'
            else:
                # as the first item was _not_ "all" or "any", we're safe to
                # assume that the rule is actually a rule clause.  In this case
                # we will want to validate the fields based on the potential
                # known values that each attribute could have.  The rule should
                # generally be constructed in the following format:
                #
                # ('filterName', 'operator', 'value')
                #
                # or in the case of a plugin constraint, then there will be a
                # fourth parameter like so:
                #
                # ('filterName', 'operator', 'value', int(pluginID))
                # or
                # ('filterName', 'operator', 'value', list(id1, id2, id3, etc.))
                resp = {
                    'type': 'clause',
                    'filterName': self._check('rule:name', rule[0], str,
                        choices=['dns', 'exploitAvailable', 'exploitFrameworks',
                            'firstseen', 'mac', 'os', 'ip', 'lastseen',
                            'netbioshost', 'netbiosworkgroup', 'pluginid',
                            'plugintext', 'port', 'severity', 'sshv1', 'sshv2',
                            'tcpport', 'udpport', 'xref']),
                    'operator': self._check('rule:operator', rule[1], str,
                        choices=['contains', 'eq', 'lt', 'lte', 'ne', 'gt',
                            'gte', 'regex', 'pcre'])
                }

                # if the value is an integer, then we will want to ensure that
                # we wrap the value within an id dictionary.  This is necessary
                # for pluginid and severity filter names.  In all other cases
                # the value should be a string.
                if rule[0] in ['pluginid', 'severity']:
                    resp['value'] = {
                        'id': self._check('rule:value', rule[2], int)}
                else:
                    resp['value'] = self._check('rule:value', rule[2], str)

                # if there is a plugin constraint, then we will want to convert
                # the plugin constraint into a string value.  If it's a single
                # plugin id, then we will simply convert from int to str.  If
                # a list of values is provided, then we will build a comma-delim
                # string with the values that were passed.
                if len(rule) == 4:
                    if isinstance(rule[3], int):
                        resp['pluginIDConstraint'] = str(rule[3])
                    elif isinstance(rule[3], list):
                        resp['pluginIDConstraint'] = ','.join(
                            [str(r) for r in rule[3]])
                    else:
                        raise TypeError(
                            'rule {} has an invalid plugin constraint.'.format(rule))
        else:
            raise TypeError('rules {} not a tuple or dict'.format(rule))
        return resp

    def _constructor(self, **kw):
        '''
        Handles parsing the keywords and returns a asset-list definition document
        '''
        if 'type' in kw:
            # ensure that they type is a string and is one of the valid values.
            self._check('type', kw['type'], str, choices=[
                'combination', 'dnsname', 'dnsnameupload', 'dynamic',
                'ldapquery', 'static', 'staticeventfilter', 'staticvulnfilter',
                'templates', 'upload', 'watchlist', 'watchlisteventfilter',
                'watchlistupload'])

        if 'prep' in kw:
            # ensure that prep is a boolean value and store the string equiv in
            # the prepare parameter.
            kw['prepare'] = str(self._check('prep', kw['prep'], bool)).lower()
            del(kw['prep'])

        if 'name' in kw:
            # validate that the name param is a string
            self._check('name', kw['name'], str)

        if 'description' in kw:
            # validate that the description param is a string
            self._check('description', kw['description'], str)

        if 'context' in kw:
            # validate that the context param is a string
            self._check('context', kw['context'], str)

        if 'tags' in kw:
            # validate that the tags param is a string
            self._check('tags', kw['tags'], str)

        if 'template' in kw:
            # if the template param is an integer then convert it into a dict
            # with the integer value stored in the id attribute.  If the
            # template attribute is a dictionary, then we will simply assume
            # that the information is what we want to pass and allow through.
            if isinstance(kw['template'], int):
                kw['template'] = {'id': self._check('template', kw['template'], int)}
            else:
                self._check('template', kw['template'], dict)

        if 'filename' in kw:
            # Validate that the filename is a string value
            self._check('filename', kw['filename'], str)

        if 'fobj' in kw:
            # Uploads the file object and stores the returned name in filename.
            kw['filename'] = self._api.files.upload(kw['fobj'])
            del(kw['fobj'])

        if 'data_fields' in kw:
            # validate that the data_fields parameter is a list and store it
            # within the assetDataFields attribute.
            kw['assetDataFields'] = self._check(
                'data_fields', kw['data_fields'], list)
            del(kw['data_fields'])

        if 'combinations' in kw:
            # if the combinations parameter is a tuple, then send the value to
            # the combo_expansion method to convert the tuple to the dictionary
            # equivalent.  If the value is a dictionary, then simply pass the
            # value as-is.
            if isinstance(kw['combinations'], tuple):
                kw['combinations'] = self._combo_expansion(kw['combinations'])
            else:
                self._check('combinations', kw['combinations'], dict)

        if 'rules' in kw:
            # pass the rules parameter to the dynamic rules constructor to
            # convert the rules from a tuple to an expanded dictionary or just
            # pass through the dictionary value if presented with a dict.
            kw['rules'] = self._dynamic_rules_constructor(kw['rules'])

        if 'dns_names' in kw:
            # validate the dns_names parameter is a list or str value and store
            # it within the definedDNSNames attribute.
            if isinstance(kw['dns_names'], list):
                kw['definedDNSNames'] = ','.join([
                    self._check('dns:item', i, str) for i in kw['dns_names']])
            else:
                kw['definedDNSNames'] = self._check(
                    'dns_names', kw['dns_names'], str)
            del(kw['dns_names'])

        if 'dn' in kw and 'search_string' in kw and 'ldap_id' in kw:
            # if the dn, search_string, and ldap_id attributes are all defined,
            # then construct the definedLDAPQuery sub-document with these fields
            # and validate that they are the appropriate types.
            kw['definedLDAPQuery'] = {
                'searchBase': self._check('dn', kw['dn'], str),
                'searchString': self._check(
                    'search_string', kw['search_string'], str),
                'ldap': {'id': self._check('ldap_id', kw['ldap_id'], int)}
            }
            del(kw['dn'])
            del(kw['search_string'])
            del(kw['ldap_id'])
        elif (('dn' in kw and ('search_string' not in kw or 'ldap_id' not in kw))
          or ('search_string' in kw and ('dn' not in kw or 'ldap_id' not in kw))
          or ('ldap_id' in kw and ('search_string' not in kw or 'dn' not in kw))):
            raise UnexpectedValueError(
                'dn, search_string, and ldap_id must all be present')

        if 'ips' in kw:
            # validate that ips is either a list or a string value and store the
            # value as a comma-seperated string in definedIPs
            if isinstance(kw['ips'], list):
                kw['definedIPs'] = ','.join([self._check('ips:item', i, str)
                    for i in kw['ips']])
            else:
                kw['definedIPs'] = self._check('ips', kw['ips'], str)
            del(kw['ips'])

        if 'exclude_managed_ips' in kw:
            # validate that exclude managed ips is a boolean value and store the
            # value as a string in excludeManagedIPs
            kw['excludeManagedIPs'] = str(self._check('exclude_managed_ips',
                kw['exclude_managed_ips'], bool)).lower()
            del(kw['exclude_managed_ips'])

        if 'filters' in kw:
            # validate the filters attribute is a list.  For each item, we will
            # want to convert any tuples to the expanded dictionaries and simply
            # pass through any dictionaries.
            flist = list()
            for f in self._check('filters', kw['filters'], list):
                if isinstance(f, tuple):
                    flist.append({
                        'filterName': self._check('filter:name', f[0], str),
                        'operator': self._check('filter:operator', f[1], str),
                        'value': self._check('filter:value', f[2], str)
                    })
                else:
                    flist.append(self._check('filter', f, dict))
            kw['filters'] = flist

        if 'tool' in kw:
            # Validate that the tools attribute is a string,
            self._check('tool', kw['tool'], str)

        if 'source_type' in kw:
            # validate that the source_type parameter is a string and store it
            # within the camelCase equiv.
            kw['sourceType'] = self._check(
                'source_type', kw['source_type'], str)
            del(kw['source_type'])

        if 'start_offset' in kw:
            # validate the start offset is an integer value and store it within
            # the camelCase equiv.
            kw['startOffset'] = self._check(
                'start_offset', kw['start_offset'], int)
            del(kw['start_offset'])

        if 'end_offset' in kw:
            # validate that the end offset is an integer value and store it
            # the camelCase equiv.
            kw['endOffset'] = self._check(
                'end_offset', kw['end_offset'], int)
            del(kw['end_offset'])

        if 'view' in kw:
            # validate that the view is a string value.
            self._check('view', kw['view'], str)

        if 'lce_id' in kw:
            # validate that the lce_id is an integer value and store it as a
            # dictionary within the lce attribute.
            kw['lce'] = {'id': self._check('lce_id', kw['lce_id'], int)}
            del(kw['lce_id'])

        if 'sort_field' in kw:
            # validate that sort_field is a string value and store within the
            # camelCase equiv.
            kw['sortField'] = self._check('sort_field', kw['sort_field'], str)
            del(kw['sort_field'])

        if 'sort_dir' in kw:
            # validate that sort_dir is a string value of either ASC or DESC and
            # store it within the camelCase equiv.
            kw['sortDir'] = self._check('sort_dir', kw['sort_dir'], str,
                case='upper', choices=['ASC', 'DESC'])
            del(kw['sort_dir'])

        if 'scan_id' in kw:
            # validate that the scan_id value is an integer and store it within
            # the camelCase equiv.
            kw['scanID'] = self._check('scan_id', kw['scan_id'], int)
            del(kw['scan_id'])

        return kw

    def create(self, name, list_type, **kw):
        '''
        Creates an asset-list.

        :sc-api:`asset-list: create <Asset.html#asset_POST>`

        Args:
            name (str):
                The name for the asset list to create.
            list_type (str):
                The type of list to create.  Supported values are
                ``combination``, ``dnsname``, ``dnsnameupload``, ``dynamic``,
                ``ldapquery``, ``static``, ``staticeventfilter``,
                ``staticvulnfilter``, ``templates``, ``upload``, ``watchlist``,
                ``watchlisteventfilter``, and ``watchlistupload``.
            combinations (tuple, optional):
                An asset combination tuple.  For further information refer to
                the asset combination logic described at
                :mod:`tenable.sc.analysis`.
            data_fields (list, optional):
                A list of data fields as required for a given asset list type.
                Each item within the list should be formatted in the following
                way: ``{'fieldName': 'name', 'fieldValue': 'value'}``
            description (str, optional):
                The description for the asset list being created.
            dn (str, optional):
                The base DN to use for an LDAP query.  Must also provide a
                ``search_string`` and an ``ldap_id``.
            dns_names (list, optional):
                When defining a DNS asset list, use this attribute to provide
                the list of DNS addresses.
            exclude_managed_ips (bool, optional):
                Determines whether or not managed IPs should be excluded from
                the asset list.
            filters (list, optional):
                A list of filter tuples to use when defining filtered asset
                list types.  Follows the same format as filters within the rest
                of pyTenable.
            fobj (FileObject, optional):
                A file-like object to use when uploading an asset list.
            ips (list, optional):
                A list of IP Addresses, CIDRs, and/or IP Address ranges to use
                for the purposes of a static asset list.
            lce_id (int, optional):
                When defining a event-based asset list, which LCE should be used
                to generate the asset list query.
            ldap_id (int, optional):
                The numeric identifier pertaining to the LDAP server to use for
                an LDAP query.  must also provide a ``dn`` and a
                ``search_string``.
            prep (bool, optional):
                Should asset preparation be run after the list is created?  If
                unspecified, the default action is ``True``.
            rules (tuple, optional):
                For a dynamic asset list, the tuple definition of the rules to
                determine what Ips are associated to this asset list.  Rules
                follow a similar pattern to the asset combination logic and
                are written in a way to follow the same visual methodology as
                the UI.

                For example, a simple dynamic ruleset may look like:

                .. code-block:: python

                    ('any', ('dns', 'contains', 'svc.company.tld'),
                            ('dns', 'contains', 'prod.company.tld'))

                Which would match all assets with either svc.company.tld or
                prod.company.tld in their DNS names.  Rule gropups can be nested
                as well, by supplying a new group tuple instead of a rule:

                .. code-block:: python

                    ('any', ('dns', 'contains', 'svc.company.tld'),
                            ('dns', 'contains', 'prod.company.tld'),
                            ('any', ('ip', 'contains', '192.168.140'),
                                    ('ip', 'contains', '192.168.141')))

                In this example we have nested another group requiring that the
                ip may contain either of the values in addition to any of the
                DNS rules.

                It's also possible to constrain the rule to a specific plugin or
                plugins as well by adding a 4th element in a rule tuple.
                Defining them would look like so:

                .. code-block:: python

                    # Singular Plugin ID
                    ('plugintext', 'contains', 'credentialed', 19506)
                    # Multiple Plugin IDs
                    ('plugintext', 'contains', 'stuff', [19506, 10180])

                * Available rules are ``dns``, ``exploitAvailable``,
                  ``exploitFrameworks``, ``firstseen``, ``mac``, ``os``, ``ip``,
                  ``lastseen``, ``netbioshost``, ``netbiosworkgroup``,
                  ``pluginid``, ``plugintext``, ``port``, ``severity``, ``sshv1``,
                  ``sshv2``, ``tcpport``, ``udpport``, and ``xref``.
                * Available operators are ``contains``, ``eq``, ``lt``, ``lte``,
                  ``ne``, ``gt``, ``gte``, ``regex``, ``pcre``.
                * Group alauses are either ``any`` or ``all``.  Any is a logical
                  or.  All is a logical and.
            scan_id (int, optional):
                When defining an "individual" source_type, the numeric id of the
                scan instance to base the query upon.
            search_string (str, optional):
                The search string to use as part of an LDAP Query.  Must also
                provide a ``dn`` and an ``ldap_id``.
            sort_dir (str, optional):
                When defining a filtered asset list type, determines the
                direction of the sort to use.  This field must be passed when
                defining a sort_field.
            sort_field (str, optional):
                When defining a filtered asset list type, determines what field
                to sort the resulting query on.
            source_type (str, optional):
                The source of the data to query from when defining a filtered
                asset list type.
            start_offset (int, optional):
                The start offset of the filter to use when defining a filtered
                asset list type.
            tags (str, optional):
                A tag to associate to the asset list.
            template (int, optional):
                The numeric id of the template to use.
            tool (str, optional):
                When specifying filtered asset list types, the analysis tool to
                use for determining what IPs should be included within the
                asset list.
            view (str, optional):
                When the source_type is "individual", the view defined what
                subset of the data to use.

        Returns:
            dict: The newly created asset-list.

        Examples:
            >>> asset-list = sc.asset_lists.create()
        '''
        kw['name'] = name
        kw['type'] = list_type

        payload = self._constructor(**kw)
        return self._api.post('asset', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific asset-list.

        :sc-api:`asset-list: details <Asset.html#AssetRESTReference-/asset/{id}>`

        Args:
            id (int): The identifier for the asset-list.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: The asset-list resource record.

        Examples:
            >>> asset-list = sc.asset_lists.details(1)
            >>> pprint(asset-list)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('asset/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, **kw):
        '''
        Edits an asset-list.

        :sc-api:`asset-list: edit <Asset.html#asset_id_PATCH>`

        Args:
            id (int):
                The numeric id of the asset list to edit.
            combinations (tuple, optional):
                An asset combination tuple.  For further information refer to
                the asset combination logic described at
                :mod:`tenable.sc.analysis`.
            data_fields (list, optional):
                A list of data fields as required for a given asset list type.
                Each item within the list should be formatted in the following
                way: ``{'fieldName': 'name', 'fieldValue': 'value'}``
            description (str, optional):
                The description for the asset list being created.
            dn (str, optional):
                The base DN to use for an LDAP query.  Must also provide a
                ``search_string`` and an ``ldap_id``.
            dns_names (list, optional):
                When defining a DNS asset list, use this attribute to provide
                the list of DNS addresses.
            exclude_managed_ips (bool, optional):
                Determines whether or not managed IPs should be excluded from
                the asset list.
            filters (list, optional):
                A list of filter tuples to use when defining filtered asset
                list types.  Follows the same format as filters within the rest
                of pyTenable.
            fobj (FileObject, optional):
                A file-like object to use when uploading an asset list.
            ips (list, optional):
                A list of IP Addresses, CIDRs, and/or IP Address ranges to use
                for the purposes of a static asset list.
            lce_id (int, optional):
                When defining a event-based asset list, which LCE should be used
                to generate the asset list query.
            ldap_id (int, optional):
                The numeric identifier pertaining to the LDAP server to use for
                an LDAP query.  must also provide a ``dn`` and a
                ``search_string``.
            name (str, optional):
                The name for the asset list to create.
            prep (bool, optional):
                Should asset preparation be run after the list is created?  If
                unspecified, the default action is ``True``.
            rules (tuple, optional):
                For a dynamic asset list, the tuple definition of the rules to
                determine what Ips are associated to this asset list.  Rules
                follow a similar pattern to the asset combination logic and
                are written in a way to follow the same visual methodology as
                the UI.
            scan_id (int, optional):
                When defining an "individual" source_type, the numeric id of the
                scan instance to base the query upon.
            search_string (str, optional):
                The search string to use as part of an LDAP Query.  Must also
                provide a ``dn`` and an ``ldap_id``.
            sort_dir (str, optional):
                When defining a filtered asset list type, determines the
                direction of the sort to use.  This field must be passed when
                defining a sort_field.
            sort_field (str, optional):
                When defining a filtered asset list type, determines what field
                to sort the resulting query on.
            source_type (str, optional):
                The source of the data to query from when defining a filtered
                asset list type.
            start_offset (int, optional):
                The start offset of the filter to use when defining a filtered
                asset list type.
            tags (str, optional):
                A tag to associate to the asset list.
            template (int, optional):
                The numeric id of the template to use.
            tool (str, optional):
                When specifying filtered asset list types, the analysis tool to
                use for determining what IPs should be included within the
                asset list.
            type (str, optional):
                The type of list to create.  Supported values are
                ``combination``, ``dnsname``, ``dnsnameupload``, ``dynamic``,
                ``ldapquery``, ``static``, ``staticeventfilter``,
                ``staticvulnfilter``, ``templates``, ``upload``, ``watchlist``,
                ``watchlisteventfilter``, and ``watchlistupload``.
            view (str, optional):
                When the source_type is "individual", the view defined what
                subset of the data to use.

        Returns:
            dict: The newly updated asset-list.

        Examples:
            >>> asset-list = sc.asset_lists.edit()
        '''
        payload = self._constructor(**kw)
        return self._api.patch('asset/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a asset-list.

        :sc-api:`asset-list: delete <Asset.html#asset_id_DELETE>`

        Args:
            id (int): The numeric identifier for the asset-list to remove.

        Returns:
            dict: The deletion response dict

        Examples:
            >>> sc.asset_lists.delete(1)
        '''
        return self._api.delete('asset/{}'.format(
            self._check('id', id, int))).json()['response']

    def list(self, fields=None):
        '''
        Retrieves the list of asset list definitions.

        :sc-api:`asset-list: list <Asset.html#AssetRESTReference-/asset>`

        Args:
            fields (list, optional):
                A list of attributes to return for each asset-list.

        Returns:
            list: A list of asset-list resources.

        Examples:
            >>> for asset-list in sc.asset_lists.list():
            ...     pprint(asset-list)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('asset', params=params).json()['response']

    def import_definition(self, fobj, name=None):
        '''
        Imports an asset list definition from an asset list definition XML file.

        :sc-api:`asset-list: import <Asset.html#asset_import_POST>`

        Args:
            name (str): The name of the asset definition to create.
            fobj (FileObject):
                The file-like object containing the XML definition.

        Returns:
            :obj:`dict`:
                The created asset list from the import.

        Examples:
            >>> with open('example.xml', 'rb') as fobj:
            ...     sc.asset_lists.import_definition('Example', fobj)
        '''
        payload = {'filename': self._api.files.upload(fobj)}
        if name:
            payload['name'] = self._check('name', name, str)
        return self._api.post('asset/import', json=payload).json()['response']

    def export_definition(self, id, fobj=None):
        '''
        Exports an asset list definition and stored the data in the file-like
        object that was passed.

        :sc-api:`asset-list: export <Asset.html#AssetRESTReference-/asset/{id}/export>`

        Args:
            id (int): The numeric identifier for the asset list to export.
            fobj (FileObject):
                The file-like object to store the asset list XML definition.

        Returns:
            :obj:`FileObject`:
                The file-like object containing the XML definition.

        Examples:
            >>> with open('example.xml', 'wb') as fobj:
            ...     sc.asset_lists.export_definition(1, fobj)
        '''
        resp = self._api.get('asset/{}/export'.format(
            self._check('id', id, int)), stream=True)

        # if no file-like object was passed, then we will instantiate a BytesIO
        # object to push the file into.
        if not fobj:
            fobj = BytesIO()

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        resp.close()
        return fobj

    def refresh(self, id, org_id, *repos):
        '''
        Initiates an on-demand recalculation of the asset list.  Note this
        endpoint requires being logged in as an admin user.

        :sc-api:`asset-list: refresh <Asset.html#AssetRESTReference-/asset/{id}/refresh>`

        Args:
            id (int): The numeric identifier of the asset list to refresh.
            org_id (int): The organization associated to the asset list.
            *repos (int): Repository ids to perform the recalculation on.

        Returns:
            :obj:`dict`:
                Response of the items that the asset list is associated to.

        Examples:
            Perform the refresh against a single repo:

            >>> sc.asset_lists.refresh(1, 1, 1)

            Perform the refresh against many repos:

            >>> sc.asset_lists.refresh(1, 1, 1, 2, 3)
        '''
        return self._api.post('asset/{}/refresh'.format(
            self._check('id', id, int)), json={
                'orgID': self._check('org_id', org_id, int),
                'repIDs': [{'id': self._check('repo:id', i, int)} for i in repos]
            }).json()['response']

    def ldap_query(self, ldap_id, dn, search_string):
        '''
        Performs a LDAP test query on the specified LDAP service configured.

        :sc-api:`asset-list: test-ldap-query <Asset.html#AssetRESTReference-/asset/testLDAPQuery>`

        Args:
            ldap_id (int):
                The numeric identifier for the configured LDAP service.
            dn (str): The valid search base to use.
            search_string(str):
                The search string to query the LDAP service with.

        Returns:
            :obj:`dict`:
                The LDAP response.

        Examples:
            >>> resp = sc.asset_lists.ldap_query(1, 'domain.com', '*')
        '''
        return self._api.post('asset/testLDAPQuery', json={
            'definedLDAPQuery': {
                'searchBase': self._check('dn', dn, str),
                'searchString': self._check('search_string', search_string, str),
                'ldap': {'id': str(self._check('ldap_id', ldap_id, int))}
            }}).json()['response']

    def tags(self):
        '''
        Retrieves the list of unique tags associated to asset lists.

        :sc-api:`asset-lists: tags <Asset.html#AssetRESTReference-/asset/tag>`

        Returns:
            :obj:`list`:
                List of tags

        Examples:
            >>> tags = sc.asset_lists.tags()
        '''
        return self._api.get('asset/tag').json()['response']

    def share(self, id, *groups):
        '''
        Shares the specified asset list to another user group.

        :sc-api:`asset-lists: share <Asset.html#AssetRESTReference-/asset/{id}/share>`

        Args:
            id (int): The numeric id for the credential.
            *groups (int): The numeric id of the group(s) to share to.

        Returns:
            :obj:`dict`:
                The updated asset-list resource.

        Examples:
            >>> sc.asset_lists.share(1, group_1, group_2)
        '''
        return self._api.post('asset/{}/share'.format(
            self._check('id', id, int)), json={
                'groups': [{'id': self._check('group:id', i, int)}
                    for i in groups]}).json()['response']
