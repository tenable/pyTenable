from .base import CSEndpoint
from tenable.errors import InvalidInputError

class JobsAPI(CSEndpoint):
    def list(self):
        '''
        `container-security-jobs: list-jobs <https://cloud.tenable.com/api#/resources/container-security-jobs/list-jobs>`_

        Returns:
            list: List of job status records.
        '''
        return self._api.get('v1/jobs/list').json()

    def status(self, job_id=None, image_id=None, digest=None):
        '''
        `container-security-jobs: job-status <https://cloud.tenable.com/api#/resources/container-security-jobs/job-status>`_
        `container-security-jobs: job-status-by-image-id <https://cloud.tenable.com/api#/resources/container-security-jobs/job-status-by-image-id>`_
        `container-security-jobs: job-status-by-image-digest <https://cloud.tenable.com/api#/resources/container-security-jobs/job-status-by-image-digest>`_

        One of the options below must be set.

        Args:
            job_id (int, optional): The unique identifier for the job.
            image_id (int, optional): The image identifier.
            digest (str, optional): The image digest.

        Returns:
            dict: The job status resource record.
        '''
        # These three calls were lumped into the same method as they all return
        # the same data in the same way, and the only real difference was the
        # identifier being called.

        if job_id:
            return self._api.get('v1/jobs/status', params={
                'job_id': self._check('job_id', job_id, int)}).json()
        elif image_id:
            return self._api.get('v1/jobs/image_status', params={
                'image_id': self._check('image_id', image_id, str)}).json()
        elif digest:
            return self._api.get('v1/jobs/image_status_digest', params={
                'image_digest': self._check('digest', digest, str)}).json()
        else:
            raise UnexpectedValueError('no identifiers were passed')

