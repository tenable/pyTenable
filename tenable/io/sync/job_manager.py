import logging
from typing import TYPE_CHECKING, Any, Dict, List, Literal
from uuid import UUID

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
    _cache_max: int = 1000
    _cache: List['BaseModel']

    def __init__(
        self,
        api: 'TenableIO',
        sync_id: str,
        job_uuid: UUID,
        terminate_on_failue: bool = True,
        max_retries: int = 3,
        cache_max: int = 1000,
    ):
        self._cache = []
        self._cache_max = cache_max
        self._max_retries = max_retries
        self.sync_id = sync_id
        self.uuid = job_uuid
        self._api = api
        self.chunks = {}
        self.chunk_id = 1
        self.terminate_on_failure = terminate_on_failue
        self._log = logging.getLogger(f'JobManager[{sync_id}:{job_uuid}]')
        self._log.info(f'Starting management of job {sync_id}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            self.submit()
        else:
            if self.terminate_on_failure:
                self.terminate()
            #Do anything else we want to...    
        
    def add(
        self,
        object: Dict[str, Any],
        object_type: Literal['device-asset', 'cve-finding'],
    ) -> None:
        """ """
        self._cache.append(self._object_map[object_type](**object))
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
            # Need to add try/except handling here.
            resp = self._api.sync.upload_chunk(
                sync_id=self.sync_id,
                job_id=self.uuid,
                chunk_id=self.chunk_id,
                objects=self._cache,
            )
            retry_counter += 1
        if not resp and self.terminate_on_failure:
            self.terminate()
            raise SyncJobTerminated(
                f'Chunk {self.chunk_id} failed to upload '
                'and caused the job to be terminated.'
            )
        elif not resp:
            raise SyncJobFailure(f'Chunk {self.chunk_id} failed to upload')
        self.chunk_id += 1
        self._cache = []

    def terminate(self):
        self._api.sync.delete(self.sync_id, self.uuid)

    def submit(self) -> bool:
        """ """
        if len(self._cache) > 0:
            self.upload()
        return self._api.sync.submit(
            sync_id=self.sync_id, job_id=self.uuid, num_chunks=self.chunk_id - 1
        )
