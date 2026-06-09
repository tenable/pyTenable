"""
Scans
=====

The following methods allow for interaction into the TVM
:devportal:`PCI Scans API <pci-scans>` API endpoints.

Methods available on ``tio.pci.scans``:

.. rst-class:: hide-signature
.. autoclass:: ScansAPI
    :members:

"""

from typing import Any, Literal, Type

from ..base import TIOEndpoint
from .iterators import PCIScansIterator


class ScansAPI(TIOEndpoint):
    _path = 'pci-asv/scans'

    @staticmethod
    def _format_sorts(
        sort: list[tuple[str, Literal['asc', 'desc']]] | None,
    ) -> str | None:
        """
        Formats the sort tuple into the expected string format for the API.
        """
        return ','.join([f'{n}:{d}' for n, d in sort]) if sort else None

    def list(
        self,
        *,
        sort: list[tuple[str, Literal['asc', 'desc']]] | None = None,
        limit: int = 1000,
        offset: int = 0,
        iterator: Type[PCIScansIterator] | None = PCIScansIterator,
    ) -> PCIScansIterator | dict[str, Any]:
        """
        Returns a list of PCI scans.

        Args:
            sort:
                Sort the results based on the field and sort order.
            limit:
                The number of results to return for each page
            offset:
                Where within the page data to start the page.
            iterator:
                Should an iterator be returned or a page of data? If set to `None`,
                the page will be returned instead of the iterable.
        """
        path = 'list'
        params = {
            'sort': self._format_sorts(sort),
            'limit': limit,
            'offset': offset,
        }
        if iterator:
            return iterator(
                self._api,
                url=f'{self._path}/{path}',
                params=params,
                offset=offset,
                limit=limit,
            )
        return self._get(path, params=params).json()
