import pytest, responses
from tenable.version import version
from tenable.ot import TenableOT


@pytest.fixture
@responses.activate
def ot():
    responses.add(
        method='GET',
        url='https://localhost:443/v1/version',
        json={
            'Module': 'Cobex',
            'Version': '3.7.0',
            'NvdVersion': '1.12.0'
        }
    )
    return TenableOT(
        address='localhost',
        vendor='pytest',
        product='pytenable-automated-testing',
        build=version
    )