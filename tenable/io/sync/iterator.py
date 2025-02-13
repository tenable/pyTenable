from typing import TYPE_CHECKING

from restfly.iterator import APIIterator

from .models.job import Job, LogLine

if TYPE_CHECKING:
    from tenable.io import TenableIO


class JobListIterator(APIIterator):
    _api: 'TenableIO'
    _sync_id: str | None = None
    _limit: int = 25
    _states: list[str] | None = None
    after: str | None = None

    def __getitem__(self, key: int) -> Job:
        return Job(**self.page[key])

    def _get_page(self):
        page = self._api.sync.list(
            sync_id=self._sync_id,
            after=self.after,
            limit=self._limit,
            states=self._states,
            return_json=True,
        )
        self.page = page
        if len(page) < self._limit:
            self.max_pages = self.page_count - 1
        else:
            self.after = str(self.page[-1].id)


class JobLogIterator(APIIterator):
    _api: 'TenableIO'
    _sync_id: str
    _job_id: str
    _levels: list[str] | None = None
    _limit: int = 25
    after: str | None = None

    def _get_page(self):
        page = self._api.sync.audit_logs(
            sync_id=self._sync_id,
            job_id=self._job_id,
            levels=self._levels,
            after=self.after,
            limit=self._limit,
            return_json=True,
        )
        self.page = page
        if len(self.page) < self._limit:
            self.max_pages = self.page_count - 1
        else:
            self.after = str(self.page[-1].id)
