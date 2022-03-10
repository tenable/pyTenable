'''
Testing the tio iterator
'''

import pytest
import responses

from tenable.io.v3.base.iterators.was_iterator import SearchIterator

BASE_URL = r'https://cloud.tenable.com/api/v3/assets/iterator'
ASSET_DATA = {
    'assets': [
        {
            'id': '116af8c3-969d-4621-9f9f-364eeb58e3a7',
            'has_agent': False,
            'last_seen': '2018-12-31T15:00:57.000Z',
            'last_scan_target': '192.0.2.57',
            'sources': [
                {
                    'name': 'NESSUS_SCAN',
                    'first_seen': '2018-12-31T15:00:57.000Z',
                    'last_seen': '2018-12-31T15:00:57.000Z'
                }
            ],
            'acr_score': 8,
            'acr_drivers': [
                {
                    'driver_name': 'device_type',
                    'driver_value': [
                        'general_purpose'
                    ]
                },
                {
                    'driver_name': 'device_capability',
                    'driver_value': [
                        'pci'
                    ]
                },
                {
                    'driver_name': 'internet_exposure',
                    'driver_value': [
                        'internal'
                    ]
                }
            ],
            'exposure_score': 753,
            'scan_frequency': [
                {
                    'interval': 90,
                    'frequency': 3,
                    'licensed': False
                },
                {
                    'interval': 30,
                    'frequency': 1,
                    'licensed': False
                },
                {
                    'interval': 60,
                    'frequency': 1,
                    'licensed': False
                }
            ],
            'ipv4': [
                '192.0.2.57'
            ],
            'ipv6': [],
            'fqdn': [
                'example.com'
            ],
            'netbios_name': [
                'example.com'
            ],
            'operating_system': [
                'Linux Kernel 3.10.0-862.14.4.el7.x86_64  7.5.1804 (Core)'
            ],
            'agent_name': [],
            'aws_ec2_name': [],
            'mac_address': []
        },
        {
            'id': '700a652e-9922-45cd-a6b7-3611c0e1601c',
            'has_agent': False,
            'last_seen': '2018-12-31T15:00:57.000Z',
            'last_scan_target': '192.0.2.58',
            'sources': [
                {
                    'name': 'NESSUS_SCAN',
                    'first_seen': '2018-12-31T14:59:23.000Z',
                    'last_seen': '2018-12-31T15:00:57.000Z'
                }
            ],
            'ipv4': [
                '192.0.2.58'
            ],
            'ipv6': [],
            'fqdn': [
                'example.com'
            ],
            'netbios_name': [
                'scanner'
            ],
            'operating_system': [
                'Linux Kernel 4.4.0-104-generic on Ubuntu 16.04'
            ],
            'agent_name': [],
            'aws_ec2_name': [],
            'mac_address': []
        },
        {
            'id': 'dc3fdd75-3a01-4277-9ecd-903a80e08332',
            'has_agent': False,
            'last_seen': '2018-12-31T15:00:57.000Z',
            'last_scan_target': '192.0.2.59',
            'sources': [
                {
                    'name': 'NESSUS_SCAN',
                    'first_seen': '2018-12-31T14:59:23.000Z',
                    'last_seen': '2018-12-31T15:00:57.000Z'
                }
            ],
            'ipv4': [
                '192.0.2.59'
            ],
            'ipv6': [],
            'fqdn': [
                'example.com'
            ],
            'netbios_name': [
                'SHANE'
            ],
            'operating_system': [
                'Microsoft Windows 10 Pro'
            ],
            'agent_name': [],
            'aws_ec2_name': [],
            'mac_address': []
        },
        {
            'id': '47351ecd-cbae-4576-9740-ff1b4eb88177',
            'has_agent': False,
            'last_seen': '2018-12-31T15:00:57.000Z',
            'last_scan_target': '192.0.2.60',
            'sources': [
                {
                    'name': 'NESSUS_SCAN',
                    'first_seen': '2018-12-31T14:59:23.000Z',
                    'last_seen': '2018-12-31T15:00:57.000Z'
                }
            ],
            'ipv4': [
                '192.0.2.60'
            ],
            'ipv6': [],
            'fqdn': [
                'example.com'
            ],
            'netbios_name': [
                'ARCHIE'
            ],
            'operating_system': [
                'Microsoft Windows 10 Pro'
            ],
            'agent_name': [],
            'aws_ec2_name': [],
            'mac_address': []
        }
    ],
    'pagination': {
        'total': 4
    }
}


@responses.activate
def test_was_iterator(api):
    '''
    Test for was search iterator
    '''

    limit = 5
    offset = 0
    query = {
        'limit': limit,
        'offset': offset
    }
    payload = dict(
        fields=['id']
    )
    pages_total = 2

    responses.add(
        method=responses.POST,
        url=BASE_URL,
        json=ASSET_DATA,
    )

    tio_iterator = SearchIterator(api,
                                  _payload=payload,
                                  _pages_total=pages_total,
                                  _query=query,
                                  _path='api/v3/assets/iterator',
                                  _resource='assets'
                                  )
    assert ASSET_DATA['assets'].__contains__(next(tio_iterator))
    assert ASSET_DATA['assets'].__contains__(next(tio_iterator))
    assert ASSET_DATA['assets'].__contains__(next(tio_iterator))
    assert ASSET_DATA['assets'].__contains__(next(tio_iterator))

    with pytest.raises(StopIteration):
        next(tio_iterator)
