'''conftest'''
import os

import pytest

from tenable.tenableone import TenableOne


@pytest.fixture
def tenable_one_api():
    '''api key fixture'''
    return TenableOne(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')
