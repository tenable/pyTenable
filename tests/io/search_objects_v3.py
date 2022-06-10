'''
This file contains the negative objects for search schema
'''

NEGATIVE_SEARCH_SCHEMA = [
    {'invalid': 'key'},
    {
        'limit': '10er',
        'fields': ['bios_name', 'name'],
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': 'bios_name',
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': ['bios_name', 12],
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': True,
        'fields': ['bios_name', '12'],
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': {},
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': True,
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': [True, 13],
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': ['test', '13'],
        'next': True,
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': ['test', '13'],
        'next': 123,
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    },
    {
        'limit': 10,
        'fields': ['test', '13'],
        'next': 'sdf7a9s8df79afsd',
        'filter': {'value': 'SCCM', 'property': 'bios_name', 'operator': 'eq'},
        'sort': [
            {'or': 'asc', 'pr': 'name'}
        ]
    },
    {
        'limit': 10,
        'fields': ['test', '13'],
        'next': 'sdf000dfssdSDFSDFSFE00dfsdffaf',
        'filter': {'vv': 'SCCM', 'pr': 'bios_name', 'op': 'eq'},
        'sort': [
            {'order': 'asc', 'property': 'name'},
            {'order': 'desc', 'property': 'bios_name'},
        ]
    }
]

NEGATIVE_SORT_SCHEMA = [
    {'invalid': 'key'},
    ('bios_name', True),
    ('bios_name', 2342),
    {'bios_name': 'random'},
    {'bios_name': 123},
    {'bios_name': True},
    {234: 'asc'},
    {False: 'asc'},
    {'pro': 'bios_name', 'order': 'asc'},
    {'property': 'bios_name', 'or': 'asc'},
    {'property': 'bios_name', 'order': 'random'},
    {'property': True, 'order': 'asc'},
    {'property': 3455, 'order': 'asc'},
    {'property': 'bios_name', 'order': True},
    {'property': 'bios_name', 'order': 4353},
    {'na': 'bios_name', 'order': 'asc'},
    {'name': 'bios_name', 'or': 'asc'},
    {'name': 'bios_name', 'order': 'random'},
    {'name': True, 'order': 'asc'},
    {'name': 3455, 'order': 'asc'},
    {'name': 'bios_name', 'order': True},
    {'name': 'bios_name', 'order': 4353}
]

NEGATIVE_FILTER_SCHEMA = [
    {'invalid': 'key'},
    (23423, 'eq', 'SCCM'),
    (True, 'eq', 'SCCM'),
    {'pro': 'filter', 'operator': 'oper', 'value': 'test'},
    {123: 'filter', 'operator': 'oper', 'value': 'test'},
    {False: 'filter', 'operator': 'oper', 'value': 'test'},
    {'property': 123, 'operator': 'oper', 'value': 'test'},
    {'property': True, 'operator': 'oper', 'value': 'test'},
    {'property': 'filter', 'ope': 'oper', 'value': 'test'},
    {'property': 'filter', 1234: 'oper', 'value': 'test'},
    {'property': 'filter', True: 'oper', 'value': 'test'},
    {'property': 'filter', 'operator': 1234, 'value': 'test'},
    {'property': 'filter', 'operator': True, 'value': 'test'},
    {'property': 'filter', 'operator': 'oper', 'va': 'test'},
    {'property': 'filter', 'operator': 'oper', 2134: 'test'},
    {'property': 'filter', 'operator': 'oper', True: 'test'},
    (
        'invalid',
        ('and', ('test', 'eq', '1'), ('test', 'eq', '2')),
        'and',
        ('test', 'eq', 3),
    ),
    (
        True,
        ('and', ('test', 'eq', '1'), ('test', 'eq', '2')),
        'and',
        ('test', 'eq', 3),
    ),
    (
        234,
        ('and', ('test', 'eq', '1'), ('test', 'eq', '2')),
        'and',
        ('test', 'eq', 3),
    ),
    (
        'and',
        ('and', ('test', 'eq', '1'), ('test', 'eq', '1')),
        'and',
        ('test', 'eq', '1'),
    ),
    (
        'and',
        ('and', ('test', 'eq', None), ('test', 'eq', '1')),
        'or',
        ('test', 'eq', '1'),
    ),
    {
        'invalid': [
            {
                'and': [
                    {'value': '1', 'operator': 'oper', 'property': '1'},
                    {'value': '2', 'operator': 'oper', 'property': '2'},
                ]
            }
        ],
        'and': [{'value': '3', 'operator': 'oper', 'property': '3'}],
    },
    {
        True: [
            {
                'and': [
                    {'value': '1', 'operator': 'oper', 'property': '1'},
                    {'value': '2', 'operator': 'oper', 'property': '2'},
                ]
            }
        ],
        'and': [{'value': '3', 'operator': 'oper', 'property': '3'}],
    },

]
