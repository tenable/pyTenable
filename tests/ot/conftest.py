import pytest, os, uuid
from tenable.version import version
from tenable.ot import TenableOT

@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_headers': [
            ('Authorization', 'Key 1234567890abcdef')
        ]
    }

@pytest.fixture(autouse=True)
def ot():
    return TenableOT(
        vendor='pytest',
        product='pytenable-automated-testing',
        build=version
    )