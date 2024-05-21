"""
conftest
"""
import pytest
import responses

from tenable.ot import TenableOT
from tenable.version import version


@pytest.fixture
@responses.activate
def fixture_ot():
    """fixture ot"""
    return TenableOT(
        url="https://localhost",
        api_key="some_random_key",
        vendor="pytest",
        product="pytenable-automated-testing",
        build=version,
    )


@pytest.fixture(scope='module')
def vcr_config():
    """vcr config fixture"""
    return {
        'filter_headers': [
            ('X-APIKeys', 'TOT_X_API_KEYS')
        ],
    }


@pytest.fixture
def api():
    """xapi key fixture"""
    return TenableOT(
        url="https://172.26.68.231",
        api_key="TOT_X_API_KEYS",
        vendor="pytest",
        product="pytenable-automated-testing",
        build=version
    )
