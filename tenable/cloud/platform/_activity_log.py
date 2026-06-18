from copy import copy
from typing import Literal

from restfly import APIEndpoint, APIIterator, AsyncAPIEndpoint, AsyncAPIIterator

from .models.activity_log import (
    ActivityLogEvent,
    ActivityLogFilter,
    ActivityLogQueryParams,
    ActivityLogResponse,
    ActivityLogSort,
)


class ActivityLogIterator(APIIterator):
    next: str | None = None
    """The next page token"""

    page: list[ActivityLogEvent]
    params: ActivityLogQueryParams

    def _get_page(self) -> None:
        params = copy(self.params)
        params.next = self.next
        resp = self._client.platform.activity_log._get_events(params=params)
        self.total = resp.pagination.total
        self.next = resp.pagination.next
        self.page = resp.events


class AsyncActivityLogIterator(AsyncAPIIterator):
    next: str | None = None
    """The next page token"""

    page: list[ActivityLogEvent]
    params: ActivityLogQueryParams

    async def _get_page(self) -> None:
        params = copy(self.params)
        params.next = self.next
        resp = await self._client.platform.activity_log._get_events(params=params)
        self.total = resp.pagination.total
        self.next = resp.pagination.next
        self.page = resp.events


class ActivityLogAPI(APIEndpoint):
    _path = "/audit-log/v1/events"

    def _get_events(self, *, params: ActivityLogQueryParams) -> ActivityLogResponse:
        return self._get(params=params, response_model=ActivityLogResponse)

    def get(
        self,
        *,
        filters: list[tuple[str, str, str] | str | ActivityLogFilter] | None = None,
        filter_type: Literal["and", "or"] | None = None,
        limit: int = 500,
        sort: str | tuple[str, str] | ActivityLogSort | None = None,
    ) -> ActivityLogIterator:
        """
        Query Activity Log Events.

        Args:
            filters: list of filters to sub-select the events to return.
            filter_type:
                If multiple filters are used, should the filters be combined as a logical
                `and` or an `or`?
            limit: The number of events to return per page.
            sort: How should the events be sorted in the response?

        Returns:
            Iterator supporting pagination of the event data.
        """
        params = ActivityLogQueryParams.model_validate(
            {
                "filters": filters,
                "filter_type": filter_type,
                "limit": limit,
                "sort": sort,
            }
        )
        return ActivityLogIterator(self._client, params=params)


class AsyncActivityLogAPI(AsyncAPIEndpoint):
    _path = "/audit-log/v1/events"

    async def _get_events(
        self, *, params: ActivityLogQueryParams
    ) -> ActivityLogResponse:
        return await self._get(params=params, response_model=ActivityLogResponse)

    async def get(
        self,
        *,
        filters: list[tuple[str, str, str] | str | ActivityLogFilter] | None = None,
        filter_type: Literal["and", "or"] | None = None,
        limit: int = 500,
        sort: str | tuple[str, str] | ActivityLogSort | None = None,
    ) -> AsyncActivityLogIterator:
        """
        Query Activity Log Events.

        Args:
            filters: list of filters to sub-select the events to return.
            filter_type:
                If multiple filters are used, should the filters be combined as a logical
                `and` or an `or`?
            limit: The number of events to return per page.
            sort: How should the events be sorted in the response?

        Returns:
            Iterator supporting pagination of the event data.
        """
        params = ActivityLogQueryParams.model_validate(
            {
                "filters": filters,
                "filter_type": filter_type,
                "limit": limit,
                "sort": sort,
            }
        )
        return AsyncActivityLogIterator(self._client, params=params)
