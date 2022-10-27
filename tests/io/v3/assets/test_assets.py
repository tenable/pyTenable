import os
import pytest

from tenable.io import TenableIO
from tests.pytenable_log_handler import setup_logging_to_file


@pytest.fixture
def api():
    """
    Fixture for setting up API Keys
    """
    setup_logging_to_file()
    return TenableIO(
        os.getenv('TIO_TEST_ADMIN_ACCESS', ''),
        os.getenv('TIO_TEST_ADMIN_SECRET', ''),
        vendor='pytest',
        product='pytenable-automated-testing')


@pytest.mark.vcr()
def test_get_asset_uuids(api):
    """
    Test case to fetch asset_uuids
    """

    asset_uuids = api.v3.assets.get_asset_uuids(filter=('and', ('tags', 'eq', ['de2e56a2-6a0e-4757-8d00-e9ad635f6231']),
                                                        ('tags', 'neq', ['f038fd3a-a844-438f-b7a7-7acc6369f3e9'])))
    assert len(asset_uuids) == 2
