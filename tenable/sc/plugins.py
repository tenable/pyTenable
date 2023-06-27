'''
Plugins
=======

The following methods allow for interaction with the Tenable Security Center
:sc-api:`Plugins <Plugin.htm>` API.  These items are typically seen under the
**Plugins** section of Tenable Security Center.

Methods available on ``sc.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginAPI
    :members:
'''
from .base import SCEndpoint, SCResultsIterator
from tenable.errors import UnexpectedValueError


class PluginResultsIterator(SCResultsIterator):
    pass


class PluginAPI(SCEndpoint):
    def _constructor(self, **kwargs):
        '''
        Constructs the plugin query.
        '''

        if 'fields' in kwargs:
            kwargs['fields'] = ','.join([self._check('field', f, str)
                                     for f in self._check('fields', kwargs['fields'], list)])

        if 'filter' in kwargs:
            # break down the filter tuple into the various query parameters
            # that the plugin api expects.
            self._check('filter', kwargs['filter'], tuple)
            if len(kwargs['filter']) != 3:
                raise UnexpectedValueError(
                    'the filter tuple must be name, operator, value.')
            kwargs['filterField'] = self._check('filter:field', kwargs['filter'][0], str)
            kwargs['op'] = self._check('filter:operator', kwargs['filter'][1], str,
                                   choices=['eq', 'gt', 'gte', 'like', 'lt', 'lte'])
            kwargs['value'] = self._check('filter:value', kwargs['filter'][2], str)
            del kwargs['filter']

        if 'sort_field' in kwargs:
            # convert the snake_cased variant of the parameter to the camelCased
            # variant that the API expects to see.
            kwargs['sortField'] = self._check(
                'sort_field', kwargs['sort_field'], str)
            del kwargs['sort_field']

        if 'sort_direction' in kwargs:
            # convert the snake_cased variant of the parameter to the camelCased
            # variant that the API expects to see.
            kwargs['sortDirection'] = self._check(
                'sort_direction', kwargs['sort_direction'], str,
                choices=['ASC', 'DESC'], case='upper')
            del kwargs['sort_direction']

        if 'since' in kwargs:
            # The since parameter should be an integer.
            self._check('since', kwargs['since'], int)

        if 'type' in kwargs:
            # Validate that the plugin type is what's expected.
            self._check('type', kwargs['type'], str, choices=[
                'active', 'all', 'compliance', 'custom',
                'lce', 'notPassive', 'passive'
            ], default='all')

        # While the iterator will handle the offset & limits, a raw json result
        # may be requested instead.
        if 'offset' in kwargs:
            kwargs['startOffset'] = self._check('offset', kwargs['offset'], int)
            del kwargs['offset']

        if 'limit' in kwargs:
            kwargs['endOffset'] = self._check(
                'limit', kwargs['limit'], int) + kwargs.get('startOffset', 0)
            del kwargs['limit']

        # Pages and json_result parameters should be removed from the document
        # if they exist.
        if 'pages' in kwargs:
            del kwargs['pages']

        if 'json_result' in kwargs:
            del kwargs['json_result']

        # Return the modified keyword dict to the caller.
        return kwargs

    def list(self, **kwargs):
        '''
        Retrieves the list of plugins.

        :sc-api:`plugins: list <Plugin.htm#PluginRESTReference-/plugin>`

        Args:
            fields (list, optional):
                A list of attributes to return.
            filter (tuple, optional):
                A filter tuple for which to filter the plugins.  Filter tuples
                must be ``('name', 'operator', 'value')`` and follow a similar
                yet different format to the analysis filters.
            limit (int, optional):
                How many records should be returned in each page of data.  If
                none is specified, the default is 1000 records.
            offset (int, optional):
                At what offset within the data should we start returning data.
                If none is specified, the default is 0.
            pages (int, optional):
                How many pages of data should we return.  If none is specified
                then all pages will return.
            sort_field (str, optional):
                The field to sort the results on.
            sort_direction (str, optional):
                The direction in which to sort the results.  Valid settings are
                ``asc`` and ``desc``.  The default is ``asc``.
            type (str, optional):
                The type of plugins to return.  Available types are ``active``,
                ``all``, ``compliance``, ``custom``, ``lce``, ``notPassive``, and
                ``passive``.  If nothing is specified, then ``all`` is assumed.

        Returns:
            PluginResultsIterator: an iterator object handling data pagination.

        Examples:
            To retrieve all of the plugins, you'll simply need to call the list
            method like so:

            >>> plugins = sc.plugins.list()
            >>> for plugin in plugins:
            ...     pprint(plugin)

            If you only want the plugins with java in the name, you'd run a
            query similar to this one:

            >>> plugins = sc.plugins.list(
            ...     filter=('name', 'like', 'java'))

            For just the active plugins, we'd run:

            >>> plugins = sc.plugins.list(type='active')
        '''
        offset = self._check('offset', kwargs.get('offset', 0), int)
        limit = self._check('limit', kwargs.get('limit', 1000), int)
        pages = self._check('pages', kwargs.get('pages'), int)
        json_result = kwargs.get('json_result', False)
        query = self._constructor(**kwargs)

        if json_result:
            return self._api.get('plugin', params=query).json()['response']
        return PluginResultsIterator(self._api,
                                         _resource='plugin',
                                         _offset=offset,
                                         _limit=limit,
                                         _query=query,
                                         _pages_total=pages)

    def details(self, plugin_id, fields=None):
        '''
        Returns the details for a specific plugin.

        :sc-api:`plugins: details <Plugin.htm#PluginRESTReference-/plugin/{id}>`

        Args:
            plugin_id (int): The identifier for the plugin.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: The plugin resource record.

        Examples:
            >>> plugin = sc.plugins.detail(19506)
            >>> pprint(plugin)
       '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('plugin/{}'.format(self._check('plugin_id', plugin_id, int)),
                             params=params).json()['response']

    def family_list(self, **kwargs):
        '''
        Returns the list of plugin families.

        :sc-api:`plugin-families: list <Plugin-Family.htm#PluginFamilyRESTReference-/pluginFamily>`

        Args:
            fields (list, optional):
                A list of attributes to return.
            filter (tuple, optional):
                A filter tuple for which to filter the plugins.  Filter tuples
                must be ``('name', 'operator', 'value')`` and follow a similar
                yet different format to the analysis filters.
            sort_field (str, optional):
                The field to sort the results on.
            sort_direction (str, optional):
                The direction in which to sort the results.  Valid settings are
                ``asc`` and ``desc``.  The default is ``asc``.
            type (str, optional):
                The type of plugins to return.  Available types are ``active``,
                ``all``, ``compliance``, ``custom``, ``lce``, ``notPassive``, and
                ``passive``.  If nothing is specified, then ``all`` is assumed.

        Returns:
            :obj:`list`:
                List of plugin family records.

        Examples:
            >>> for fam in sc.plugins.family_list():
            ...     pprint(fam)
        '''
        query = self._constructor(**kwargs)
        return self._api.get('pluginFamily', params=query).json()['response']

    def family_details(self, plugin_id, fields=None):
        '''
        Returns the details for the specified plugin family.

        :sc-api:`plugin-family: details <Plugin-Family.htm#PluginFamilyRESTReference-/pluginFamily/{id}>`

        Args:
            plugin_id (int): The plugin family numeric identifier.
            fields (list, optional):
                A list of attributes to return.

        Returns:
            :obj:`dict`:
                The plugin family resource.

        Examples:
            >>> family = sc.plugins.family_details(10)
            >>> pprint(family)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str)
                                         for f in fields])

        return self._api.get('pluginFamily/{}'.format(self._check('plugin_id', plugin_id, int)), params=params).json()['response']

    def family_plugins(self, plugin_id, **kwargs):
        '''
        Retrieves the plugins for the specified family.

        :sc-api:`plugin-family: plugins <Plugin-Family.htm#PluginFamilyRESTReference-/pluginFamily/{id}/plugins::GET>`

        Args:
            plugin_id (int): The numeric identifier for the plugin family.
            fields (list, optional):
                A list of attributes to return.
            filter (tuple, optional):
                A filter tuple for which to filter the plugins.  Filter tuples
                must be ``('name', 'operator', 'value')`` and follow a similar
                yet different format to the analysis filters.
            limit (int, optional):
                How many records should be returned in each page of data.  If
                none is specified, the default is 1000 records.
            offset (int, optional):
                At what offset within the data should we start returning data.
                If none is specified, the default is 0.
            pages (int, optional):
                How many pages of data should we return.  If none is specified
                then all pages will return.
            sort_field (str, optional):
                The field to sort the results on.
            sort_direction (str, optional):
                The direction in which to sort the results.  Valid settings are
                ``asc`` and ``desc``.  The default is ``asc``.
            type (str, optional):
                The type of plugins to return.  Available types are ``active``,
                ``all``, ``compliance``, ``custom``, ``lce``, ``notPassive``, and
                ``passive``.  If nothing is specified, then ``all`` is assumed.

        Returns:
            PluginResultsIterator: an iterator object handling data pagination.

        Examples:
            >>> plugins = sc.plugins.family_plugins(10)
            >>> for plugin in plugins:
            ...     pprint(plugin)
        '''
        offset = self._check('offset', kwargs.get('offset', 0), int)
        limit = self._check('limit', kwargs.get('limit', 1000), int)
        pages = self._check('pages', kwargs.get('pages'), int)
        json_result = kwargs.get('json_result', False)
        query = self._constructor(**kwargs)

        if json_result:
            return self._api.get('plugin', params=query).json()['response']
        return PluginResultsIterator(self._api,
                                         _resource='pluginFamily/{}/plugins'.format(
                                             self._check('plugin_id', plugin_id, int)),
                                         _offset=offset,
                                         _limit=limit,
                                         _query=query,
                                         _pages_total=pages)
