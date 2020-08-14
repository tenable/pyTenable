import pytest, os, uuid, warnings
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
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    return Downloads(os.getenv('DL_TOKEN'),
        vendor='pytest',
        product='pytenable-automated-testing')