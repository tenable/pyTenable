import pytest
import responses

from tenable.exposuremanagement.exposure_view.cards.schema import CESGrade
from tenable.exposuremanagement.inventory.schema import SortDirection


@pytest.fixture
def cards_response() -> dict:
    return {
        "data": {
            "cards": [
                {
                    "card_id": 1,
                    "card_name": "Global Card",
                    "card_type": "GLOBAL",
                    "is_global": True,
                    "ces_score": {
                        "score": 750,
                        "grade": "B"
                    },
                    "sla_percentage": 85.5,
                    "ces_trend": [],
                    "tag_count": 3,
                    "exposures": ["VM", "CLOUD"],
                    "last_data_update_date": "2023-09-15T12:30:45Z",
                    "created_at": "2023-08-01T10:00:00Z",
                    "updated_at": "2023-09-15T12:30:45Z",
                    "sources": ["T.IO", "CLOUD"]
                },
                {
                    "card_id": 2,
                    "card_name": "Custom Card",
                    "card_type": "CUSTOM",
                    "is_global": False,
                    "ces_score": {
                        "score": 650,
                        "grade": "C"
                    },
                    "sla_percentage": 72.5,
                    "ces_trend": [],
                    "tag_count": 5,
                    "exposures": ["VM"],
                    "last_data_update_date": "2023-09-14T08:15:30Z",
                    "created_at": "2023-08-10T14:20:00Z",
                    "updated_at": "2023-09-14T08:15:30Z",
                    "sources": ["T.IO"]
                }
            ],
            "pagination": {
                "page_number": 1,
                "page_size": 25
            }
        }
    }


@responses.activate
def test_list(cards, cards_response):
    # Arrange
    is_global_card = True
    page_number = 1
    page_size = 25
    sorting_order = SortDirection.ASC

    # Build the expected payload - update to match what the API actually sends
    payload = {
        "filter": {
            "is_global_card": is_global_card
        },
        "pagination": {
            "page_number": page_number,
            "page_size": page_size
        },
        "sorting_order": sorting_order.value
    }

    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.json_params_matcher(payload)]
    )

    # Act
    result = cards.list(
        is_global_card=is_global_card,
        page_number=page_number,
        page_size=page_size,
        sorting_order=sorting_order
    )

    # Assert
    assert len(result.cards) == 2
    assert result.cards[0].card_name == "Global Card"
    assert result.cards[0].is_global is True
    assert result.cards[0].ces_score.score == 750
    assert result.cards[0].ces_score.grade == CESGrade.B
    assert result.cards[1].card_name == "Custom Card"
    assert result.cards[1].is_global is False
    assert result.pagination.page_number == 1
    assert result.pagination.page_size == 25


@responses.activate
def test_should_pass_request_parameters_for_text_search(cards, cards_response):
    # Arrange
    query_text = "test"
    
    # Build the expected payload with text query
    payload = {
        "filter": {
            "text_query": query_text
        },
        "pagination": {
            "page_number": 1,
            "page_size": 25
        },
        "sorting_order": SortDirection.ASC.value
    }

    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.json_params_matcher(payload)]
    )

    # Act
    result = cards.list(query_text=query_text)

    # Assert
    assert len(result.cards) == 2
    assert result.cards[0].card_name == "Global Card"
    assert result.cards[1].card_name == "Custom Card"


@responses.activate
def test_should_pass_request_parameters_for_DESC_sorting(cards, cards_response):
    # Arrange
    sorting_order = SortDirection.DESC
    
    # Build the expected payload with DESC sorting
    payload = {
        "filter": {},
        "pagination": {
            "page_number": 1,
            "page_size": 25
        },
        "sorting_order": sorting_order.value
    }

    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.json_params_matcher(payload)]
    )

    # Act
    result = cards.list(sorting_order=sorting_order)

    # Assert
    assert len(result.cards) == 2
    assert result.cards[0].card_name == "Global Card"
    assert result.cards[1].card_name == "Custom Card"


@responses.activate
def test_list_default_parameters(cards, cards_response):
    # Arrange - test with minimal parameters
    # Default payload with no optional parameters specified
    payload = {
        "filter": {},
        "pagination": {
            "page_number": 1,
            "page_size": 25
        },
        "sorting_order": SortDirection.ASC.value
    }

    responses.add(
        responses.POST,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.json_params_matcher(payload)]
    )

    # Act
    result = cards.list()

    # Assert
    assert len(result.cards) == 2
    assert result.cards[0].card_name == "Global Card"
    assert result.cards[1].card_name == "Custom Card"
