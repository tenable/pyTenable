'''
This contains the objects for negative tests for assets
'''

NEGATIVE_ASSIGN_TAGS_SCHEMA = [
    {'invalid': 'key'},
    {
        'assets': [True, 'test_invalid', 1233],
        'tags': ['00000000-0000-0000-0000-000000000000'],
        'action': 'add'
    },
    {
        'assets': ['b9584671-68e6-426b-a67c-6373778b8a0a'],
        'tags': ['test_invalid', True, 1234],
        'action': 'add'
    },
    {
        'assets': ['b9584671-68e6-426b-a67c-6373778b8a0a'],
        'tags': ['00000000-0000-0000-0000-000000000000'],
        'action': 'invalid'
    },
    {
        'assets': ['b9584671-68e6-426b-a67c-6373778b8a0a'],
        'tags': ['00000000-0000-0000-0000-000000000000'],
        'action': 1234
    },
    {
        'assets': ['b9584671-68e6-426b-a67c-6373778b8a0a'],
        'tags': ['00000000-0000-0000-0000-000000000000'],
        'action': True
    }
]

NEGATIVE_IMPORT_ASSET_SCHEMA = [
    {'invalid': 'key'},
    {'source': True,
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 'example',
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'source': 2344,
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 'example',
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'source': 'example_source',
     'assets': [{
         'fqdn': [True, 1234],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 'example',
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'source': 'example_source',
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': [True, 1234],
         'netbios_name': 'example',
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'source': 'example_source',
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 'example',
         'mac_address': [True, 1234]
     }]},
    {'source': 'example_source',
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': True,
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'source': 'example_source',
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 1234,
         'mac_address': ['00:00:00:00:00:00']
     }]}
]

NEGATIVE_MOVE_ASSET_SCHEMA = [
    {'invalid': 'test'},
    {'source': 'invalid_test',
     'destination': '00000000-0000-0000-0000-000000000000',
     'targets': ['127.0.0.1']
     },
    {'source': 234,
     'destination': '00000000-0000-0000-0000-000000000000',
     'targets': ['127.0.0.1']
     },
    {'source': True,
     'destination': '00000000-0000-0000-0000-000000000000',
     'targets': ['127.0.0.1']
     },
    {'source': '00000000-0000-0000-0000-000000000000',
     'destination': 'invalid_test',
     'targets': ['127.0.0.1']
     },
    {'source': '00000000-0000-0000-0000-000000000000',
     'destination': 1234,
     'targets': ['127.0.0.1']
     },
    {'source': '00000000-0000-0000-0000-000000000000',
     'destination': False,
     'targets': ['127.0.0.1']
     },
    {'source': '00000000-0000-0000-0000-000000000000',
     'destination': '00000000-0000-0000-0000-000000000000',
     'targets': ['invalid_ip', True, 1234]
     }
]

NEGATIVE_UPDATE_ACR_SCHEMA = [
    {'invalid': 'test'},
    {'reason': [True, 123, 'invalid_test'],
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 'example',
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'reason': ['Business Critical'],
     'assets': [{
         'fqdn': [True, 1234],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 'example',
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'reason': ['Business Critical'],
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': [True, 1234],
         'netbios_name': 'example',
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'reason': ['Business Critical'],
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 'example',
         'mac_address': [True, 1234]
     }]},
    {'reason': ['Business Critical'],
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': True,
         'mac_address': ['00:00:00:00:00:00']
     }]},
    {'reason': ['Business Critical'],
     'assets': [{
         'fqdn': ['example.py.test'],
         'ipv4': ['192.168.254.1'],
         'netbios_name': 1234,
         'mac_address': ['00:00:00:00:00:00']
     }]}
]
