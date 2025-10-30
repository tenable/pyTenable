"""
As exports are asynchronous, pyTenable by default will return an iterator to
handle the state tracking, data chunking, and presentation of the data in order
to reduce the amount of boilerplate code that would otherwise have to be
created.  These iterators support both serial iteration and threaded
handling of data depending on how the data is accessed.

.. autoclass:: ExportsIterator
    :members:
"""

import time
from concurrent.futures import Future, ThreadPoolExecutor
from copy import deepcopy
from typing import Any, Callable

from box import Box
from restfly.iterator import APIIterator

from tenable.errors import TioExportsError, TioExportsTimeout


class ExportsIterator(APIIterator):
    """
    The export iterator can be used to handle the downloading and processing
    of the data chunks from an export request.
    """

    _term_on_error: bool = True
    _wait_for_complete: bool = False
    _is_iterator: bool | None = None

    boxify: bool = False
    """Should items be returned as box objects?"""

    chunks: list[int]
    """Current list of available chunks."""

    processed: list[int]
    """Chunks that have already been processed."""

    page: list[dict[str, Any]]
    """Current Page (chunk) of data thats being worked on."""

    chunk_id: int | None = None
    """Id of the chunk currently being processed."""

    timeout: int | None = None
    """Max seconds to wait in pending before cancelling the job."""

    uuid: str
    """Export job id."""

    type: str
    """Export job type."""

    version: str
    """Export job version."""

    status: str
    """Export job status."""

    start_time: int
    """Export job start time (unix timestamp)."""

    count: int = 0
    """Number of objects processed so far within the current page (chunk)."""

    page_count: int = 0
    """Number of pages (chunks) processed so far across the entire export job."""

    def __init__(self, api, **kwargs):
        self.chunks = []
        self.processed = []
        self.page = []
        self.start_time = int(time.time())
        super().__init__(api, **kwargs)

    def _get_status_resp(self) -> dict[str, Any]:
        return self._api.exports.status(self.type, self.uuid, version=self.version)

    def _get_status(self) -> dict[str, Any]:
        """
        Get the current status of the export, and then calculate where the iterator is
        within the export job and return the status to the caller
        """
        status = self._get_status_resp()
        self._log.debug(
            f'{self.type} export {self.version} {self.uuid} is currently {status.status}',
        )

        # If the export has errored and the _term_on_error flag is set, then
        # we will raise an export error.
        if status.status == 'ERROR' and self._term_on_error:
            raise TioExportsError(self.type, self.uuid)

        # If the export is still queued and the timeout has been reached, then
        # we will inform the API that we want to cancel the export and then
        # raise a timeout exception.
        if (
            status.status == 'QUEUED'
            and self.timeout is not None
            and time.time() > self.timeout + self.start_time
        ):
            self.cancel()
            raise TioExportsTimeout(self.type, self.uuid)

        # If the _wait_for_complete flag has been set, then we will always
        # return an empty list until the status is 'FINISHED'
        if self._wait_for_complete and status.status != 'FINISHED':
            status.chunks_unfinished = []

        # In all other situations, we will Compute which chunks are currently
        # unprocessed by the iterator and store the list within the
        # "chunks_unfinished" attribute.
        else:
            avail = status.get('chunks_available', [])
            unfinished = [c for c in avail if c not in self.processed]
            status.chunks_unfinished = unfinished
        self.chunks = status.chunks_unfinished
        self.status = status.status

        # Return the status to the caller.
        return status

    def _get_chunks(self):
        """
        Update the chunks list with the currently available chunks that we have
        yet to process.  Note that this method will only run when there appear
        to be no chunks in the chunk list.
        """
        if len(self.chunks) < 1:
            status = self._get_status()

            backoff_counter = 1
            # If the export is still processing, but there aren't any chunks
            # for us to process yet, then we will wait here in a loop and call
            # for status once a second until we get something else to work on.
            while len(status.chunks_unfinished) < 1 and status.status not in [
                'ERROR',
                'FINISHED',
            ]:
                backoff_counter += 1
                time.sleep(backoff_counter if backoff_counter < 30 else 30)
                status = self._get_status()
            self._log.debug(f'{status} and {self.chunks}')
            if (
                self.status in ['ERROR', 'FINISHED']
                and len(self.chunks) == 0
                and self._is_iterator
            ):
                self._log.info(
                    f'Export {self.type}:{self.uuid} '
                    f'has {self.status} and has '
                    f'processed {self.page_count} items.'
                )
                raise StopIteration()
        return self.chunks

    def _get_chunk_data(self, type, uuid, chunk_id) -> list:
        return self._api.exports.download_chunk(
            type, uuid, chunk_id, version=self.version
        )

    def _get_page(self):
        """
        Gets the next chunk of data for the iterator
        """
        # We need to update the chunk queue and raise a stop iteration exception if
        # there is nothing left to process.
        self._get_chunks()

        # Now to take the first chunk off the local queue, move it to the processed
        # list, and store the chunk id
        self.chunk_id = self.chunks.pop(0)
        self.processed.append(self.chunk_id)
        self.page = self._get_chunk_data(self.type, self.uuid, self.chunk_id)

        # If the chunk of data is empty, then we will call ourselves to get the
        # next page of data. This allows us to properly handle empty chunks of
        # data.
        if len(self.page) < 1:
            self._get_page()

    def next(self):
        """
        Get the next item in the current page
        """
        # If the threading flag has not been set, then we should set it now.
        if self._is_iterator is None:
            self._is_iterator = True

        # If the threading flag has already been set and is indicating that this export
        # job should be treated as a threaded job, and not an iterator, then throw an
        # error.
        elif not self._is_iterator:
            raise TioExportsError(
                export=self.type,
                uuid=self.uuid,
                msg=(
                    f'ExportIterator for {self.uuid} already set to run as a threaded '
                    'job.  Cannot perform iterable operations.'
                ),
            )

        # If we have worked through the current page of records then we should query
        # the next page of records.
        if self.page_count >= len(self.page):
            if self.chunk_id:
                self._log.info(
                    f'Job {self.type}:{self.uuid}:{self.chunk_id} processed {self.count} items.'
                )
            self._get_page()
            self.page_count = 0

        # Get the relevant record, increment the counters, and return the record.
        item = self.page[self.page_count]
        self.count += 1
        self.page_count += 1
        if self.boxify:
            return Box(item)
        return item

    def cancel(self) -> None:
        """
        Cancels the current export
        """
        self._api.exports.cancel(self.type, self.uuid, version=self.version)

    def run_threaded(
        self,
        func: Callable,
        kwargs: dict[str, Any] | None = None,
        num_threads: int = 2,
    ) -> list[Future]:
        """
        Initiate a multi-threaded export using the provided function and
        keyword arguments.  The following field names are reserved and must be
        accepted either as an optional keyword argument, or as a named param.

            * data (list[dict]): Receiver of the data-chunk.
            * export_uuid (str): Receiver for the export job UUID.
            * export_type (str): Receiver for the export data-type.
            * export_chunk_id (int): Receiver for the export chunk id.
            * version (int): Receiver for the export version.

        Args:
            func:
                The function to pass to the thread executor.
            kwargs:
                Any additional keyword arguments that are to be passed to the
                function as part of execution.
            num_threads:
                How many concurrent threads should be run.  The default is
                ``2``.

        Examples:

            A simple example to download the chunks and write them to disk.

            >>> def write_chunk(data,
            ...                 export_uuid: str,
            ...                 export_type: str,
            ...                 export_chunk_id: int,
            ...                 version: int
            ...                 ):
            ...     fn = f'{export_type}-{export_uuid}-{export_chunk_id}-{version}.json'
            ...     with open(fn, 'w') as fobj:
            ...         json.dump(data, fobj)
            >>>
            >>> export = tio.exports.vulns()
            >>> export.run_threaded(write_chunk, num_threads=4)
        """
        if not kwargs:
            kwargs = {}
        # If the iterator flag is unset, then we will set it.
        if self._is_iterator is None:
            self._is_iterator = False

        # If the iterator flag was already set to be an iterable, then we will raise an
        # error that we cannot continue.
        elif self._is_iterator:
            raise TioExportsError(
                export=self.type,
                uuid=self.uuid,
                msg=(
                    f'ExportIterator for {self.uuid} '
                    'already set to run as an iterable '
                    'job.  Cannot perform threaded '
                    'operations.'
                ),
            )

        def thread_job(chunk_id: int):
            kw: dict[str, Any] = deepcopy(kwargs)  # ty: ignore[invalid-assignment]
            kw['data'] = self._get_chunk_data(self.type, self.uuid, chunk_id)
            kw['export_uuid'] = self.uuid
            kw['export_type'] = self.type
            kw['export_chunk_id'] = chunk_id
            kw['version'] = self.version
            self._log.debug(
                (
                    f'{self.type} export {self.uuid} chunk {chunk_id} '
                    'has been downloaded and the data has been handed '
                    'off to the specified function'
                )
            )
            return func(**kw)

        # Initiate the thread pool and get the show on the road.
        jobs = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # We will want to make sure to stay in this loop until the job is finished
            # and all the chunks have been processed.
            while not (len(self._get_chunks()) < 1 and self.status in ['FINISHED']):
                # Loop over the number of chunks that are available, pulling each chunk
                # id out of the chunk list, constructing the kwargs with the necessary
                # elements, and loading that job into the executor. When all the chunks
                # have been added to the pool, then call the _get_chunks method again
                # for more chunks to become available.
                num_chunks = range(len(self.chunks))
                for _ in num_chunks:
                    chunk_id = self.chunks.pop(0)
                    jobs.append(executor.submit(thread_job, chunk_id))
                    self.processed.append(chunk_id)
        return jobs
