"""
Findings
========
Methods described in this section relate to the exposure view cards API.
These methods can be accessed at ``TenableExposureManagement.exposure_view.cards``.

.. rst-class:: hide-signature
.. autoclass:: CardsAPI
    :members:
"""

from typing import Optional

from restfly import APIEndpoint

from tenable.tenableone.exposure_view.cards.schema import Cards, Timeframe, SlaBreakdownFilter, GetCardByIdResponse
from tenable.tenableone.inventory.schema import SortDirection


class CardsAPI(APIEndpoint):
    def list(
        self,
        is_global_card: Optional[bool] = None,
        query_text: Optional[str] = None,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 25,
        sorting_order: Optional[SortDirection] = SortDirection.ASC,
    ) -> Cards:
        """
        List cards based on filter criteria

        Args:
            is_global_card: Filter cards by is_global flag
            query_text: Text query to filter cards
            page_number: Page number for pagination
            page_size: Number of items per page
            sorting_order: Sorting direction (ASC or DESC)

        Returns:
            Cards object containing the list of cards and pagination info
        """
        params = {
            'page_number': page_number,
            'page_size': page_size,
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
    ) -> GetCardByIdResponse:
        """
        Get a specific card by its ID with optional filters

        Args:
            card_id: The ID of the card to retrieve
            trend_timeframe: Optional timeframe for trend data
            sla_efficiency_timeframe: Optional timeframe for SLA efficiency data
            sla_breakdown_filter: Optional filter for SLA breakdown (ANY, REMEDIATED, NON_REMEDIATED)
            include_trend_events: Whether to include trend events in the response

        Returns:
            GetCardByIdResponse object containing the card details
        """
        payload = {
            "id": card_id,
            "get_card_request": {
                "sla_breakdown_filter": sla_breakdown_filter.value,
                "include_trend_events": include_trend_events
            }
        }

        if trend_timeframe:
            payload["get_card_request"]["trend_timeframe"] = {
                "start_date": trend_timeframe.start_date.isoformat(),
                "end_date": trend_timeframe.end_date.isoformat()
            }
        if sla_efficiency_timeframe:
            payload["get_card_request"]["sla_efficiency_timeframe"] = {
                "start_date": sla_efficiency_timeframe.start_date.isoformat(),
                "end_date": sla_efficiency_timeframe.end_date.isoformat()
            }

        card_response = self._post(path=f"api/v1/t1/exposure-view/cards/{card_id}", json=payload, box=False)
        return GetCardByIdResponse(**card_response.json())
