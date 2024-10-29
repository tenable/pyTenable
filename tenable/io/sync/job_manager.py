import logging
import time
from typing import TYPE_CHECKING, Any, Literal
from uuid import UUID

from restfly.errors import APIError, InvalidContentError

from .models.cve_finding import CVEFinding
from .models.device_asset import DeviceAsset

if TYPE_CHECKING:
    from pydantic import BaseModel

    from tenable.io import TenableIO


class SyncJobFailure(Exception):
    pass


class SyncJobTerminated(Exception):
    pass


class JobManager:
    sync_id: str
    uuid: UUID
    _api: 'TenableIO'
    _log: logging.Logger
    chunk_id: int
    _max_retries: int = 3
    terminate_on_failure: bool
    _object_map: dict[str, Any] = {
        'cve-finding': CVEFinding,
        'device-asset': DeviceAsset,
    }
    assets: int = 0
    findings: int = 0
    _cache_max: int = 1000
    _cache: list['BaseModel']

    def __init__(
        self,
        api: 'TenableIO',
        sync_id: str,
        job_uuid: UUID,
        terminate_on_failue: bool = True,
        max_retries: int = 3,
        retry_delay: int = 30,
        cache_max: int = 1000,
    ):
        self._cache = []
        self._cache_max = cache_max
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self.sync_id = sync_id
        self.uuid = job_uuid
        self._api = api
        self.chunks = {}
        self.chunk_id = 1
        self.terminate_on_failure = terminate_on_failue
        self._log = logging.getLogger(f'JobManager[{sync_id}:{job_uuid}]')
        self._log.info(f'Starting management of job {sync_id} :: {job_uuid}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # If no exception was raised while the job was in progress
        # we will then submit the job and close it out.
        if exc_type is None:
            self.submit()

        # Otherwise we will check to see if we should be terminating
        # the job and perform the appropriate action.
        else:
            self._log.error(f'failed with {exc_type}:{exc_value}')
            if self.terminate_on_failure:
                self.terminate()

    def add(
        self,
        object: dict[str, Any],
        object_type: Literal['device-asset', 'cve-finding'],
    ) -> None:
        """
        Adds an object to the job for processing.

        Args:
            object: The dictionary object to load into the sync job.
            object_type: The type of sync object that is being added to the job.
        """
        type_switch = {'device-asset': self.assets, 'cve-finding': self.findings}
        self._cache.append(self._object_map[object_type](**object))
        type_switch[object_type] += 1

        # If the number of items added to the cache exceeds the cache limits, then we
        # should upload a new chunk of data and flush the cache.
        if len(self._cache) >= self._cache_max:
            self.upload()

    def upload(self) -> None:
        """
        Uploads a collection ob objects to the job processor as a chunk of data.

        Args:
            num_entries (int, 3):
                The number of times to retry a failed upload before raising an error.
        """
        retry_counter = 0
        resp = None
        while retry_counter < self._max_retries and not resp:
            self._log.info(
                f'Uploading chunk={self.chunk_id} '
                f'attempt {retry_counter + 1} of {self._max_retries}'
            )
            try:
                resp = self._api.sync.upload_chunk(
                    sync_id=self.sync_id,
                    job_id=self.uuid,
                    chunk_id=self.chunk_id,
                    objects=self._cache,
                )
            except InvalidContentError as err:
                # If we receive a 422 response, then we should terminate the job and
                # raise job termination error detailing why the job was terminated.
                self.terminate()
                raise SyncJobTerminated(
                    f'Job {self.uuid} has been terminated due to server error.  '
                    f'The upstream server error is {err.response.content}'
                ) from err
            except APIError as _:
                # If we receive any other API error, we will log the error and wait
                # for the retry delay to expire before attempting again.
                self._log.exception('Upstream API Error Occurred.')
                time.sleep(self._retry_delay)
            except Exception as err:
                # If any other exception is fired then we will terminate the job and
                # raise a job termination error.
                self.terminate()
                raise SyncJobTerminated(
                    'An unknown error has occurred and caused the sync job to terminate'
                ) from err

            # We always want to increment the retry counter by one no matter what.
            retry_counter += 1

        if not resp and self.terminate_on_failure:
            # If we ran out of retries and still havent received a response back, then
            # we should terminate the job and inform the caller that the upload has
            # failed.
            self.terminate()
            raise SyncJobTerminated(
                f'Chunk {self.chunk_id} failed to upload '
                'and caused the job to be terminated.'
            )
        elif not resp:
            # If there isn't any response, but the automatic termination of the job is
            # not enabled, then raise a job failure error instead.
            raise SyncJobFailure(f'Chunk {self.chunk_id} failed to upload')

        # Increment the chunk counter and flush the cache.
        self.chunk_id += 1
        self._cache = []

    def terminate(self):
        """
        Terminates the current job, abandoning any data that
        has already been uploaded.
        """
        self._log.info(f'terminating Job {self.sync_id} :: {self.uuid}')
        self._api.sync.delete(self.sync_id, self.uuid)

    def submit(self) -> bool:
        """
        Submits the current job for processing.
        """
        # if there are any remaining items in the cache, then we will drain the cache
        # before submitting the job.
        if len(self._cache) > 0:
            self.upload()
        self._log.info(f'Submitting {self.sync_id} :: {self.uuid} for processing.')

        # Submit the job
        return self._api.sync.submit(
            sync_id=self.sync_id, job_id=self.uuid, num_chunks=self.chunk_id - 1
        )
