import pytest


@pytest.mark.vcr()
def test_get_licensed(api):
    """test to get licensed scanned assets count"""
    data = api.display.get_licensed()
    assert data == 2502
