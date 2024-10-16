import logging
from typing import TYPE_CHECKING, Any, Dict, List
from uuid import UUID

if TYPE_CHECKING:
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
    terminate_on_failure: bool

    def __init__(
        self,
        api: 'TenableIO',
        sync_id: str,
        job_uuid: UUID,
        terminate_on_failue: bool = True,
    ):
        self.sync_id = sync_id
        self.uuid = job_uuid
        self._api = api
        self.chunks = {}
        self.chunk_id = 1
        self.terminate_on_failure = terminate_on_failue
        self._log = logging.getLogger(f'JobManager[{sync_id}:{job_uuid}]')

    def upload(self, objects: List[Dict[str, Any]], num_retries: int = 3) -> None:
        """
        Uploads a collection ob objects to the job processor as a chunk of data.

        Args:
            num_entries (int, 3):
                The number of times to retry a failed upload before raising an error.
            **objects: (dict[str, Any]):
                The object definitions
        """
        retry_counter = 0
        resp = None
        while retry_counter < num_retries and not resp:
            # Need to add try/except handling here.
            resp = self._api.sync.upload_chunk(
                sync_id=self.sync_id,
                job_id=self.uuid,
                chunk_id=self.chunk_id,
                objects=objects,
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

    def terminate(self):
        self._api.sync.delete(self.sync_id, self.uuid)

    def submit(self) -> bool:
        """ """
        return self._api.sync.submit(
            sync_id=self.sync_id, job_id=self.uuid, num_chunks=self.chunk_id - 1
        )
