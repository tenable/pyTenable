'''conftest'''
import os

import pytest

from tenable.exposure_management.inventory import TenableInventory


@pytest.fixture
def api():
    '''api key fixture'''
    return TenableInventory(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')
