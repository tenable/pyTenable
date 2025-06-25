import pytest


@pytest.fixture
def cards(tenable_one_api):
    return tenable_one_api.exposure_view.cards