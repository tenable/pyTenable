'''conftest'''
import os

import pytest

from tenable.apa import TenableAPA


@pytest.fixture
def api():
    '''api key fixture'''
    return TenableAPA(
        os.getenv('TIO_TEST_ADMIN_ACCESS', 'ffffffffffffffffffffffffffffffff'),
        os.getenv('TIO_TEST_ADMIN_SECRET', 'ffffffffffffffffffffffffffffffff'),
        vendor='pytest',
        product='pytenable-automated-testing')
