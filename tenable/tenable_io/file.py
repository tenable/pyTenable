from tenable.tenable_io.base import TIOEndpoint

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
        return self._api.post('file/upload', 
            data={'no_enc': int(encrypted)},
            files={'Filedata': fobj}).json()['fileuploaded']