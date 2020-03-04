'''
queries
=======

The following methods allow for interaction into the Tenable.sc
:sc-api:`Query <Query.html>` API.  These items are typically seen
under the **Workflow -> Query** section of Tenable.sc.

Methods available on ``sc.queries``:

.. rst-class:: hide-signature
.. autoclass:: QueryAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: share
    .. automethod:: tags
'''
from .base import SCEndpoint
from tenable.utils import dict_merge

class QueryAPI(SCEndpoint):
    def _constructor(self, *filters, **kw):
        '''
        Handles parsing the keywords and returns a query definition document
        '''
        query = self._query_constructor(*filters, **kw)
        kw = dict_merge(kw, query.get('query', dict()))

        if 'name' in kw:
            self._check('name', kw['name'], str)

        if 'description' in kw:
            self._check('description', kw['description'], str)

        if 'tags' in kw:
            self._check('tags', kw['tags'], str)

        if 'sort_field' in kw:
            kw['sortField'] = self._check(
                'sort_field', kw['sort_field'], str)
            del(kw['sort_field'])

        if 'sort_direction' in kw:
            kw['sortDir'] = self._check(
                'sort_direction', kw['sort_direction'], str,
                choices=['ASC', 'DESC'], case='upper')
            del(kw['sort_direction'])

        if 'offset' in kw:
            kw['startOffset'] = self._check('offset', kw['offset'], int)
            del(kw['offset'])

        if 'limit' in kw:
            kw['endOffset'] = self._check('limit', kw['limit'], int)
            del(kw['limit'])

        if 'owner_id' in kw:
            kw['ownerID'] = str(self._check(
                'owner_id', kw['owner_id'], int))
            del(kw['owner_id'])

        if 'context' in kw:
            self._check('context', kw['context'], str)

        if 'browse_cols' in kw:
            kw['browseColumns'] = ','.join(self._check(
                'browse_cols', kw['browse_cols'], list))
            del(kw['browse_cols'])

        if 'browse_sort_col' in kw:
            kw['browseSortColumn'] = self._check(
                'browse_sort_col', kw['browse_sort_col'], str)
            del(kw['browse_sort_col'])

        if 'browse_sort_direction' in kw:
            kw['browseSortDirection'] = self._check(
                'browse_sort_direction', kw['browse_sort_direction'],
                str, case='upper', choices=['ASC', 'DESC'])
            del(kw['browse_sort_direction'])

        return kw


    def create(self, name, tool, data_type, *filters, **kw):
        '''
        Creates a query.

        :sc-api:`query: create <Query.html#query_POST>`

        Args:
            name (str):
                The name of the new query
            tool (str):
                The tool to use to query the data.
            data_type (str):
                The type of data to query.
            *filters (tuple, optional):
                The filters to use for the query.  Refer to the documentation
                within the :ref:'tenable.sc.analysis' for more information on
                how to construct these.
            browse_cols (list, optional):
                What columns are set to be browsable for the analysis view.
            browse_sort_col (str, optional):
                The browsable column in which to sort on.
            browse_sort_dir (str, optional):
                The direction in which to sort.  Valid values are ``asc`` and
                ``desc``.
            description (str, optional):
                The description for the query.
            limit (int, optional):
                The limit to the number of records to return.  If nothing is
                specified, the API defaults to 100 records.
            offset (int, optional):
                The number of records to skip before returning results.  If
                nothing is specified, then the default is 0.
            owner_id (int, optional):
                The identifier stating the owner of the query.  If left
                unspecified, then the default is the current user.
            sort_direction (str, optional):
                The direction in which to sort.  Valid values are ``asc`` and
                ``desc``.
            sort_field (str, optional):
                The field in which to sort the results.
            tags (str, optional):
                Tags definition for the query.

        Returns:
            :obj:`dict`:
                The newly created query.

        Examples:
            >>> query = sc.queries.create('New Query', 'vulndetails', 'vuln',
            ...     ('pluginID', '=', '19506'))
        '''
        kw['name'] = name
        kw['tool'] = tool
        kw['type'] = data_type
        payload = self._constructor(*filters, **kw)
        return self._api.post('query', json=payload).json()['response']

    def details(self, id, fields=None):
        '''
        Returns the details for a specific query.

        :sc-api:`query: details <Query.html#QueryRESTReference-/query/{id}>`

        Args:
            id (int): The identifier for the query.
            fields (list, optional): A list of attributes to return.

        Returns:
            :obj:`dict`:
                The query resource record.

        Examples:
            >>> query = sc.queries.details(1)
            >>> pprint(query)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('query/{}'.format(self._check('id', id, int)),
            params=params).json()['response']

    def edit(self, id, *filters, **kw):
        '''
        Edits a query.

        :sc-api:`query: edit <Query.html#query_id_PATCH>`

        Args:
            *filters (tuple, optional):
                The filters to use for the query.  Refer to the documentation
                within the :ref:'tenable.sc.analysis' for more information on
                how to construct these.
            browse_cols (str, optional):
                What columns are set to be browsable for the analysis view.
            browse_sort_col (list, optional):
                The browsable column in which to sort on.
            browse_sort_dir (str, optional):
                The direction in which to sort.  Valid values are ``asc`` and
                ``desc``.
            description (str, optional):
                The description for the query.
            limit (int, optional):
                The limit to the number of records to return.  If nothing is
                specified, the API defaults to 100 records.
            name (str, optional):
                The name of the new query
            offset (int, optional):
                The number of records to skip before returning results.  If
                nothing is specified, then the default is 0.
            owner_id (int, optional):
                The identifier stating the owner of the query.  If left
                unspecified, then the default is the current user.
            sort_direction (str, optional):
                The direction in which to sort.  Valid values are ``asc`` and
                ``desc``.
            sort_field (str, optional):
                The field in which to sort the results.
            tags (str, optional):
                Tags definition for the query.
            tool (str, optional):
                The tool to use to query the data.
            type (str, optional):
                The type of data to query.
        Returns:
           :obj:` dict`:
                The newly updated query.

        Examples:
            >>> query = sc.queries.edit()
        '''
        payload = self._constructor(*filters, **kw)
        return self._api.patch('query/{}'.format(
            self._check('id', id, int)), json=payload).json()['response']

    def delete(self, id):
        '''
        Removes a query.

        :sc-api:`query: delete <Query.html#query_id_DELETE>`

        Args:
            id (int): The numeric identifier for the query to remove.

        Returns:
            :obj:`str`:
                An empty response.

        Examples:
            >>> sc.queries.delete(1)
        '''
        return self._api.delete('query/{}'.format(
            self._check('id', id, int))).json()['response']

    def list(self, fields=None):
        '''
        Retrieves the list of query definitions.

        :sc-api:`query: list <Query.html#QueryRESTReference-/query>`

        Args:
            fields (list, optional):
                A list of attributes to return for each query.

        Returns:
            :obj:`list`:
                A list of query resources.

        Examples:
            >>> for query in sc.queries.list():
            ...     pprint(query)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                for f in fields])

        return self._api.get('query', params=params).json()['response']

    def share(self, id, *groups):
        '''
        Shares the specified query to another user group.

        :sc-api:`query: share <Query.html#QueryRESTReference-/query/{id}/share>`

        Args:
            id (int): The numeric id for the query.
            *groups (int): The numeric id of the group(s) to share to.

        Returns:
            :obj:`dict`:
                The updated query resource.

        Examples:
            >>> sc.queries.share(1, group_1, group_2)
        '''
        return self._api.post('query/{}/share'.format(
            self._check('id', id, int)), json={
                'groups': [{'id': self._check('group:id', i, int)}
                    for i in groups]}).json()['response']

    def tags(self):
        '''
        Retrieves the list of unique tags associated to queries.

        :sc-api:`query: tags <Query.html#QueryRESTReference-/query/tag>`

        Returns:
            :obj:`list`:
                List of tags

        Examples:
            >>> tags = sc.queries.tags()
        '''
        return self._api.get('query/tag').json()['response']