'''conftest'''
import os

import pytest

from tenable.tenableone import TenableExposureManagement


@pytest.fixture
def tenable_exposure_management_api():
    '''api key fixture'''
    return TenableExposureManagement(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')
