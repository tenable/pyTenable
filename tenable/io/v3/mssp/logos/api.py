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
import os
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
        Adds a new logo

        Args:
            fobj (FileObject, optional):
                A file-like object of the logo.
            name (str):
                Name of the logo.

        Returns:
            :obj:`str`:
                Return the logo_id.

        Example:
            >>>> with open('/opt/download1.png', 'rb') as fobj:
                    resp = tio.v3.mssp.logos.add(fobj, 'logo1')
        '''
        payload = {'files': {'logo': logo, 'name': name}}
        return self._post(**payload)['id']

    def list(self):
        '''
        Returns list of logos

        Args:

        Returns:
            :obj:`list`:
                Returns all the logo details as a list.

        Example:
            >>>> tio.v3.mssp.logos.list()
        '''
        return self._get()['logos']

    def search(self):
        '''
        Get the listing of Logos from MSSP portal.

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

    def update(self, logo_id: UUID, **kw) -> str:
        '''
        Returns Logo details

        Args:
            logo_id (UUID):
                The UUID of the logo
        Returns:
            :obj:`str`:
                Return the logo_id.

        Example:
            >>>> fobj = open('/opt/test_image.png', 'rb')
                 update_resp = tio.v3.mssp.logos.update(
                     '0cba902a-bd11-4481-bd28-999c88ffe22f',
                     name='update_name.png',
                     logo=fobj
                    )
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
            >>>> tio.v3.mssp.logos.delete(
                '61a36add-d29b-4a52-bbce-c8215952ede5')
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
            >>>> tio.v3.mssp.logos.assign_logos(
                    'a39f6b74-9b7f-4372-a7ac-a2a4bcb8dbad',
                    ['0fc4ef49-2649-4c76-bfa7-c181be3adf26']
                )
        '''
        payload = {'account_ids': account_ids, 'logo_id': logo_id}
        self._schema.load(self._schema.dump({
            'account_ids': account_ids,
            'logo_id': logo_id
        }
        ))
        self._api.put('api/v3/mssp/accounts/logos', json=payload)

    def download_png(
        self,
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
            >>>> with open('/opt/f2.png', 'wb') as f:
                    tio.v3.mssp.logos.download_png(
                        'a39f6b74-9b7f-4372-a7ac-a2a4bcb8dbad',
                        fobj=f
                    )
        '''
        logo_name = self.details(logo_id)['name']
        if not fobj:
            logo_path = os.path.join(
                os.getcwd(),
                os.path.dirname(__file__),
                logo_name
            )
            fobj = open(logo_path, 'wb')

        image = self._get(f'{logo_id}/logo.png', stream=True)
        for chunk in image.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)
        image.close()

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
            >>>> resp = tio.v3.mssp.logos.download_base64(
                    '61a36add-d29b-4a52-bbce-c8215952ede5'
                    )
        '''
        image = self._get(f'{logo_id}/logo.base64')
        return image.content
