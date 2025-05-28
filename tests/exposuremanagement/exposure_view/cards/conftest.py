import pytest

from tenable.exposuremanagement.exposure_view.cards.api import CardsAPI


@pytest.fixture
def cards(tenable_exposure_management_api):
    return tenable_exposure_management_api.exposure_view.cards