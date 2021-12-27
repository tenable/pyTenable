'''
Logos
========

The following methods allow for interaction into the Tenable.io
:devportal:`Logos <io-mssp-logos>` API endpoints.

Methods available on ``tio.v3.mssp.logos``:

.. rst-class:: hide-signature
.. autoclass:: LogosAPI
    :members:
'''
import base64
import os
from io import BytesIO
from typing import ByteString, Dict, List
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint
from tenable.io.v3.mssp.logos.schema import LogoSchema


class LogosAPI(ExploreBaseEndpoint):
    '''
    This class contains methods related to Networks API
    '''
    _path = 'api/v3/mssp/logos'
    # _path = 'mssp/logos'
    _conv_json = True
    _schema = LogoSchema()

    def add(self, logo: BytesIO, name: str) -> Dict:
        '''
        Adds a new logo

        Args:

        Returns:

        Example:
            >>>> tio.v3.mssp.logos.add('D:\\Downloads\\download1.png', 'logo1')
        '''
        # if os.path.exists(logo_path):
        #     file_obj = open(logo_path, 'rb')
        #     kw = {'files': {'logo': file_obj, 'name': name}}
        #     return self._post(**kw)

        payload = {'files': {'logo': logo, 'name': name}}
        payload_dict = self._schema.dump(self._schema.load(payload['files']))
        payload['files'] = payload_dict
        return self._post(**payload)

    def list(self):
        '''
        Returns list of logos

        Args:

        Returns:

        Example:
            >>>> tio.v3.mssp.logos.list()
        '''
        return self._get()

    def search(self):
        '''
        Get the listing of configured networks from Tenable.io.
        :devportal:`networks: list <networks-list>`
        Args:
            *filters (tuple, optional):
                Filters are tuples in the form of
                ('NAME', 'OPERATOR', 'VALUE'). Multiple filters can be used
                to filter down the data being returned from the API.
                Examples:
                    - ``('name', 'eq', 'example')``
            limit (int, optional):
                The number of records to retrieve.  Default is 50
            sort (tuple, optional):
                A tuple of tuples identifying the the field and sort order of
                the field.
            fields (list):
                list of fields to retrieve.
        Returns:
            :obj:`LogosIterator`:
                An iterator that handles the page management of the requested
                records.
        Examples:
            Todo
        '''
        raise NotImplementedError('Search method will be implemented later')

    def details(self, logo_id: UUID) -> Dict:
        '''
        Returns Logo details

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            :obj:`dict`:
                Return the logo details.

        Example:
            >>>> tio.v3.mssp.logos.details(
                '61a36add-d29b-4a52-bbce-c8215952ede5')
        '''
        return self._get(f'{logo_id}')

    def update(self, logo_id: UUID, **kw) -> Dict:
        '''
        Returns Logo details

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            :obj:`dict`:
                Return the logo details.

        Example:
            >>>> tio.v3.mssp.logos.update(
                '61a36add-d29b-4a52-bbce-c8215952ede5',
                 name='updated_name'
                )
        '''
        logo_dict = {}
        if kw.get('name'):
            logo_dict['name'] = kw['name']
        if kw.get('logo'):
            logo_dict['logo'] = kw['logo']
        payload_dict = self._schema.dump(self._schema.load(logo_dict))
        payload = {'files': payload_dict}
        return self._patch(f'{logo_id}', **payload)

    def delete(self, logo_id: UUID) -> None:
        '''
        Returns Logo details

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            :obj:`dict`:
                Return the logo details.

        Example:
            >>>> tio.v3.mssp.logos.delete(
                '61a36add-d29b-4a52-bbce-c8215952ede5')
        '''
        self._delete(f'{logo_id}')

    def assign_logos(self, logo_id: UUID, account_ids: List) -> None:
        '''
        Returns Logo details

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            :obj:`dict`:
                Return the logo details.

        Example:
            >>>> tio.v3.mssp.logos.assign_logos()
        '''
        payload = {'account_ids': account_ids, 'logo_id': logo_id}
        self._schema.load(self._schema.dump({
            'account_ids': account_ids,
            'logo_id': logo_id
        }
        ))
        self._api.put('api/v3/mssp/accounts/logos', json=payload)

    def download(self, logo_id: UUID, type: str) -> ByteString:
        '''
        Downloads the logo in either base64 or png format.

        Args:
            logo_id (UUID):
                The UUID of the logo
            type (str):
                image type png or base64
        Returns:
            :obj:`dict`:
                Return the logo details.

        Example:
            >>>> tio.v3.mssp.logos.download(
                    '61a36add-d29b-4a52-bbce-c8215952ede5',
                     type='base64'
                    )
        '''
        image = self._get(f'{logo_id}/logo.{type}')
        logo_name = self.details(logo_id)['name']

        # confirm path with the team
        logo_path = os.path.join(
            os.getcwd(),
            os.path.dirname(__file__),
            logo_name
        )
        if type == 'png':
            image_64_encode = base64.encodestring(image.content)
        if type == 'base64':
            image_64_encode = image.content.replace(
                b'data:image/png;base64,', b'')

        image_64_decode = base64.decodestring(image_64_encode)
        with open(logo_path, 'wb') as image_file:
            image_file.write(image_64_decode)
