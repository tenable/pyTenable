'''
credentials
===========

The following methods allow for interaction into the Tenable.io
:devportal:`credentials <credentials>` API endpoints.

Methods available on ``tio.credentials``:

.. rst-class:: hide-signature
.. autoclass:: CredentialsAPI

    .. automethod:: create
    .. automethod:: delete
    .. automethod:: details
    .. automethod:: edit
    .. automethod:: list
    .. automethod:: types
    .. automethod:: upload
'''
from tenable.utils import dict_merge
from .base import TIOEndpoint, TIOIterator

class CredentialsIterator(TIOIterator):
    '''
    The credentials iterator provides a scalable way to work through networks
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

class CredentialsAPI(TIOEndpoint):
    def _permissions_constructor(self, permissions):
        '''
        Validates and/or transforms thew permissions items into the desired
        format.  If a dict it will validate.  If a tuple, will convert.
        '''
        resp = list()
        for p in permissions:
            if isinstance(p, tuple):
                # if the item is a tuple, lets validate it and convert it into
                # the dictionary format the API expects
                ptnx = {
                    32: 32,
                    64: 64,
                    'use': 32,
                    'edit': 64,
                }
                resp.append({
                    'type': self._check('permission:type', p[0], str,
                        choices=['user', 'group']),
                    'permissions': ptnx[self._check('permissions:permission',
                        p[1], (str, int), choices=[32, 64, 'use', 'edit'])],
                    'grantee_uuid': self._check('permission:uuid', p[2], 'uuid')
                })

            elif isinstance(p, dict) :
                # if the item is a dictionary, validate it and then pass into
                # the response list.
                self._check('permission:type', p['type'], str,
                    choices=['user', 'group'])
                self._check('permission:permissions', p['permissions'], int,
                    choices=[32, 64])
                self._check('permission:grantee_uuid', p['grantee_uuid'], 'uuid')
                resp.append(p)

            else :
                raise TypeError('permission object is not tuple or dict type')
        return resp


    def create(self, cred_name, cred_type, description=None,
               permissions=None, **settings):
        '''
        Creates a new managed credential.

        :devportal:`credentials: create <credentials-create>`

        Args:
            cred_name (str):
                The name of the credential.
            cred_type (str):
                The type of credential to create.  For a list of values refer to
                the output of the :py:meth:`types() <CredentialsAPI.types>`
                method.
            description (str, optional):
                A description for the credential.
            permissions (list, optional):
                A list of permissions (in either tuple or native dict format)
                detailing whom is allowed to use or edit this credential set.
                For the dictionary format, refer to the API docs.  The tuple
                format uses the customary ``(type, perm, uuid)`` format.

                Examples:
                    - ``('user', 32, user_uuid)``
                    - ``('group', 32, group_uuid)``
                    - ``('user', 'use', user_uuid)``

            **settings (dict, optional):
                Additional keywords passed will be added to the settings dict
                within the API call.  As this dataset can be highly variable,
                it will not be validated and simply passed as-is.

        Returns:
            :obj:`str`:
                The UUID of the newly created credential.

        Examples:
            >>> group_id = '00000000-0000-0000-0000-000000000000'
            >>> tio.credentials.create('SSH Account', 'SSH',
            ...     permissions=[('group', 'use', group_id)],
            ...     username='user1',
            ...     password='sekretsquirrel',
            ...     escalation_account='root',
            ...     escalation_password='sudopassword',
            ...     elevate_privileges_with='sudo',
            ...     bin_directory='/usr/bin',
            ...     custom_password_prompt='')
        '''
        if not permissions:
            permissions = list()

        return self._api.post('credentials', json={
            'name': self._check('cred_name', cred_name, str),
            'description': self._check('description', description, str, default=''),
            'type': self._check('cred_type', cred_type, str),
            'settings': settings,
            'permissions': self._permissions_constructor(permissions)
        }).json()['uuid']

    def edit(self, cred_uuid, cred_name=None, description=None,
             permissions=None, ad_hoc=None, **settings):
        '''
        Creates a new managed credential.

        :devportal:`credentials: create <credentials-create>`

        Args:
            ad_hoc (bool, optional):
                Determines whether the credential is managed (``False``) or an
                embedded credential in a scan or policy (``True``).
            cred_name (str, optional):
                The name of the credential.
            description (str, optional):
                A description for the credential.
            permissions (list, optional):
                A list of permissions (in either tuple or native dict format)
                detailing whom is allowed to use or edit this credential set.
                For the dictionary format, refer to the API docs.  The tuple
                format uses the customary ``(type, perm, uuid)`` format.

                Examples:
                    - ``('user', 32, user_uuid)``
                    - ``('group', 32, group_uuid)``
                    - ``('user', 'use', user_uuid)``

            **settings (dict, optional):
                Additional keywords passed will be added to the settings dict
                within the API call.  As this dataset can be highly variable,
                it will not be validated and simply passed as-is.

        Returns:
            :obj:`bool`:
                The status of the update process.

        Examples:
            >>> cred_uuid = '00000000-0000-0000-0000-000000000000'
            >>> tio.credentials.edit(cred_uuid,
            ...     password='sekretsquirrel',
            ...     escalation_password='sudopassword')
        '''
        current = self.details(cred_uuid)

        payload = {
            'name': self._check('cred_name', cred_name, str,
                default=current['name']),
            'description': self._check('description', description, str,
                default=current['description']),
            'ad_hoc': self._check('ad_hoc', ad_hoc, bool,
                default=current['ad_hoc']),
        }
        if permissions:
            payload['permissions'] = self._permissions_constructor(permissions)
        payload['settings'] = dict_merge(current['settings'], settings)

        return self._api.put('credentials/{}'.format(cred_uuid),
            json=payload).json()['updated']

    def details(self, id):
        '''
        Retrieves the details of the specified credential.

        :devportal:`credentials: details <credentials-details>`

        Args:
            id (str): The UUID of the credential to retrieve.

        Returns:
            :obj:`dict`:
                The resource record for the credential.

        Examples:
            >>> cred_uuid = '00000000-0000-0000-0000-000000000000'
            >>> cred = tio.credentials.details(cred_uuid)
        '''
        return self._api.get('credentials/{}'.format(
            self._check('id', id, 'uuid'))).json()

    def delete(self, id):
        '''
        Deletes the specified credential.

        :devportal:`credentials: delete <credentials-delete>`

        Args:
            id (str): The UUID of the credential to retrieve.

        Returns:
            :obj:`bool`:
                The status of the action.

        Examples:
            >>> cred_uuid = '00000000-0000-0000-0000-000000000000'
            >>> cred = tio.credentials.delete(cred_uuid)
        '''
        return self._api.delete('credentials/{}'.format(
            self._check('id', id, 'uuid'))).json()['deleted']

    def types(self):
        '''
        Lists all of the available credential types.

        :devportal:`credentials: list-types <credentials-list-credential-types>`

        Returns:
            :obj:`list`:
                A list of the available credential types and definitions.

        Examples:
            >>> cred_types = tio.credentials.types()
        '''
        return self._api.get('credentials/types').json()['credentials']

    def list(self, *filters, **kw):
        '''
        Get the listing of configured credentials from Tenable.io.

        :devportal:`credentials: list <credentials-list>`

        Args:
            *filters (tuple, optional):
                Filters are tuples in the form of ('NAME', 'OPERATOR', 'VALUE').
                Multiple filters can be used and will filter down the data being
                returned from the API.

                Examples:
                    - ``('name', 'eq', 'example')``

                As the filters may change and sortable fields may change over
                time, it's highly recommended that you look at the output of
                the :py:meth:`tio.filters.networks_filters() <FiltersAPI.networks_filters>`
                endpoint to get more details.
            filter_type (str, optional):
                The filter_type operator determines how the filters are combined
                together.  ``and`` will inform the API that all of the filter
                conditions must be met for an access group to be returned,
                whereas ``or`` would mean that if any of the conditions are met,
                the access group record will be returned.
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            offset (int, optional):
                The starting record to retrieve.  Default is 0.
            owner_uuid (str, optional):
                The UUID of the scan owner.  If specified it will limit the
                responses to credentials assigned to scans owned by the
                specified user UUID.
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.
            wildcard (str, optional):
                A string to pattern match against all available fields returned.
            wildcard_fields (list, optional):
                A list of fields to optionally restrict the wild-card matching
                to.

        Returns:
            :obj:`CredentialsIterator`:
                An iterator that handles the page management of the requested
                records.

        Examples:
            >>> for cred in tio.credentials.list():
            ...     pprint(cred)
        '''
        limit = 50
        offset = 0
        pages = None
        query = self._parse_filters(filters,
            self._api.filters.networks_filters(), rtype='colon')

        # If a referrer owner uuid is passed, then add it to the query.
        if 'owner_uuid' in kw and self._check('owner_uuid', kw['owner_uuid'], 'uuid'):
            query['referrer_owner_uuid'] = kw['owner_uuid']

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

        # Return the Iterator.
        return CredentialsIterator(self._api,
            _limit=limit,
            _offset=offset,
            _pages_total=pages,
            _query=query,
            _path='credentials',
            _resource='credentials'
        )

    def upload(self, fobj):
        '''
        Uploads a file for use with a managed credential.

        :devportal:`credentials: upload <file-upload>`

        Args:
            fobj (FileObject):
                The file object intended to be uploaded into Tenable.io.

        Returns:
            :obj:`str`:
                The fileuploaded attribute
        '''

        # We will attempt to discover the name of the file stored within the
        # file object.  If the name of the file is successfully discovered, we
        # will generate a random uuid string and append it to the name.
        # Otherwise, we will generate a random uuid string to use instead.
        kw = {
            'files': {
                'Filedata': fobj
            }
        }

        return self._api.post('credentials/files', **kw).json()['fileuploaded']
