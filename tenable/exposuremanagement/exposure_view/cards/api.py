from typing import Optional

from restfly import APIEndpoint

from tenable.exposuremanagement.exposure_view.cards.schema import CardFilter, Cards, Pagination, CardsResponse
from tenable.exposuremanagement.inventory.schema import SortDirection


class CardsAPI(APIEndpoint):
    def list(
            self,
            is_global_card: Optional[bool] = None,
            query_text: Optional[str] = None,
            page_number: Optional[int] = 1,
            page_size: Optional[int] = 25,
            sorting_order: Optional[SortDirection] = SortDirection.ASC
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
        payload = {
            "filter": {},
            "pagination": {
                "page_number": page_number,
                "page_size": page_size
            },
            "sorting_order": sorting_order.value
        }
        
        # Add filter parameters if provided
        if is_global_card is not None:
            payload["filter"]["is_global_card"] = is_global_card
        if query_text is not None:
            payload["filter"]["text_query"] = query_text

        # Make the API request
        cards_response = self._post(path="api/v1/em/exposure-view/cards", json=payload)
        
        # If the response is a Box object, convert it to a dict first
        if hasattr(cards_response, 'to_dict'):
            cards_response = cards_response.to_dict()
        
        # Parse the response into a CardsResponse object and return its data attribute
        return CardsResponse(**cards_response).data
