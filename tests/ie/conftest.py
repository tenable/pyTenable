'''conftest'''
import os

import pytest

from tenable.ie.session import TenableIE

RE_BASE = 'https://pytenable.tenable.ad/api'


@pytest.fixture
def api():
    '''api key fixture'''
    return TenableIE(
        api_keys=os.getenv('TAD_API_KEY',
                           'ffffffffffffffffffffffffffffffffffff'),
        url='https://pytenable.tenable.ad',
        ssl_verify=False,
        vendor='pytest',
        product='pytenable-automated-testing'
    )
