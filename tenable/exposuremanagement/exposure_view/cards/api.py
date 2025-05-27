from typing import Optional

from restfly import APIEndpoint

from tenable.exposuremanagement.exposure_view.cards.schema import CardFilter, Cards, Pagination, CardsResponse
from tenable.exposuremanagement.inventory.schema import SortDirection


class CardsAPI(APIEndpoint):
    @property
    def list(
            self,
            is_global: bool = None,
            query_text: Optional[str] = None,
            page_number: int = 1,
            page_size: int = 20,
            sort_direction: Optional[SortDirection] = None
    ) -> Cards:
        payload = {"filter": CardFilter(), "pagination": Pagination(),
                   "sort_direction": sort_direction.value if sort_direction else SortDirection.ASC.value}
        if is_global is not None:
            payload["filter"].is_global = is_global
        if query_text is not None:
            payload["filter"].text_query = query_text
        if page_number is not None:
            payload["pagination"].page_number = page_number
        if page_size is not None:
            payload["pagination"].page_size = page_size

        cards_response: dict = self._post(path="/api/v1/em/exposure-view/cards", json=payload)
        return CardsResponse(**cards_response).data
