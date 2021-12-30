ETYPE = 'scan'
OBJECT_ID = '471430'
FILE_ID = '28223'

CONFIGURATION_ID = '04a0d852-0dc2-4e62-874d-a81e33b4a9f24e51e1f403febe40'
CONFIGURATION_DETAILS = {
    'is_was': None,
    'user_permissions': 128,
    'owner': 'user2@example.com',
    'title': 'Custom Scan',
    'is_agent': None,
    'id': CONFIGURATION_ID,
    'settings': {
        'basic': {
            'inputs': [
                {
                    'type': 'entry',
                    'name': 'Name',
                    'id': 'name',
                    'default': 'KitchenSinkScan',
                    'required': True
                }
            ],
            'title': 'Basic',
            'groups': [
                {
                    'title': 'Permissions',
                    'name': 'permissions',
                    'acls': [
                        {
                            'permissions': 0,
                            'owner': None,
                            'display_name': None,
                            'name': None,
                            'id': None,
                            'type': 'default'
                        }
                    ]
                }
            ],
            'sections': []
        }
    },
    'filter_attributes': [
        {
            'operators': [
                'eq',
                'neq',
                'match',
                'nmatch'
            ],
            'control': {
                'readable_regex': 'NUMBER',
                'type': 'entry',
                'regex': '^[0-9]+$',
                'maxlength': 18
            },
            'name': 'bid',
            'readable_name': 'Bugtraq ID'
        }
    ],
    'name': 'custom'
}

TEMPLATE_ID = 'd883b87b-a09d-4eea-89ae-317d2777ec4d08c3a05ec2812bcf'
TEMPLATE_DETAILS = {
    'is_was': None,
    'user_permissions': None,
    'owner': None,
    'title': 'Host Discovery',
    'is_agent': None,
    'id': TEMPLATE_ID,
    'settings': {
        'basic': {
            'inputs': [
                {
                    'type': 'select',
                    'id': 'include_aggregate',
                    'name': 'Scan results',
                    'default': True,
                    'options': [
                        {
                            'name': 'Keep private',
                            'value': 'false'
                        }
                    ]
                }
            ],
            'title': 'Basic',
            'groups': [
                {
                    'title': 'Schedule',
                    'name': 'schedule'
                },
                {
                    'inputs': [
                        {
                            'type': 'textarea',
                            'name': 'Email Recipient(s)',
                            'placeholder': 'Example: me@example.com, you@examp'
                        }
                    ],
                    'title': 'Notifications',
                    'name': 'email',
                    'filters': []
                }
            ],
            'sections': []
        },
        'discovery': {
            'inputs': None,
            'modes': {
                'id': 'discovery_mode',
                'name': 'mode',
                'type': 'ui_radio',
                'default': 'Host enumeration',
                'options': [
                    {
                        'desc': '<ul><li>General Settings:<ul><li>Always test',
                        'name': 'Host enumeration'
                    }
                ]
            },
            'title': 'Discovery',
            'groups': [
                {
                    'inputs': [
                        {
                            'type': 'ui_checkbox',
                            'name': 'Ping the remote host',
                            'id': 'ping_the_remote_host',
                            'default': 'yes',
                            'options': [
                                {
                                    'inputs': None,
                                    'name': 'no'
                                },
                                {
                                    'inputs': None,
                                    'name': 'yes',
                                    'sections': [
                                        {
                                            'inputs': [
                                                {
                                                    'type': 'checkbox',
                                                    'id': 'fast_network_disry',
                                                    'label': 'Use fastscovery',
                                                    'default': 'no',
                                                    'hint': 'If a host  tests.'
                                                }
                                            ],
                                            'title': 'General Settings',
                                            'name': 'general'
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    'title': 'Host Discovery',
                    'name': 'host_discovery',
                    'sections': [
                        {
                            'inputs': [
                                {
                                    'type': 'checkbox',
                                    'id': 'scan_network_printers',
                                    'label': 'Scan Network Printers',
                                    'default': 'no'
                                }
                            ],
                            'title': 'Fragile Devices',
                            'name': 'fragile_devices'
                        }
                    ]
                },
                {
                    'inputs': None,
                    'title': 'Port Scanning',
                    'name': 'network_discovery',
                    'sections': [
                        {
                            'inputs': [
                                {
                                    'type': 'checkbox',
                                    'id': 'unscanned_closed',
                                    'label': 'Consider unscanned ports as cl',
                                    'default': 'no'
                                },
                                {
                                    'type': 'medium-entry',
                                    'id': 'portscan_range',
                                    'label': 'Port scan range:',
                                    'default': 'default'
                                }
                            ],
                            'title': 'Ports',
                            'name': 'ports'
                        }
                    ]
                }
            ],
            'sections': []
        },
        'report': {
            'inputs': None,
            'modes': [
                {
                    'desc': '<ul><li>Report processing:<ul><li>Normal r</ul>',
                    'id': 'default',
                    'name': 'Default',
                    'default': True
                }
            ],
            'title': 'Report',
            'groups': [],
            'sections': [
                {
                    'inputs': [
                        {
                            'type': 'checkbox',
                            'id': 'reverse_lookup',
                            'label': 'Designate hosts by their DNS name',
                            'default': 'no'
                        }
                    ],
                    'title': 'Output',
                    'name': 'report_output'
                }
            ]
        }
    },
    'filter_attributes': [
        {
            'operators': [
                'eq',
                'neq',
                'match',
                'nmatch'
            ],
            'control': {
                'readable_regex': 'NUMBER',
                'type': 'entry',
                'regex': '^[0-9]+$',
                'maxlength': 18
            },
            'name': 'bid',
            'readable_name': 'Bugtraq ID'
        }
    ],
    'name': 'discovery'
}

PLUGIN_ID = '56777'
POLICY_ID = '3242'
FAMILY_ID = '32543'
PLUGIN_DETAILS = {
    'plugindescription': {
        'severity': None,
        'pluginname': 'Ubuntu 10.04 LTS / 10.10 / 11.04 / 11.10 : clamav',
        'pluginattributes': {
            'synopsis': 'The remote Ubuntu host is missing a security-related',
            'description': 'Stephane Chazelas discovered the bytecode engine',
            'risk_information': {
                'cvss_vector': 'CVSS2#AV:N/AC:M/Au:N/C:N/I:N/A:P',
                'risk_factor': 'Medium',
                'cvss_base_score': '4.3',
                'cvss_temporal_score': '3.2',
                'cvss_temporal_vector': 'CVSS2#E:U/RL:OF/RC:C'
            },
            'ref_information': {
                'ref': [
                    {
                        'name': 'bid',
                        'values': {
                            'value': [
                                '50183'
                            ]
                        },
                        'url': 'http://www.securityfocus.com/bid/'
                    },
                    {
                        'name': 'usn',
                        'values': {
                            'value': [
                                '1258-1'
                            ]
                        },
                        'ext': '/',
                        'url': 'http://www.ubuntu.com/usn/usn-'
                    },
                    {
                        'name': 'cve',
                        'values': {
                            'value': [
                                'CVE-2011-3627'
                            ]
                        },
                        'url': 'http://web.nvd.nist.gov/view/vuln/detail?vuln'
                    }
                ]
            },
            'plugin_name': 'Ubuntu 10.04 LTS / 10.10 / 11.04 / 11.10 : clamav',
            'see_also': [
                'https://usn.ubuntu.com/1258-1/'
            ],
            'fname': 'ubuntu_USN-1258-1.nasl',
            'usn': '1258-1',
            'plugin_information': {
                'plugin_version': '1.8',
                'plugin_id': 56777,
                'plugin_type': 'local',
                'plugin_publication_date': '2011/11/11',
                'plugin_family': 'Ubuntu Local Security Checks',
                'plugin_modification_date': '2018/12/01'
            },
            'solution': 'Update the affected libclamav6 package.',
            'vuln_information': {
                'cpe': 'cpe:/o:canonical:ubuntu_linux:10.04:-:lts\ncpe:/o:can',
                'exploitability_ease': 'No known exploits are available',
                'exploit_available': 'false',
                'patch_publication_date': '2011/11/10'
            }
        },
        'pluginfamily': 'Ubuntu Local Security Checks',
        'pluginid': PLUGIN_ID
    }
}
