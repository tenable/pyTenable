'''
Attachments
===========

The following methods allow for interaction into the Tenable.io
:devportal:`attachments <was-v2-attachments>` API.

Methods available on ``tio.v3.was.attachments``:

.. rst-class:: hide-signature
.. autoclass:: AttachmentsAPI
    :members:
'''
from io import BytesIO
from typing import BinaryIO, Optional
from uuid import UUID

from tenable.io.v3.base.endpoints.explore import ExploreBaseEndpoint


class AttachmentsAPI(ExploreBaseEndpoint):

    '''
    This class contains methods related to Attachments API
    '''

    _path = 'api/v3/was/attachments'

    def download_attachment(self,
                            attachment_id: UUID,
                            fobj: Optional[BinaryIO] = None
                            ) -> BinaryIO:
        '''
        Download an attachment.

        :devportal:`attachments: download <was-v2-attachments-download>`

        Args:
            attachment_id:
                The unique identifier for attachment.
            fobj:
                A file-like object to write the contents of the attachment to.
                If none is provided a BytesIO object will be returned with the
                attachment.

        Returns:
            :obj:`Response`
                The Response object based for the requested attachment.

        Examples:
            >>> with open('example.png', 'wb') as img_attachment:
            ...     tio.v3.was.attachments.download_attachment(
            ...             '00000000-0000-0000-0000-000000000000',
            ...             img_attachment
            ...     )
        '''

        # If no file object was given to us, then lets create a new BytesIO
        # object to dump the data into.
        if not fobj:
            fobj = BytesIO()

        resp = self._get(attachment_id, stream=True)

        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)

        fobj.seek(0)
        resp.close()

        return fobj
