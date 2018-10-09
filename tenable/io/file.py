from .base import TIOEndpoint
import uuid

class FileAPI(TIOEndpoint):
    def upload(self, fobj, encrypted=False):
        '''
        `file: upload <https://cloud.tenable.com/api#/resources/file/upload>`_

        Args:
            fobj (FileObject):
                The file object intended to be uploaded into Tenable.io.
            encrypted (bool, optional):
                If the file is encrypted, set the flag to True.

        Returns:
            str: The fileuploaded attribute
        '''

        # We will attempt to discover the name of the file stored within the
        # file object.  If none exists however, we will generate a random
        # uuid string to use instead.
        try:
            name = fobj.name
        except AttributeError:
            name = str(uuid.uuid4())

        return self._api.post('file/upload', 
            data={'no_enc': int(encrypted)},
            files={'Filedata': (name, fobj)}).json()['fileuploaded']