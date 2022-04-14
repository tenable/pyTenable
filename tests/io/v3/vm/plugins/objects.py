PLUGIN_ID = 22372
PLUGIN = {
    'attributes': [
        {
            'attribute_value': 'aix_IY19744.nasl',
            'attribute_name': 'fname'
        },
        {
            'attribute_value': 'AIX 5.1 : IY19744',
            'attribute_name': 'plugin_name'
        },
        {
            'attribute_value': '$Revision: 1.5 $',
            'attribute_name': 'script_version'
        },
        {
            'attribute_value': 'http://www-912.ibm.com/eserver/support/fixes/',
            'attribute_name': 'solution'
        },
        {
            'attribute_value': 'High',
            'attribute_name': 'risk_factor'
        },
        {
            'attribute_value': 'The remote host is missing AIX Critical '
                               'Security Patch number IY19744 (SECURITY: '
                               'BufferOverflow in ...',
            'attribute_name': 'description'
        },
        {
            'attribute_value': '2006/09/16',
            'attribute_name': 'plugin_publication_date'
        }, {
            'attribute_value': 'The remote host is missing a vendor-supplied '
                               'security patch',
            'attribute_name': 'synopsis'
        }
    ],
    'family_name': 'AIX Local Security Checks',
    'name': 'AIX 5.1 : IY19744',
    'id': PLUGIN_ID
}
PLUGINS_IN_FAMILY_ID = 1
PLUGINS_IN_FAMILY = {
    'plugins': [
        {
            'id': 22372,
            'name': 'AIX 5.1 : IY19744'
        },
        {
            'id': 22373,
            'name': 'AIX 5.1 : IY20486'
        },
        {
            'id': 22374,
            'name': 'AIX 5.1 : IY21309'
        }
    ],
    'name': 'AIX Local Security Checks',
    'id': PLUGINS_IN_FAMILY_ID
}
FAMILIES = [
    {
        'count': 11342,
        'name': 'AIX Local Security Checks',
        'id': 1
    },
    {
        'count': 1164,
        'name': 'Amazon Linux Local Security Checks',
        'id': 35
    },
    {
        'count': 114,
        'name': 'Backdoors',
        'id': 17
    }
]
PLUGINS_LIST = {
    'plugins': [
        {
            'id': 13670,
            'name': 'Fedora Core 1 : kernel-2.4.22-1.2140.nptl (2003-047)',
            'modification_date': '2018-07-19T00:00:00Z',
            'version': '1.17',
            'exploited_by_malware': False,
            'description': 'Various RTC drivers had the potential to leak '
                           'small amounts of kernel memory to userspace '
                           'through IO ...',
            'unsupported_by_vendor': False,
            'cvss_temporal_score': 0,
            'patch_publication_date': '2004-01-07T00:00:00Z',
            'see_also': [
                'http://www.nessus.org/u?07bc9e7f'
            ],
            'default_account': False,
            'exploit_available': False,
            'cve': [
                'CVE-2003-0984'
            ],
            'exploit_framework_canvas': False,
            'cvss_base_score': 4.6,
            'solution': 'Update the affected packages.',
            'cvss_vector': {
                'raw': 'AV:L/AC:L/Au:N/C:P/I:P/A:P',
                'AccessVector': 'Local-access',
                'Availability-Impact': 'Partial',
                'Authentication': 'None required',
                'Integrity-Impact': 'Partial',
                'AccessComplexity': 'Low',
                'Confidentiality-Impact': 'Partial'
            },
            'exploit_framework_exploithub': False,
            'cpe': [
                'p-cpe:/a:fedoraproject:fedora:kernel-source',
                'cpe:/o:fedoraproject:fedora_core:1',
                'p-cpe:/a:fedoraproject:fedora:kernel-BOOT',
                'p-cpe:/a:fedoraproject:fedora:kernel-debuginfo',
                'p-cpe:/a:fedoraproject:fedora:kernel',
                'p-cpe:/a:fedoraproject:fedora:kernel-doc',
                'p-cpe:/a:fedoraproject:fedora:kernel-smp'
            ],
            'publication_date': '2004-07-23T00:00:00Z',
            'exploit_framework_core': False,
            'in_the_news': False,
            'has_patch': True,
            'xref': [
                'FEDORA:2003-047'
            ],
            'malware': False,
            'exploit_framework_d2_elliot': False,
            'xrefs': [
                {
                    'type': 'FEDORA',
                    'id': '2003-047'
                }
            ],
            'risk_factor': 'Medium',
            'synopsis': 'The remote Fedora Core host is missing a security '
                        'update.',
            'cvss3_temporal_score': 0,
            'exploited_by_nessus': False,
            'cvss3_base_score': 0,
            'exploit_framework_metasploit': False,
            'type': 'local'
        },
        {
            'id': 13671,
            'name': 'Fedora Core 1 : mc-4.6.0-8.4 (2004-058)',
            'modification_date': '2018-07-19T00:00:00Z',
            'version': '1.14',
            'exploited_by_malware': False,
            'description': '- Sat Jan 31 2004 Jakub Jelinek <jakub at '
                           'redhat.com>4.6.0-8.4, - fix previous patch - '
                           'Fri...',
            'unsupported_by_vendor': False,
            'cvss_temporal_score': 0,
            'patch_publication_date': '2004-02-09T00:00:00Z',
            'see_also': [
                'http://www.nessus.org/u?ea1a95cb'
            ],
            'default_account': False,
            'exploit_available': False,
            'cve': [
                'CVE-2003-1023'
            ],
            'exploit_framework_canvas': False,
            'cvss_base_score': 7.5,
            'solution': 'Update the affected mc and / or mc-debuginfo '
                        'packages.',
            'cvss_vector': {
                'raw': 'AV:N/AC:L/Au:N/C:P/I:P/A:P',
                'AccessVector': 'Network',
                'Availability-Impact': 'Partial',
                'Authentication': 'None required',
                'Integrity-Impact': 'Partial',
                'AccessComplexity': 'Low',
                'Confidentiality-Impact': 'Partial'
            },
            'exploit_framework_exploithub': False,
            'cpe': [
                'cpe:/o:fedoraproject:fedora_core:1',
                'p-cpe:/a:fedoraproject:fedora:mc-debuginfo',
                'p-cpe:/a:fedoraproject:fedora:mc'
            ],
            'publication_date': '2004-07-23T00:00:00Z',
            'exploit_framework_core': False,
            'in_the_news': False,
            'has_patch': True,
            'xref': [
                'FEDORA:2004-058'
            ],
            'malware': False,
            'exploit_framework_d2_elliot': False,
            'xrefs': [
                {
                    'type': 'FEDORA',
                    'id': '2004-058'
                }
            ],
            'risk_factor': 'High',
            'synopsis': 'The remote Fedora Core host is missing a security '
                        'update.',
            'cvss3_temporal_score': 0,
            'exploited_by_nessus': False,
            'cvss3_base_score': 0,
            'exploit_framework_metasploit': False,
            'type': 'local'
        }
    ],
    'size': 1000,
    'params': {
        'page': 3,
        'size': 1000,
        'last_updated': '2018-01-01'
    },
    'total_count': 75621
}
PLUGIN_FILTER = {
    'and': [
        {
            'property': 'exploited_by_malware',
            'operator': 'eq',
            'value': False
        }
    ]
}
PLUGIN_FIELDS = ['id', 'name', 'modification_date', 'version',
                 'exploited_by_malware', 'description',
                 'unsupported_by_vendor', 'cvss_temporal_score',
                 'patch_publication_date', 'see_also', 'default_account',
                 'exploit_available', 'cve', 'exploit_framework_canvas',
                 'cvss_base_score', 'solution', 'cvss_vector',
                 'exploit_framework_exploithub', 'cpe' 'publication_date',
                 'exploit_framework_core', 'in_the_news', 'has_patch', 'xref',
                 'malware', 'exploit_framework_d2_elliot', 'xrefs',
                 'risk_factor', 'synopsis', 'cvss3_temporal_score',
                 'exploited_by_nessus', 'cvss3_base_score',
                 'exploit_framework_metasploit', 'type']
FAMILY_FILTER = {
    'and': [
        {
            'property': 'id',
            'operator': 'eq',
            'value': '1'
        }
    ]
}
FAMILY_FIELDS = ['count', 'name', 'id']
