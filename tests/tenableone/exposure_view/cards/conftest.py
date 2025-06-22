import pytest


@pytest.fixture
def cards(tenable_exposure_management_api):
    return tenable_exposure_management_api.exposure_view.cards