import pytest


@pytest.mark.vcr()
def test_get_asset_uuids(api):
    """
    Test case to fetch asset_uuids
    """

    asset_uuids = api.v3.assets.get_asset_uuids(filter=('and', ('tags', 'eq', ['de2e56a2-6a0e-4757-8d00-e9ad635f6231']),
                                                        ('tags', 'neq', ['f038fd3a-a844-438f-b7a7-7acc6369f3e9'])))
    assert len(asset_uuids) == 2
