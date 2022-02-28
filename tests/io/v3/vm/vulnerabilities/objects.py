NEGATIVE_VULNERABILITY_OBJECT_SCHEMA = [
    {'invalid': 'str'},
    {'tenable_plugin_id': 123},
    {'cve': 123, 'tenable_plugin_id': 'test'},
    {'cve': 'test'},
    {'port': False, 'tenable_plugin_id': 'test'},
    {'protocol': 123, 'tenable_plugin_id': 'test'},
    {'authenticated': 'test', 'tenable_plugin_id': 'test'},
    {'last_found': False, 'tenable_plugin_id': 'test'},
    {'output': 123, 'tenable_plugin_id': 'test'},
]

NEGATIVE_NETWORK_INTERFACE_OBJECT_SCHEMA = [
    {'invalid': 'key'},
    {'ipv4': 'invalid'},
    {'ipv4': [123]},
    {'ipv6': 'invalid'},
    {'ipv6': [False]},
    {'mac_address': []},
    {'netbios_name': False},
    {'fqdn': 123},
]

NEGATIVE_ASSET_OBJECT_SCHEMA = [
    {'invalid': 'key'},
    {'hostname': 123, 'netbios_name': 'test'},
    {'hostname': 'test', 'netbios_name': 123},
    {'hostname': 'test'},
    {'netbios_name': 'test'},
    {'servicenow_sysid': False, 'hostname': 'test', 'netbios_name': 'test'},
    {'ssh_fingerprint': 123, 'hostname': 'test', 'netbios_name': 'test'},
    {'bios_uuid': 123, 'hostname': 'test', 'netbios_name': 'test'},
    {'operating_systems': False, 'hostname': 'test', 'netbios_name': 'test'},
    {'tenable_agent_id': 1234, 'hostname': 'test', 'netbios_name': 'test'},
    {'tenable_network_id': [], 'hostname': 'test', 'netbios_name': 'test'},
    {'authenticated': 'invalid', 'hostname': 'test', 'netbios_name': 'test'},
    {'vulnerabilities': 'invalid', 'hostname': 'test', 'netbios_name': 'test'},
    {
        'vulnerabilities': ['invalid'],
        'hostname': 'test',
        'netbios_name': 'test'
    },
    {
        'network_interfaces': ['invalid'],
        'hostname': 'test',
        'netbios_name': 'test'
    },
    {
        'network_interfaces': 'invalid',
        'hostname': 'test',
        'netbios_name': 'test'
    },
    {
        'network_interfaces': [{'invalid': 'test'}],
        'hostname': 'test',
        'netbios_name': 'test'
    },
    {
        'vulnerabilities': [{'invalid': 'test'}],
        'hostname': 'test',
        'netbios_name': 'test'
    }
]

NEGATIVE_VULNERABILITY_SCHEMA = [
    {'invalid': 'key'},
    {
        'vendor': 123,
        'date_type': 'vm',
        'source': 'test',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}]
    },
    {
        'vendor': 'test',
        'date_type': 123,
        'source': 'test',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}]
    },
    {
        'vendor': 'test',
        'date_type': 'invalid',
        'source': 'test',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}]
    },
    {
        'vendor': 'test',
        'date_type': 'vm',
        'source': 123,
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}]
    },
    {
        'vendor': 'test',
        'date_type': 'vm',
        'source': 'test',
        'assets': 'invalid'
    },
    {
        'date_type': 'vm',
        'source': 'test',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}]
    },
    {
        'vendor': 'test',
        'source': 'test',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}]
    },
    {
        'vendor': 'test',
        'date_type': 'vm',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}]
    },
    {
        'vendor': 'test',
        'date_type': 'vm',
        'source': 'test',
    },
    {
        'vendor': 'test',
        'date_type': 'vm',
        'source': 'test',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}],
        'product': 1234
    },
    {
        'vendor': 'test',
        'date_type': 'vm',
        'source': 'test',
        'assets': [{'hostname': 'test', 'netbios_name': 'test'}],
        'coverage': False
    }
]
