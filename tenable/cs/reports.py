from .base import CSEndpoint
from tenable.errors import InvalidInputError
from io import BytesIO

class ReportsAPI(CSEndpoint):
    def report(self, container_id=None, image_id=None, digest=None):
        '''
        `container-security-reports: report-by-container-id <https://cloud.tenable.com/api#/resources/container-security-reports/report-by-container-id>`_
        `container-security-reports: report-by-image-id <https://cloud.tenable.com/api#/resources/container-security-reports/report-by-image-id>`_
        `container-security-reports: report-by-image-digest <https://cloud.tenable.com/api#/resources/container-security-jobs/report-by-image-digest>`_

        One of the options below must be set.

        Args:
            container_id (int, optional): The conatiner id.
            image_id (int, optional): The image identifier.
            digest (str, optional): The image digest.

        Returns:
            dict: The report resource record.
        '''
        # These three calls were lumped into the same method as they all return
        # the same data in the same way, and the only real difference was the
        # identifier being called.

        if container_id:
            return self._api.get('v1/reports/show', params={
                'job_id': self._check('container_id', container_id, int)}).json()
        elif image_id:
            return self._api.get('v1/reports/by_image', params={
                'image_id': self._check('image_id', image_id, str)}).json()
        elif digest:
            return self._api.get('v1/reports/by_image_digest', params={
                'image_digest': self._check('digest', digest, str)}).json()
        else:
            raise UnexpectedValueError('no identifiers were passed')

    def nessus_report(self, container_id, fobj=None):
        '''
        `container-security-reports: nessus-report-by-container-id <https://cloud.tenable.com/api#/resources/container-security-reports/nessus-report-by-container-id>`_

        Args:
            container_id (int): The unique identifier for the container image.
            fobj (FileObject, optional): 
                The file-like object to write the Nessus report into.  If none
                is specified, then we will use a BytesIO object to write the
                Nessus report into.

        Returns:
            FileObject: The Nessus report file.
        '''
        resp = self._api.get('v1/reports/nessus/show', params={
            'id': self._check('container_id', container_id, int)})

        # If no file object was given to us, then lets create a new BytesIO
        # object to dump the data into.
        if not fobj:
            fobj = BytesIO()

        # Stream the data into the file.
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # return the FileObject.
        return fobj
