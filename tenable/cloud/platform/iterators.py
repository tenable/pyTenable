from copy import copy
from typing import Callable

from restfly import APIIterator, APIModel, AsyncAPIIterator

from .models.pagination_v1 import PageV1Response, PaginationV1Query


class PaginationV1Iterator(APIIterator):
    _path: str
    _method: str
    _request: Callable[[str, PaginationV1Query], PageV1Response]
    page: list[APIModel]
    params: PaginationV1Query

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        obj = self._client
        for key in self._method.split("."):
            obj = getattr(obj, key)
            if obj is None:
                raise TypeError(f"{self._method} is not a valid callable path.")
        self._request = obj

    def _get_page(self) -> None:
        params = copy(self.params)
        params.offset = self.count if self.count > 0 else None
        resp = self._request(path=self.path, params=params)
        self.total = resp.pagination.total
        self.page = resp.items


class AsyncPaginationV1Iterator(AsyncAPIIterator):
    _path: str
    _method: str
    _request: Callable[[str, PaginationV1Query], PageV1Response]
    page: list[APIModel]
    params: PaginationV1Query

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        obj = self._client
        for key in self._method.split("."):
            obj = getattr(obj, key)
            if obj is None:
                raise TypeError(f"{self._method} is not a valid callable path.")
        self._request = obj

    async def _get_page(self) -> None:
        params = copy(self.params)
        params.offset = self.count if self.count > 0 else None
        resp = await self._request(path=self.path, params=params)
        self.total = resp.pagination.total
        self.page = resp.items
