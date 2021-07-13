'''
conftest
'''
import os
import warnings
import pytest
from tenable.downloads import Downloads


@pytest.fixture(scope='module')
def vcr_config():
    '''
    vcr_config fixture
    '''
    return {
        'filter_headers': [
            ('Authorization', 'Bearer 000'),
        ],
    }


@pytest.fixture(autouse=True, scope='module')
def dl():
    '''dl fixture'''
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    return Downloads(os.getenv('DL_TOKEN'),
                     vendor='pytest',
                     product='pytenable-automated-testing')
