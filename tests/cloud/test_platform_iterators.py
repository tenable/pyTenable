import pytest

from tenable.cloud.platform.iterators import AsyncPaginationV1Iterator, PaginationV1Iterator
from tenable.cloud.platform.models.pagination_v1 import PaginationV1Query


class _NullClient:
    null_attr = None


class _SyncBadIterator(PaginationV1Iterator):
    _method = "null_attr"
    path: str = "/test"
    params: PaginationV1Query = PaginationV1Query(limit=10)  # type: ignore[assignment]


class _AsyncBadIterator(AsyncPaginationV1Iterator):
    _method = "null_attr"
    path: str = "/test"
    params: PaginationV1Query = PaginationV1Query(limit=10)  # type: ignore[assignment]


def test_sync_iterator_none_method_raises():
    with pytest.raises(TypeError, match="null_attr is not a valid callable path"):
        _SyncBadIterator(
            _NullClient(),
            path="/test",
            params=PaginationV1Query(limit=10),
        )


def test_async_iterator_none_method_raises():
    with pytest.raises(TypeError, match="null_attr is not a valid callable path"):
        _AsyncBadIterator(
            _NullClient(),
            path="/test",
            params=PaginationV1Query(limit=10),
        )
