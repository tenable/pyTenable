"""
Cards
=====
Methods described in this section relate to the exposure view cards API.
These methods can be accessed at ``TenableExposureManagement.exposure_view.cards``.

.. rst-class:: hide-signature
.. autoclass:: CardsAPI
    :members:
"""

from typing import Optional

from restfly import APIEndpoint

from tenable.tenableone.exposure_view.cards.schema import (
    Cards,
    CardDetails,
    SlaBreakdownFilter,
    Timeframe,
)
from tenable.tenableone.inventory.schema import SortDirection


class CardsAPI(APIEndpoint):
    def list(
        self,
        is_global_card: Optional[bool] = None,
        query_text: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 25,
        sorting_order: Optional[SortDirection] = SortDirection.ASC,
    ) -> Cards:
        """
        List cards based on filter criteria

        Args:
            is_global_card: Filter cards by is_global flag
            query_text: Text query to filter cards
            offset: The number of items to skip before starting to collect the result set
            limit: Max number of items to return
            sorting_order: Sorting direction (ASC or DESC)

        Returns:
            Cards object containing the list of cards and pagination info
        """
        params = {
            'offset': offset,
            'limit': limit,
            'sorting_order': sorting_order.value,
        }

        if is_global_card is not None:
            params['is_global_card'] = is_global_card
        if query_text is not None:
            params['text_query'] = query_text

        cards_response = self._get(
            path='api/v1/t1/exposure-view/cards', params=params, box=False
        )

        return Cards(**cards_response.json())

    def get_by_id(
            self,
            card_id: str,
            trend_timeframe: Optional[Timeframe] = None,
            sla_efficiency_timeframe: Optional[Timeframe] = None,
            sla_breakdown_filter: Optional[SlaBreakdownFilter] = SlaBreakdownFilter.ANY,
            include_trend_events: Optional[bool] = False
    ) -> CardDetails:
        """
        Get a specific card by its ID with optional filters

        Args:
            card_id: The ID of the card to retrieve
            trend_timeframe: Optional timeframe for trend data
            sla_efficiency_timeframe: Optional timeframe for SLA efficiency data
            sla_breakdown_filter: Optional filter for SLA breakdown (ANY, REMEDIATED, NON_REMEDIATED)
            include_trend_events: Whether to include trend events in the response

        Returns:
            CardDetails object containing the card details
        """
        params = {
            "sla_breakdown_filter": sla_breakdown_filter.value,
            "include_trend_events": include_trend_events
        }

        if trend_timeframe:
            params["trend_start_date"] = trend_timeframe.start_date.isoformat()
            params["trend_end_date"] = trend_timeframe.end_date.isoformat()
        if sla_efficiency_timeframe:
            params["sla_efficiency_start_date"] = sla_efficiency_timeframe.start_date.isoformat()
            params["sla_efficiency_end_date"] = sla_efficiency_timeframe.end_date.isoformat()

        card_response = self._get(path=f"api/v1/t1/exposure-view/cards/{card_id}", params=params, box=False)
        return CardDetails(**card_response.json())
