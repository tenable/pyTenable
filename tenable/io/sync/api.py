"""
Synchronization
===============

Methods described in this section relate to the synchronization API.
These methods can be accessed at ``TenableIO.sync``.

.. rst-class:: hide-signature
.. autoclass:: SynchronizationAPI
    :members:
"""

from __future__ import annotations

from typing import Any
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
        sync_id: str | None = None,
        after: str | None = None,
        limit: str | None = 25,
        states: list[str] | None = None,
        return_json: bool = False,
    ) -> JobListIterator | list[Job]:
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

        Returns:
            JobListIterator:
                An iterable for handling pagination of the job listing.

        Example:
            >>> for job in tvm.sync.list():
            ...     print(job.id, job.sync_id)
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

    def get(self, sync_id: str, job_id: UUID | str) -> Job:
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
        response = self._get(f'{sync_id}/jobs/{job_id}')
        return Job(**response)

    def create(
        self,
        sync_id: str,
        submission_timeout: int = 1800,
        job_lifetime: int = 604800,
        return_json: bool = False,
    ) -> JobManager | dict[str, Any]:
        """
        Initialized a new synchronization job. It is _highly_ recommended to use the
        default JobManager object that's returned from this call instead of building
        your own.

        Args:
            sync_id (str):
                The synchonization id
            submission_timeout (int, 1800):
                The number of seconds to wait after a chunk has been uploaded before
                automatically terminating the job.  This timeout allows for automatic
                cleanup of stalled jobs to ensure that a single bad job doesn't clog
                the pipeline.
            job_lifetime (int, 6048000):
                The number of seconds that the job can exist in any non-active state
                before automatic cleanup.

        Returns:
            JobManager:
                The JobManager object handles most of the basic state tracking of the
                job for you.  It'll also send all of the data objects added to the job
                through the supported data models before sending those objects to the
                job processor.  This allows for catching any potentially bad data
                objects early and informs the developer what attributes are malformed
                or are missing.

        Example:
            >>> job = tvm.sync.create('example_id')
            >>> with job:
            ...     for obj in dataset:
            ...         job.add(obj)
            >>> print(job.counters)
        """
        payload = {
            'active_state_timeout_seconds': submission_timeout,
            'expire_after_seconds': job_lifetime,
        }
        resp = self._post(
            path=f'{sync_id}/jobs',
            json=payload,
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
        objects: list[dict[str, Any]],
    ) -> bool:
        """
        Uploads the data chunk to the supplied job id.

        Args:
            sync_id (str):
                The synchronization id
            job_id (str):
                The job UUID
            chunk_id (int):
                The chunk id for the chunk being uploaded.
            objects (list[dict[str, Any]]):
                The list of supported objects to be uploaded into the chunk

        Returns:
            Returns the boolean response from the data processor indicating whether the
            data chunk follows the supported schema.

        Example:
            >>> tvm.sync.upload_chunk(
            ...     sync_id='example_id',
            ...     job_id='12345678-1234-1234-1234-123456789012',
            ...     chunk_id=1,
            ...     objects=[list, of, data, objects],
            ... )
        """
        data = SyncChunkObjects(objects=objects)
        return self._post(
            f'{sync_id}/jobs/{job_id}/chunks/{chunk_id}',
            json=data.model_dump(exclude_none=True, mode='json'),
        ).success

    def delete(self, sync_id: str, job_id: UUID | str) -> None:
        """
        Cancels the sync job and informs the processor to terminate and remove the job
        details

        Args:
            sync_id (str):
                The synchronization id
            job_id (str):
                The job UUID

        Returns:
            None

        Example:
            >>> tvm.sync.delete('example_id', '12345678-1234-1234-1234-123456789012')
        """
        self._delete(f'{sync_id}/jobs/{job_id}')

    def submit(self, sync_id: str, job_id: str, num_chunks: int) -> bool:
        """
        Informs the job processor that the job is complete and ready for processing.

        Args:
            sync_id (str):
                The synchronization id
            job_id (str):
                The job uuid
            num_chunks (int):
                The total number of chunks that have been submitted for the job.

        Return:
            Returns a boolean value indicating whether the job has successfully been
            closed and submitted for processing.

        Example:
            >>> tvm.sync.submit(
            ...     sync_id='example_id',
            ...     job_id='12345678-1234-1234-1234-123456789012',
            ...     num_chunks=20
            ... )
        """
        return self._post(
            path=f'{sync_id}/jobs/{job_id}/_submit',
            json={'number_of_chunks': num_chunks},
        ).success

    def audit_logs(
        self,
        sync_id: str,
        job_id: UUID | str,
        levels: list[Literal['INFO', 'WARN', 'ERROR']] | None = None,
        after: str | None = None,
        limit: int | None = 25,
        return_json: bool = False,
    ) -> JobLogIterator | list[LogLine]:
        """
        Retreives the audit logs for the requested synchronization job.

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

        Example:
            >>> sync_id = 'example_id'
            >>> job_id = '12345678-1234-1234-1234-123456789012'
            >>> for line in tvm.sync.audit_logs(sync_id, job_id):
            ...     print(line.id, line.message)
        """
        if return_json:
            resp = self._get(
                f'{sync_id}/jobs/{job_id}/audits',
                params={'after': after, 'levels': levels},
            )
            return [LogLine(**i) for i in resp.audits]
        return JobLogIterator(
            self._api,
            _sync_id=sync_id,
            _job_id=job_id,
            after=after,
            _levels=levels,
            _limit=limit,
        )
