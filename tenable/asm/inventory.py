"""
Inventory
=========

Methods described in this section relate to the inventory API and can be accessed at
``TenableASM.inventory``.

.. rst-class:: hide-signature
.. autoclass:: InventoryAPI
    :members:

.. autoclass:: InventoryIterator
    :members:
"""
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
from copy import copy
from tenable.base.endpoint import APIEndpoint
from restfly.iterator import APIIterator

if TYPE_CHECKING:
    from .session import TenableASM
    from box import BoxList


class InventoryIterator(APIIterator):
    """
    Asset inventory iterator
    """
    _after_asset_id: str = '0000000000'
    _filters: List[Dict[str, str]]
    _query: Dict[str, Any]
    _api: 'TenableASM'
    page: 'BoxList'
    limit: int = 1000
    total: int
    stats: Dict[str, Any]

    def _get_page(self):
        query = copy(self._query)
        if not query.get('after'):
            query['after'] = self._after_asset_id

        query['limit'] = self.limit
        resp = self._api.post('inventory', params=query, json=self._filters)
        self.page = resp.assets
        self.total = resp.total
        self.stats = resp.stats

        if self.page:
            self._after_asset_id = self.page[-1].id



class InventoryAPI(APIEndpoint):
    def list(self,
             *search: Tuple[str, str, str],
             columns: Optional[List[str]] = None,
             size: int = 1000,
             sort_field: Optional[str] = None,
             sort_asc: bool = True,
             inventory: bool = False,
             ) -> InventoryIterator:
        """
        Lists the assets in the inventory

        Args:
            *search (tuple[str, str, str], optional):
                A 3-part search tuple detailing what to search for from the ASM
                dataset.  For example:
                ``('bd.original_hostname', 'ends with', '.com')``
            columns (list[str], optional):
                The list of columns to return in the response.
            size (int, optional):
                The number of records to return with each page from the API.  Must be
                an integer between `1` and `10000`.
            sort_field (str, optional):
                What field should the results be worted by?
            sort_asc (bool):
                How should the results be sorted?  ``True`` specifies ascending sort,
                whereas ``False`` refers to descending.

        Example:
            >>> for item in asm.inventory.list():
            ...     print(item)
        """
        if not columns:
            columns = [
                'bd.original_hostname',
                'bd.severity_ranking',
                'bd.hostname',
                'bd.record_type',
                'bd.ip_address',
                'id',
                'bd.addedtoportfolio',
                'bd.smartfolders',
                'bd.app_updates',
                'ports.ports',
                'screenshot.redirect_chain',
                'screenshot.finalurl',
                'ports.cves',
            ]
        return InventoryIterator(
            self._api,
            _query={
                'columns': ','.join(columns),
                'inventory': str(bool(inventory)).lower(),
                'sortorder': str(bool(sort_asc)).lower(),
                'sortby': sort_field,
            },
            _filters = [{'column': c, 'type': t, 'value': v} for c, t, v in search],
            limit=size
        )
