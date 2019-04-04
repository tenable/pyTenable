'''
plugins
=======

The following methods allow for interaction with the Tenable.sc
`Repositories <https://docs.tenable.com/sccv/api/Plugin.html>`_ API.  These
items are typically seen under the **Plugins** section of Tenable.sc. 

Methods available on ``sc.plugins``:

.. rst-class:: hide-signature
.. autoclass:: PluginAPI

    .. automethod:: list
    .. automethod:: details
'''
from .base import SCEndpoint, SCResultsIterator
from tenable.errors import UnexpectedValueError

class PluginResultsIterator(SCResultsIterator):
    def _get_page(self):
        '''
        Retreives the next page of results when the current page has been
        exhausted.
        '''
        # First we need to see if there is a page limit and if there is, have
        # we run into that limit.  If we have, then return a StopIteration
        # exception.
        if self._pages_total and self._pages_requested >= self._pages_total:
            raise StopIteration()

        # Now we need to do is construct the query with the current offset 
        # and limits
        query = self._query
        query['startOffset'] = self._offset
        query['endOffset'] = self._limit + self._offset

        # Lets actually call the API for the data at this point.
        resp = self._api.get('plugin', params=query).json()

        # Now that we have the response, lets reset any counters we need to, 
        # and increment things like the page counter, offset, etc.
        self.page_count = 0
        self._pages_requested += 1
        self._offset += self._limit
        self._raw = resp
        self.page = resp['response']

        # As no total is returned via the API, we will simply need to re-compute
        # the total to be N+1 every page as long as the page of data is equal to
        # the limit.  If we ever get a page of data that is less than the limit,
        # then we will set the total to be the count + page length.
        if len(resp['response']) < self._limit:
            self.total = self.count + len(resp['response'])
        else:
            self.total = self.count + self._limit + 1


class PluginAPI(SCEndpoint):
    def _constructor(self, **kw):
        '''
        Constructs the plugin query.
        '''

        if 'fields' in kw:
            kw['fields'] = ','.join([self._check('field', f, str) 
                for f in self._check('fields', kw['fields'], list)])

        if 'filter' in kw: 
            # break down the filter tuple into the various query parameters
            # that the plugin api expects.
            self._check('filter', kw['filter'], tuple)
            if len(kw['filter']) != 3:
                raise UnexpectedValueError(
                    'the filter tuple must be name, operator, value.')
            kw['filterField'] = self._check('filter:field', kw['filter'][0], str)
            kw['op'] = self._check('filter:operator', kw['filter'][1], str, 
                choices=['eq', 'gt', 'gte', 'like', 'lt', 'lte'])
            kw['value'] = self._check('filter:value', kw['filter'][2], str)
            del(kw['filter'])
        
        if 'sort_field' in kw:
            # convert the snake_cased variant of the parameter to the camelCased
            # variant that the API expects to see.
            kw['sortField'] = self._check(
                'sort_field', kw['sort_field'], str)
            del(kw['sort_field'])
        
        if 'sort_direction' in kw:
            # convert the snake_cased variant of the parameter to the camelCased
            # variant that the API expects to see.
            kw['sortDirection'] = self._check(
                'sort_direction', kw['sort_direction'], str, 
                choices=['ASC', 'DESC'], case='upper')
            del(kw['sort_direction'])
        
        if 'since' in kw:
            # The since parameter should be an integer.
            self._check('since', kw['since'], int)
        
        if 'type' in kw:
            # Validate that the plugin type is whats expected.
            self._check('type', kw['type'], str, choices=[
                    'active', 'all', 'compliance', 'custom', 
                    'lce', 'notPassive', 'passive'
                ], default='all')
        

        # While the iterator will handle the offset & limits, a raw json result
        # may be requested instead.
        if 'offset' in kw:
            kw['startOffset'] = self._check('offset', kw['offset'], int)
            del(kw['offset'])
        
        if 'limit' in kw:
            kw['endOffset'] = self._check(
                'limit', kw['limit'], int) + kw.get('startOffset', 0)
            del(kw['limit'])
        
        # Pages and json_result paramaters should be removed from the document
        # if they exist.
        if 'pages' in kw:
            del(kw['pages'])
        
        if 'json_result' in kw:
            del(kw['json_result'])
        
        # Return the modified keyword dict to the caller.
        return kw

    def list(self, **kw):
        '''
        Retrieves the list of plugins.

        + `SC Plugin List <https://docs.tenable.com/sccv/api/Plugin.html#PluginRESTReference-/plugin>`_

        Args:
            fields (list, optional): 
                A list of attributes to return.
            filter (tuple, optional):
                A filter tuple for which to filter the plugins.  Filter tuples 
                must be ``('name', 'operator', 'value')`` and follow a similar
                yet different format to the analysis filters.
            limit (int, optional):
                How many records should be returned in each page of data.  If
                none is specified, the default is 200 records.
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
        offset = self._check('offset', kw.get('offset', 0), int)
        limit = self._check('limit', kw.get('limit', 200), int)
        pages = self._check('pages', kw.get('pages'), int)
        json_result = kw.get('json_result', False)
        query = self._constructor(**kw)

        if json_result:
            return self._api.get('plugin', params=query).json()['response']
        else:
            return PluginResultsIterator(self._api,
                _offset=offset,
                _limit=limit,
                _query=query,
                _pages_total=pages)
    
    def details(self, id, fields=None):
        '''
        Returns the details for a specific plugin.

        + `SC Plugin Details <https://docs.tenable.com/sccv/api/Plugin.html#PluginRESTReference-/plugin/{id}>`_

        Args:
            id (int): The identifier for the plugin.
            fields (list, optional): A list of attributes to return.

        Returns:
            dict: The plugin resource record.

        Examples:
            >>> plugin = sc.alerts.detail(19506)
            >>> pprint(plugin)
        '''
        params = dict()
        if fields:
            params['fields'] = ','.join([self._check('field', f, str) for f in fields])

        return self._api.get('plugin/{}'.format(self._check('id', id, int)),
            params=params).json()['response']