"""
Attestations
============

The following methods allow for interaction into the TVM
:devportal:`PCI Attestation API <pci-attestations>` API endpoints.

Methods available on ``tio.pci.attestations``:

.. rst-class:: hide-signature
.. autoclass:: AttestationsAPI
    :members:

"""

from typing import Any, List, Literal, Type
from uuid import UUID

from ..base import TIOEndpoint
from .iterators import (
    PCIAttestationAssetsIterator,
    PCIAttestationsIterator,
    PCIDisputesIterator,
    PCIUndisputedFailuresIterator,
)


class AttestationsAPI(TIOEndpoint):
    _path = 'pci-asv/attestations'

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
        status_type: list[
            Literal[
                'IN_PROGRESS',
                'NEEDS_WORK',
                'IN_REVIEW',
                'INFO_REQUESTED',
                'INFO_PROVIDED',
                'FAILED',
                'PASSED',
                'CLOSED',
            ]
        ]
        | None = None,
        sort: list[tuple[str, Literal['asc', 'desc']]] | None = None,
        limit: int = 1000,
        offset: int = 0,
        iterator: Type[PCIAttestationsIterator] | None = PCIAttestationsIterator,
    ) -> PCIAttestationsIterator | dict[str, Any]:
        """
        Returns a list of PCI attestations.

        Args:
            status_type:
                Filters the attestations based on the status types defined.
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
            'status_type': status_type,
        }
        if iterator:
            return iterator(
                self._api,
                url=f'{self._path}/{path}',
                params=params,
                offset=offset,
                limit=limit,
            )
        return self._get(path, params=params, conv_json=True)

    def details(self, id: UUID | str) -> dict[str, Any]:
        """
        Retrieves the details of a specific attestation.

        Args:
            id: The attestation UUID to retrieve.
        """
        return self._get(f'details/{str(id)}').json()

    def disputes(
        self,
        id: UUID | str,
        *,
        sort: List[tuple[str, Literal['asc', 'desc']]] | None = None,
        limit: int = 1000,
        offset: int = 0,
        iterator: Type[PCIDisputesIterator] | None = PCIDisputesIterator,
    ) -> PCIDisputesIterator | dict[str, Any]:
        """
        Retrieves the list of disputes for the attestation ID provided.

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
        path = f'details/{str(id)}/disputes'
        params = {'sort': self._format_sorts(sort), 'limit': limit, 'offset': offset}
        if iterator:
            return iterator(
                self._api,
                url=f'{self._path}/{path}',
                attestations_id=id,
                params=params,
                offset=offset,
                limit=limit,
            )
        return self._get(path, params=params).json()

    def failures(
        self,
        id: UUID | str,
        *,
        sort: List[tuple[str, Literal['asc', 'desc']]] | None = None,
        limit: int = 1000,
        offset: int = 0,
        iterator: Type[PCIUndisputedFailuresIterator]
        | None = PCIUndisputedFailuresIterator,
    ) -> PCIUndisputedFailuresIterator | dict[str, Any]:
        """
        Retrieves the list of undisputed failures for the attestation ID provided.

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
        path = f'{str(id)}/failures/undisputed/list'
        params = {'sort': self._format_sorts(sort), 'limit': limit, 'offset': offset}
        if iterator:
            return iterator(
                self._api,
                url=f'{self._path}/{path}',
                attestations_id=id,
                params=params,
                offset=offset,
                limit=limit,
            )
        return self._get(path, params=params).json()

    def assets(
        self,
        id: UUID | str,
        *,
        sort: List[tuple[str, Literal['asc', 'desc']]] | None = None,
        limit: int = 1000,
        offset: int = 0,
        iterator: Type[PCIAttestationAssetsIterator]
        | None = PCIAttestationAssetsIterator,
    ) -> PCIAttestationAssetsIterator | dict[str, Any]:
        """
        Retrieves the list of assets associated to the attestation ID provided.

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
        path = f'{str(id)}/assets/list'
        params = {'sort': self._format_sorts(sort), 'limit': limit, 'offset': offset}
        if iterator:
            return iterator(
                self._api,
                url=f'{self._path}/{path}',
                attestations_id=id,
                params=params,
                offset=offset,
                limit=limit,
            )
        return self._get(path, params=params).json()
