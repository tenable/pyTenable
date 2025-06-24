from datetime import datetime

import pytest
import responses

from tenable.tenableone.exposure_view.cards.schema import CESGrade, CardDetails, ExposureClass, SlaSeverityLevel, \
    Timeframe, SlaBreakdownFilter
from tenable.tenableone.inventory.schema import SortDirection


@pytest.fixture
def cards_response() -> dict:
    return {
        "data": [
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


@responses.activate
def test_list(cards, cards_response):
    # Arrange
    is_global_card = True
    page_number = 1
    page_size = 25
    sorting_order = SortDirection.ASC

    # Build the expected query parameters
    params = {
        "is_global_card": is_global_card,
        "page_number": page_number,
        "page_size": page_size,
        "sorting_order": sorting_order.value
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.query_param_matcher(params)]
    )

    # Act
    result = cards.list(
        is_global_card=is_global_card,
        page_number=page_number,
        page_size=page_size,
        sorting_order=sorting_order
    )

    # Assert
    assert len(result.data) == 2
    assert result.data[0].card_name == "Global Card"
    assert result.data[0].is_global is True
    assert result.data[0].ces_score.score == 750
    assert result.data[0].ces_score.grade == CESGrade.B
    assert result.data[1].card_name == "Custom Card"
    assert result.data[1].is_global is False
    assert result.pagination.page_number == 1
    assert result.pagination.page_size == 25


@responses.activate
def test_should_pass_request_parameters_for_text_search(cards, cards_response):
    # Arrange
    query_text = "test"
    
    # Build the expected query parameters with text query
    params = {
        "text_query": query_text,
        "page_number": 1,
        "page_size": 25,
        "sorting_order": SortDirection.ASC.value
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.query_param_matcher(params)]
    )

    # Act
    result = cards.list(query_text=query_text)

    # Assert
    assert len(result.data) == 2
    assert result.data[0].card_name == "Global Card"
    assert result.data[1].card_name == "Custom Card"


@responses.activate
def test_should_pass_request_parameters_for_DESC_sorting(cards, cards_response):
    # Arrange
    sorting_order = SortDirection.DESC
    
    # Build the expected query parameters with DESC sorting
    params = {
        "page_number": 1,
        "page_size": 25,
        "sorting_order": sorting_order.value
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.query_param_matcher(params)]
    )

    # Act
    result = cards.list(sorting_order=sorting_order)

    # Assert
    assert len(result.data) == 2
    assert result.data[0].card_name == "Global Card"
    assert result.data[1].card_name == "Custom Card"


@responses.activate
def test_list_default_parameters(cards, cards_response):
    # Arrange - test with minimal parameters
    # Default query parameters with no optional parameters specified
    params = {
        "page_number": 1,
        "page_size": 25,
        "sorting_order": SortDirection.ASC.value
    }

    responses.add(
        responses.GET,
        'https://cloud.tenable.com/api/v1/t1/exposure-view/cards',
        json=cards_response,
        match=[responses.matchers.query_param_matcher(params)]
    )

    # Act
    result = cards.list()

    # Assert
    assert len(result.data) == 2
    assert result.data[0].card_name == "Global Card"
    assert result.data[1].card_name == "Custom Card"


@pytest.fixture
def card_details_response() -> dict:
    return {
        "card_id": 1,
        "card_name": "Global Card",
        "is_global": True,
        "ces_score": {
            "score": 750,
            "grade": "B"
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
        "exposure_classes_details": {
            "ALL": {
                "score_benchmark": {
                    "industry_benchmark": {
                        "industry_id": 1,
                        "ces_score": {
                            "score": 800,
                            "grade": "A"
                        }
                    },
                    "population_benchmark": {
                        "score": 700,
                        "grade": "B"
                    }
                },
                "asset_risk_breakdown": {
                    "critical": 10.0,
                    "high": 20.0,
                    "medium_low": 70.0
                },
                "score_trend_metric": {
                    "ces_trend": [
                        {
                            "date": "2024-01-01T00:00:00Z",
                            "ces_score": {
                                "score": 750,
                                "grade": "B"
                            }
                        }
                    ],
                    "target_score": 800
                },
                "sla_efficiency": [
                    {
                        "sla_severity_level": "CRITICAL",
                        "sla_inside_count": 5,
                        "sla_total_count": 10,
                        "sla_efficiency": 50.0,
                        "sla_efficiency_target": 80.0
                    }
                ],
                "sla_breakdown": {
                    "risk_distribution": {
                        "risk_inside_sla": {
                            "number_of_risks": 5,
                            "percentage_of_total": 50.0
                        },
                        "risks_outside_sla": {
                            "number_of_risks": 5,
                            "percentage_of_total": 50.0
                        }
                    },
                    "risk_distribution_in_days": {
                        "inside_sla": 3,
                        "outside_sla": 7
                    },
                    "exposure_category_breakdown": [
                        {
                            "exposure_class": "ALL",
                            "contribution_percentage": 100.0
                        }
                    ],
                    "top_affecting_tags": [
                        {
                            "id": "tag1",
                            "name": "Critical Tag"
                        }
                    ]
                }
            }
        }
    }


@responses.activate
def test_get_by_id(cards, card_details_response):
    # Arrange
    card_id = "1"
    trend_timeframe = Timeframe(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 31)
    )
    sla_efficiency_timeframe = Timeframe(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 31)
    )
    sla_breakdown_filter = SlaBreakdownFilter.REMEDIATED
    include_trend_events = True

    # Build the expected query parameters
    params = {
        "trend_start_date": "2024-01-01T00:00:00",
        "trend_end_date": "2024-01-31T00:00:00",
        "sla_efficiency_start_date": "2024-01-01T00:00:00",
        "sla_efficiency_end_date": "2024-01-31T00:00:00",
        "sla_breakdown_filter": "REMEDIATED",
        "include_trend_events": True
    }

    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/exposure-view/cards/{card_id}',
        json=card_details_response,
        match=[responses.matchers.query_param_matcher(params)]
    )

    # Act
    result = cards.get_by_id(
        card_id=card_id,
        trend_timeframe=trend_timeframe,
        sla_efficiency_timeframe=sla_efficiency_timeframe,
        sla_breakdown_filter=sla_breakdown_filter,
        include_trend_events=include_trend_events
    )

    # Assert
    assert isinstance(result, CardDetails)
    assert result.card_id == 1
    assert result.card_name == "Global Card"
    assert result.is_global is True
    assert result.ces_score.score == 750
    assert result.ces_score.grade == CESGrade.B

    # Test exposure classes details
    exposure_details = result.exposure_classes_details[ExposureClass.ALL]
    assert exposure_details.score_benchmark.industry_benchmark.industry_id == 1
    assert exposure_details.score_benchmark.industry_benchmark.ces_score.score == 800
    assert exposure_details.score_benchmark.industry_benchmark.ces_score.grade == CESGrade.A
    assert exposure_details.score_benchmark.population_benchmark.score == 700
    assert exposure_details.score_benchmark.population_benchmark.grade == CESGrade.B

    # Test asset risk breakdown
    assert exposure_details.asset_risk_breakdown.critical == 10.0
    assert exposure_details.asset_risk_breakdown.high == 20.0
    assert exposure_details.asset_risk_breakdown.medium_low == 70.0

    # Test score trend metric
    assert len(exposure_details.score_trend_metric.ces_trend) == 1
    assert exposure_details.score_trend_metric.target_score == 800

    # Test SLA efficiency
    assert len(exposure_details.sla_efficiency) == 1
    sla_stat = exposure_details.sla_efficiency[0]
    assert sla_stat.sla_severity_level == SlaSeverityLevel.CRITICAL
    assert sla_stat.sla_inside_count == 5
    assert sla_stat.sla_total_count == 10
    assert sla_stat.sla_efficiency == 50.0
    assert sla_stat.sla_efficiency_target == 80.0

    # Test SLA breakdown
    assert exposure_details.sla_breakdown.risk_distribution.risk_inside_sla.number_of_risks == 5
    assert exposure_details.sla_breakdown.risk_distribution.risk_inside_sla.percentage_of_total == 50.0
    assert exposure_details.sla_breakdown.risk_distribution.risks_outside_sla.number_of_risks == 5
    assert exposure_details.sla_breakdown.risk_distribution.risks_outside_sla.percentage_of_total == 50.0
    assert exposure_details.sla_breakdown.risk_distribution_in_days.inside_sla == 3
    assert exposure_details.sla_breakdown.risk_distribution_in_days.outside_sla == 7
    assert len(exposure_details.sla_breakdown.exposure_category_breakdown) == 1
    assert exposure_details.sla_breakdown.exposure_category_breakdown[0].exposure_class == ExposureClass.ALL
    assert exposure_details.sla_breakdown.exposure_category_breakdown[0].contribution_percentage == 100.0
    assert len(exposure_details.sla_breakdown.top_affecting_tags) == 1
    assert exposure_details.sla_breakdown.top_affecting_tags[0].id == "tag1"
    assert exposure_details.sla_breakdown.top_affecting_tags[0].name == "Critical Tag"


@responses.activate
def test_get_by_id_minimal_parameters(cards, card_details_response):
    # Arrange
    card_id = "1"

    # Build the expected query parameters with minimal parameters
    params = {
        "sla_breakdown_filter": "ANY",
        "include_trend_events": False
    }

    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/api/v1/t1/exposure-view/cards/{card_id}',
        json=card_details_response,
        match=[responses.matchers.query_param_matcher(params)]
    )

    # Act
    result = cards.get_by_id(card_id=card_id)

    # Assert
    assert isinstance(result, CardDetails)
    assert result.card_id == 1
    assert result.card_name == "Global Card"
    assert result.is_global is True
