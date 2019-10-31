import pytest, os, uuid
from tenable.downloads import Downloads
from tenable.errors import *

@pytest.fixture(scope='module')
def vcr_config():
    return {
        'filter_headers': [
            ('Authorization', 'Bearer 000'),
        ],
    }


@pytest.fixture(autouse=True, scope='module')
def dl(request, vcr):
    return Downloads(os.getenv('DL_TOKEN'),
        vendor='pytest',
        product='pytenable-automated-testing')