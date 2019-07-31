'''
networks
========

The following methods allow for interaction into the Tenable.io
:devportal:`networks <networks>` API endpoints.

Methods available on ``tio.networks``:

.. rst-class:: hide-signature
.. autoclass:: NetworksAPI

    .. automethod:: assign_scanners
    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: list_scanners
    .. automethod:: unassigned_scanners
'''
from .base import TIOEndpoint, TIOIterator

class NetworksIterator(TIOIterator):
    '''
    The networks iterator provides a scalable way to work through networks
    result sets of any size.  The iterator will walk through each page of data,
    returning one record at a time.  If it reaches the end of a page of records,
    then it will request the next page of information and then continue to
    return records from the next page (and the next, and the next) until the
    counter reaches the total number of records that the API has reported.

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

class NetworksAPI(TIOEndpoint):
    def create(self, name, description=None):
        '''
        Creates a new network within Tenable.io

        :devportal:`networks: create <networks-create>`

        Args:
            name (str): The name of the new network.
            description (str, optional): Description of the network.

        Returns:
            :obj:`dict`:
                The resource record of the newly created network.

        Examples:
            >>> nw = tio.networks.create('Example')
        '''
        if not description:
            description = ''

        return self._api.post('networks', json={
            'name': self._check('name', name, str),
            'description': self._check('description', description, str)
        }).json()

    def delete(self, id):
        '''
        Deletes the specified network.

        :devportal:`networks: delete <networks-delete>`

        Args:
            id (str): The UUID of the network to remove.

        Examples:
            >>> tio.networks.delete('00000000-0000-0000-0000-000000000000')
        '''
        self._api.delete('networks/{}'.format(self._check('id', id, 'uuid')))

    def details(self, id):
        '''
        Retreives the details of the specified network.

        :devportal:`networks: details <networks-details>`

        Args:
            id (str): The UUID of the network.

        Examples:
            >>> nw = tio.networks.details('00000000-0000-0000-0000-000000000000')
        '''
        return self._api.get('networks/{}'.format(
            self._check('id', id, 'uuid'))).json()

    def edit(self, id, name, description=None):
        '''
        Updates the specified network resource.

        :devportal:`networks: update <networks-update>`

        Args:
            id (str): The UUID of the network resource to update.
            name (str): The new name of the network resource.
            description (str, optional):
                The new description of the network resource.

        Returns:
            :obj:`dict`:
                The updates network resource.

        Examples:
            >>> nw = tio.networks.edit('00000000-0000-0000-0000-000000000000',
            ...     'Updated Network', 'Updated Description')
        '''
        if not description:
            description = ''

        return self._api.put('networks/{}'.format(self._check('id', id, 'uuid')),
            json={
                'name': self._check('name', name, str),
                'description': self._check('description', description, str)
            }).json()

    def assign_scanners(self, id, *scanner_uuids):
        '''
        Assigns one or many scanners to a network.

        :devportal:`networks: assign-scanner <networks-assign-scanner>`
        :devportal:`networks: bulk-assign-scanner <networks-assign-scanner-bulk>`

        Args:
            id (str): The UUID of the network.
            *scanner_uuids (str): Scanner UUID(s) to assign to the network.

        Examples:
            Assign a single scanner:

            >>> tio.networks,assign_scanners(
            ...     '00000000-0000-0000-0000-000000000000', # Network UUID
            ...     '00000000-0000-0000-0000-000000000000') # Scanner UUID

            Assign multiple scanners:

            >>> tio.networks,assign_scanners(
            ...     '00000000-0000-0000-0000-000000000000', # Network UUID
            ...     '00000000-0000-0000-0000-000000000000', # Scanner1 UUID
            ...     '00000000-0000-0000-0000-000000000000') # Scanner2 UUID
        '''
        if len(scanner_uuids) == 1:
            self._api.post('networks/{}/scanners/{}'.format(
                self._check('id', id, 'uuid'),
                self._check('scanner_uuid', scanner_uuids[0], 'scanner-uuid')
            ))
        elif len(scanner_uuids) > 1:
            self._api.post('networks/{}/scanners'.format(
                self._check('id', id, 'uuid')),
                    json={'scanner_uuids': [self._check('scanner_uuid', i, 'scanner-uuid')
                        for i in scanner_uuids]})
        else:
            raise UnexpectedValueError('No scanner_uuids were supplied.')

    def list_scanners(self, id):
        '''
        Retreives the list of scanners associated to a given network.

        :devportal:`networks: list-scanners <networks-list-scanners>`

        Args:
            id (str): The UUID of the network.

        Returns:
            :obj:`list`:
                List of scanner resources associated to this network.

        Examples:
            >>> network = '00000000-0000-0000-0000-000000000000'
            >>> for scanner in tio.networks.list_scanners(network):
            ...     pprint(scanner)
        '''
        return self._api.get('networks/{}/scanners'.format(
            self._check('id', id, 'uuid'))).json()['scanners']

    def unassigned_scanners(self, id):
        '''
        Retrives the list of scanners that are currently unassigned to the given
        network.  This will include scanners and scanner groups that are
        currently assigned to the default network.

        :devportal:`networks: list-assignable-scanners <networks-list-assignable-scanners>`

        Args:
            id (str): The UUID of the network.

        Returns:
            :obj:`list`:
                The list of unassigned scanner resources

        Examples:
            >>> network = '00000000-0000-0000-0000-000000000000'
            >>> for scanner in tio.networks.unassigned_scanners(network):
            ...     pprint(scanner)
        '''
        return self._api.get('networks/{}/assignable-scanners'.format(
            self._check('id', id, 'uuid'))).json()['scanners']

    def list(self, *filters, **kw):
        '''
        Get the listing of configured networks from Tenable.io.

        :devportal:`networks: list <networks-list>`

        Args:
            *filters (tuple, optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('name', 'eq', 'example')``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.networks.network_filters() <FiltersAPI.networks_filters>`
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met for an access group to be returned,
                whereas ``or`` would mean that if any of the conditions are met,
                the access group record will be returned.
            include_deleted (bool, optional):
                Indicates whether deleted network objects should be included in
                the response.  If left unspecified, the default is ``False``.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.
            wildcard (str, optional):
                A string to pattern match against all available fields returned.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`NetworksIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            Getting the listing of all agents:

            >>> for nw in tio.networks.list():
            ...     pprint(nw)

            Retrieving all of the windows agents:

            >>> for nw in tio.access_groups.list(('name', 'match', 'win')):
            ...     pprint(nw)
        '''
        limit = 50
        offset = 0
        pages = None
        query = self._parse_filters(filters,
            self._api.filters.networks_filters(), rtype='colon')

        # If the offset was set to something other than the default starting
        # point of 0, then we will update offset to reflect that.
        if 'offset' in kw and self._check('offset', kw['offset'], int):
            offset = kw['offset']

        # The limit parameter affects how many records at a time we will pull
        # from the API.  The default in the API is set to 50, however we can
        # pull any variable amount.
        if 'limit' in kw and self._check('limit', kw['limit'], int):
            limit = kw['limit']

        # For the sorting fields, we are converting the tuple that has been
        # provided to us and converting it into a comma-delimited string with
        # each field being represented with its sorting order.  e.g. If we are
        # presented with the following:
        #
        #   sort=(('field1', 'asc'), ('field2', 'desc'))
        #
        # we will generate the following string:
        #
        #   sort=field1:asc,field2:desc
        #
        if 'sort' in kw and self._check('sort', kw['sort'], tuple):
            query['sort'] = ','.join(['{}:{}'.format(
                self._check('sort_field', i[0], str),
                self._check('sort_direction', i[1], str, choices=['asc', 'desc'])
            ) for i in kw['sort']])

        # The filter_type determines how the filters are combined together.
        # The default is 'and', however you can always explicitly define 'and'
        # or 'or'.
        if 'filter_type' in kw and self._check(
            'filter_type', kw['filter_type'], str, choices=['and', 'or']):
            query['ft'] = kw['filter_type']

        # The wild-card filter text refers to how the API will pattern match
        # within all fields, or specific fields using the wildcard_fields param.
        if 'wildcard' in kw and self._check('wildcard', kw['wildcard'], str):
            query['w'] = kw['wildcard']

        # The wildcard_fields parameter allows the user to restrict the fields
        # that the wild-card pattern match pertains to.
        if 'wildcard_fields' in kw and self._check(
            'wildcard_fields', kw['wildcard_fields'], list):
            query['wf'] = ','.join(kw['wildcard_fields'])

        if 'include_deleted' in kw and self._check(
            'include_deleted', kw['include_deleted'], bool):
            query['includeDeleted'] = kw['include_deleted']

        # Return the Iterator.
        return NetworksIterator(self._api,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
            _query=query,
            _path='networks',
            _resource='networks'
        )

