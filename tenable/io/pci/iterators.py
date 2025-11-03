from copy import deepcopy
from typing import TYPE_CHECKING, Any
from uuid import UUID

from restfly.iterator import APIIterator

if TYPE_CHECKING:
    from tenable.io import TenableIO


class PCIBaseIterator(APIIterator):
    _api: 'TenableIO'
    url: str
    params: dict[str, Any]
    envelope: str
    offset: int = 0
    limit: int = 1000

    def _get_page(self) -> None:
        params = deepcopy(self.params)
        params['offset'] = self.offset
        params['limit'] = self.limit
        resp = self._api.get(self.url, params=self.params).json()
        self.total = resp['pagination']['total']
        self.page = resp[self.envelope]
        self.offset += self.limit


class PCIAttestationsIterator(PCIBaseIterator):
    envelope: str = 'attestations'


class PCIDisputesIterator(PCIBaseIterator):
    attestation_id: UUID
    envelope: str = 'disputes'


class PCIUndisputedFailuresIterator(PCIDisputesIterator):
    envelope: str = 'failures'


class PCIAttestationAssetsIterator(PCIDisputesIterator):
    envelope: str = 'assets'


class PCIScansIterator(PCIBaseIterator):
    envelope: str = 'scans'
