'''
Logos
=====

The following methods allow for interaction into the Tenable.io
:devportal:`Managed Security Service Provider v3 logos
<io-mssp-logos>` API.

Methods available on ``tio.v3.mssp.logos``:

.. rst-class:: hide-signature
.. autoclass:: LogosAPI
    :members:
'''
from io import BytesIO
from typing import BinaryIO, Dict, List, Optional, Union
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.mssp.logos.schema import LogoSchema


class LogosAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Logos API
    '''
    _path = 'api/v3/mssp/logos'
    _conv_json = True
    _schema = LogoSchema()

    def add(self, logo: Union[BytesIO, BinaryIO], name: str) -> UUID:
        '''
        Adds a logo to the Tenable.io MSSP Portal

        Args:
            fobj (FileObject):
                A file-like object of the logo.
            name (str):
                Name of the logo.

        Returns:
            :obj:`str`:
                Return the logo_id.

        Example:
            >>> with open('/opt/download1.png', 'rb') as fobj:
            ...    resp = tio.v3.mssp.logos.add(fobj, 'logo1')
        '''
        payload = {'files': {'logo': logo, 'name': name}}
        return self._post(**payload)['id']

    def search(self):
        '''
        Initiate a search

        Args:
            resource (str):
                The json key to fetch the data from response
            api_path (str):
                API path for search endpoint
            is_sort_with_prop (bool):
                If set to True sort structure will be in form of
                {'property':'field_name','order': 'asc'} else
                {'field_name': 'asc'}
            fields (list):
                The list of field names to return.
                Example:
                    - ``['field1', 'field2']``
            sort (list(tuple)):
                A list of dictionaries describing how to sort the data
                that is to be returned.
                Examples:
                    - ``[{'last_observed': 'desc'}]``
            filter (tuple, dict):
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
            limit (int):
                How many objects should be returned in each request.
                 Default is 1000.
            next (str):
                The pagination token to use when requesting the next page of
                results.  This token is presented in the previous response.
            return_resp (bool):
                If set to true, will override the default behavior to return
                an iterable and will instead return the results for the
                specific page of data.
            return_csv (bool):
                If set to true, It wil return the CSV Iteratble
            iterator_cls:
                If specified, will override the default iterator class that
                will be used for instantiating the iterator.
            schema_cls:
                If specified, will override the default schema class that
                will be used to validate the

        Returns:
            Iterable:
                The iterable that handles the pagination and potentially
                async requests for the job.
            requests.Response:
                If ``return_json`` was set to ``True``, then a response
                object is instead returned instead of an iterable.
        '''
        raise NotImplementedError('Search method will be implemented later')

    def details(self, logo_id: UUID) -> Dict:
        '''
        Returns details for the specified logo in the Tenable.io MSSP Portal.

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            :obj:`dict`:
                Return the logo details.

        Example:
            >>> tio.v3.mssp.logos.details(
            ...    '61a36add-d29b-4a52-bbce-c8215952ede5')
        '''
        return self._get(f'{logo_id}')

    def update(self, logo_id: UUID, **kw) -> str:
        '''
        Updates a logo in the Tenable.io MSSP Portal.
        This update overwrites the existing logo.

        Args:
            logo_id (UUID):
                The UUID of the logo
            fobj (FileObject):
                A file-like object of the logo.
            name (str):
                Name of the logo.

        Returns:
            :obj:`str`:
                Return the logo_id.

        Example:
            >>> fobj = open('/opt/test_image.png', 'rb')
            ...     update_resp = tio.v3.mssp.logos.update(
            ...     '0cba902a-bd11-4481-bd28-999c88ffe22f',
            ...     name='update_name.png',
            ...     logo=fobj)
        '''
        logo_dict = {}
        if kw.get('name'):
            logo_dict['name'] = kw['name']
        if kw.get('logo'):
            logo_dict['logo'] = kw['logo']
        payload = {'files': logo_dict}
        return self._patch(f'{logo_id}', **payload)['id']

    def delete(self, logo_id: UUID) -> None:
        '''
        Deletes Logo for the gived logo_id

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            None

        Example:
            >>> tio.v3.mssp.logos.delete(
            ...    '61a36add-d29b-4a52-bbce-c8215952ede5')
        '''
        self._delete(f'{logo_id}')

    def assign_logos(self, logo_id: UUID, account_ids: List) -> None:
        '''
        Assigns a logo to one or more customer accounts in the Tenable.io
        MSSP Portal.

        Args:
            logo_id (UUID):
                The UUID of the logo
            account_ids (List):
                list of accoint_ids to assign logos to.

        Returns:
            None

        Example:
            >>> tio.v3.mssp.logos.assign_logos(
            ...    'a39f6b74-9b7f-4372-a7ac-a2a4bcb8dbad',
            ...        ['0fc4ef49-2649-4c76-bfa7-c181be3adf26'])
        '''
        payload = {'account_ids': account_ids, 'logo_id': logo_id}
        self._schema.load(self._schema.dump({
            'account_ids': account_ids,
            'logo_id': logo_id
        }
        ))
        self._api.put('api/v3/mssp/accounts/logos', json=payload)

    def download_png(self,
                     logo_id: UUID,
                     fobj: Optional[Union[BytesIO, BinaryIO]] = None
                     ) -> Union[BytesIO, BinaryIO]:
        '''
        Downloads the logo in either base64 or png format.

        Args:
            logo_id (UUID):
                The UUID of the logo
            fobj (FileObject, optional):
                A file-like object to write the contents of the logo to.
        Returns:
            :obj:`FileObject`:
                A file-like object containing the contents of the image

        Example:
            >>> with open('/opt/f2.png', 'wb') as f:
            ...        tio.v3.mssp.logos.download_png(
            ...        'a39f6b74-9b7f-4372-a7ac-a2a4bcb8dbad',
            ...        fobj=f)
        '''
        if not fobj:
            fobj = BytesIO()

        image = self._get(f'{logo_id}/logo.png', stream=True)
        for chunk in image.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        image.close()
        return fobj

    def download_base64(self, logo_id: UUID) -> str:
        '''
        Downloads the logo in either base64 or png format.

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            :obj:`str`:
                Return the encoded base64 image contents.

        Example:
            >>> resp = tio.v3.mssp.logos.download_base64(
            ...    '61a36add-d29b-4a52-bbce-c8215952ede5')
        '''
        image = self._get(f'{logo_id}/logo.base64')
        return image.content
