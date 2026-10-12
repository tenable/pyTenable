"""
configuration which would be used for testing sc.
"""

import pytest
import responses

from tenable.sc import TenableSC


@pytest.fixture
def group():
    """
    test fixture for group
    """
    return {
        'id': '2',
        'name': 'groupname',
        'description': '',
        'createdTime': '1554499673',
        'modifiedTime': '1554499673',
        'lces': [],
        'repositories': [],
        'definingAssets': [],
        'userCount': 0,
        'users': [],
        'assets': [],
        'policies': [],
        'queries': [],
        'credentials': [],
        'dashboardTabs': [],
        'auditFiles': [],
        'arcs': [],
    }


@pytest.fixture
def tsc():
    with responses.RequestsMock() as rsps:
        rsps.get(
            'https://nourl/rest/system',
            json={'error_code': None, 'response': {'version': '6.4.0'}},
        )
        return TenableSC(
            url='https://nourl', access_key='SOMETHING', secret_key='SECRET'
        )
