'''
conftest
'''
import pytest
import responses

from tenable.ot import TenableOT
from tenable.version import version


@pytest.fixture
@responses.activate
def fixture_ot():
    '''fixture ot'''
    return TenableOT(
        url='https://localhost',
        api_key='some_random_key',
        vendor='pytest',
        product='pytenable-automated-testing',
        build=version
    )
