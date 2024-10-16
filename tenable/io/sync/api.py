"""
Synchronization
===============

Methods described in this section relate to the synchronization API.
These methods can be accessed at ``TenableIO.sync``.

.. rst-class:: hide-signature
.. autoclass:: SynchronizationAPI
    :members:
"""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from typing_extensions import Literal

from tenable.base.endpoint import APIEndpoint

from .iterator import JobListIterator, JobLogIterator
from .job_manager import JobManager
from .models.job import Job, LogLine
from .models.sync_objects import SyncChunkObjects


class SynchronizationJobCreationError(Exception):
    pass


class SynchronizationAPI(APIEndpoint):
    _path = 'api/v3/data/synchronizations'
    _box = True

    def list(
        self,
        sync_id: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[str] = 25,
        states: Optional[List[str]] = None,
        return_json: bool = False,
    ) -> Union[JobListIterator, List[Job]]:
        """
        Returns the list of jobs regardless of state as long as they have not been
        deleted or expired.

        Args:
            sync_id (str, optional):
            after (str, optional):
                Retreive the jobs in the listing after this one.  used in pagination.
            limit (int, 25):
                Collect job objects until the limit is reached for the page.
            states (list[str], optional):
                Filter the results to only be the specified states.  Supported states
                are ``active``, ``canceled``, ``pending``, ``processing``, ``errored``.
        """
        if return_json:
            params = {
                'after': after,
                'limit': limit,
                'states': [s.upper() for s in states] if states else None,
            }
            path = f'{sync_id}/jobs' if sync_id else 'jobs'
            return self._get(path, params=params).jobs
        return JobListIterator(
            self._api, _sync_id=sync_id, _after=after, _limit=limit, _states=states
        )

    def get(self, sync_id: str, job_id: Union[UUID, str]) -> Job:
        """
        Retreives the details about a specific job

        Args:
            sync_id (str):
                The synchronization identifier
            job_id (UUID | str):
                The job identifier

        Returns:
            Job:
                The job resource object
        """
        response = self._get(f'{sync_id}/jobs/{job_id}')  # TODO: Is this enveloped????
        return Job(**response)

    def create(
        self,
        sync_id: str,
        product: str,
        source: str,
        vendor: str,
        submission_timeout: int = 1800,
        job_lifetime: int = 604800,
        ignore_orphaned: bool = True,
        return_json: bool = False,
    ) -> Union[JobManager, Dict[str, Any]]:
        """ """
        resp = self._post(
            path=f'{sync_id}/jobs',
            json={
                'active_state_timeout_seconds': submission_timeout,
                'expire_after_seconds': job_lifetime,
                'data_integrity_object': {
                    'ignore_orphaned': ignore_orphaned,
                },
                'origin': {
                    'product_id': product,
                    'source_id': source,
                    'vendor_id': vendor,
                },
            },
        )
        if return_json:
            return resp
        if resp.success:
            return JobManager(api=self._api, sync_id=sync_id, job_uuid=resp.id)
        raise SynchronizationJobCreationError(
            'Could not create the job, received {dict(resp)}'
        )

    def upload_chunk(
        self,
        sync_id: str,
        job_id: str,
        chunk_id: int,
        objects: List[Dict[str, Any]],
    ) -> bool:
        """ """
        data = SyncChunkObjects(objects=objects)
        return self._post(
            f'{sync_id}/jobs/{job_id}/chunks/{chunk_id}',
            json=data.model_dump(exclude_none=True, mode='json'),
        ).success

    def delete(self, sync_id: str, job_id: Union[UUID, str]) -> None:
        """ """
        self._delete(f'{sync_id}/jobs/{job_id}')

    def submit(self, sync_id: str, job_id: str, num_chunks: int) -> bool:
        """ """
        return self._post(
            path=f'{sync_id}/jobs/{job_id}/_submit',
            json={'number_of_chunks': num_chunks},
        ).success

    def logs(
        self,
        sync_id: str,
        job_id: Union[UUID, str],
        levels: Optional[List[Literal['INFO', 'WARN', 'ERROR']]] = None,
        after: Optional[str] = None,
        limit: Optional[int] = 25,
        return_json: bool = False,
    ) -> Union[JobLogIterator, List[LogLine]]:
        """
        Retreives the logs for the requested synchronization job.

        Args:
            sync_id (str):
                The synchronization identifier
            job_id (UUID | str):
                The job identifier
            levels (list[str], optional):
                The log levels to return.  Must specify each explicit level to return.
                By default will return all levels.
            after: (str, optional):
                Return the log data after this log line id.
            limit: (int, 25):
                Return the defined number of log entries for this page.

        Return:
            JobLogIterator:
                An iterable to handle pagination of the log entries.
        """
        if return_json:
            resp = self._get(
                f'{sync_id}/jobs/{job_id}/logs',
                params={'after': after, 'levels': levels},
            )
            return [LogLine(**i) for i in resp.lines]
        return JobLogIterator(
            self.api,
            _sync_id=sync_id,
            _job_id=job_id,
            after=after,
            _levels=levels,
            _limit=limit,
        )
