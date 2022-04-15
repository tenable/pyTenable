VM_DEFINITIONS = {
    'AGENT_EXCLUSIONS': {
        "fields": [
            "id",
            "name",
            "core_updates_blocked",
            "schedule.enabled",
            "schedule.starttime",
            "schedule.endtime",
            "schedule.rrules",
            "schedule.timezone",
            "creation_date",
            "last_modification_date",
            "description"
        ],
        "filters": [
            {
                "name": "id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists",
                    "contains"
                ]
            },
            {
                "name": "core_updates_blocked",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "schedule.enabled",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "schedule.starttime",
                "logical_type": "DateTime",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "schedule.endtime",
                "logical_type": "DateTime",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "schedule.rrules.freq",
                "logical_type": "String",
                "types": [
                    "error",
                    "ps"
                ],
                "operators": [
                    "eq"
                ]
            },
            {
                "name": "schedule.rrules.interval",
                "logical_type": "String",
                "types": [
                    "error",
                    "ps"
                ],
                "operators": [
                    "eq"
                ]
            },
            {
                "name": "schedule.rrules.byweekday",
                "logical_type": "String",
                "types": [
                    "error",
                    "ps"
                ],
                "operators": [
                    "eq"
                ]
            },
            {
                "name": "schedule.rrules.bymonthday",
                "logical_type": "String",
                "types": [
                    "error",
                    "ps"
                ],
                "operators": [
                    "eq"
                ]
            },
            {
                "name": "schedule.timezone",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists",
                    "contains"
                ]
            },
            {
                "name": "creation_date",
                "logical_type": "DateTime",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_modification_date",
                "logical_type": "DateTime",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "description",
                "logical_type": "String",
                "operators": [
                    "contains",
                    "exists",
                    "nexists"
                ]
            }
        ],
        "sortable_fields": [
            "id",
            "name",
            "schedule.starttime",
            "schedule.endtime",
            "schedule.timezone",
            "creation_date",
            "last_modification_date"
        ]
    },
    'AGENT_GROUPS': {
        "fields": [
            "agents_count",
            "created",
            "id",
            "modified",
            "name",
            "owner_id",
            "shared",
            "user_permissions"
        ],
        "wildcard_fields": [
            "name"
        ],
        "filters": [
            {
                "name": "id",
                "readable_name": "Id",
                "operators": [
                    "eq",
                    "neq"
                ],
                "control": {
                    "readable_regex": "textfield"
                }
            },
            {
                "name": "name",
                "readable_name": "Name",
                "operators": [
                    "eq",
                    "neq",
                    "match",
                    "nmatch"
                ],
                "control": {
                    "type": "textfield"
                }
            },
            {
                "name": "created",
                "readable_name": "Creation Date",
                "operators": [
                    "date-lt",
                    "date-gt",
                    "date-eq",
                    "date-neq"
                ],
                "control": {
                    "type": "datefield"
                }
            },
            {
                "name": "modified",
                "readable_name": "Last Modified",
                "operators": [
                    "date-lt",
                    "date-gt",
                    "date-eq",
                    "date-neq"
                ],
                "control": {
                    "type": "datefield"
                }
            }
        ],
        "sort": {
            "sortable_fields": [
                "name",
                "created",
                "modified",
                "agents_count"
            ]
        }
    },
    'AGENTS': {
        "wildcard_fields": [
            "core_version",
            "distro",
            "groups",
            "ip",
            "name",
            "platform",
            "status"
        ],
        "filters": [
            {
                "name": "core_version",
                "readable_name": "Version",
                "operators": [
                    "match",
                    "lt",
                    "neq",
                    "eq",
                    "nmatch",
                    "gt"
                ],
                "control": {
                    "readable_regex": "X.Y.Z",
                    "type": "entry",
                    "regex": ".*"
                }
            },
            {
                "name": "distro",
                "readable_name": "Distro",
                "operators": [
                    "match",
                    "nmatch"
                ],
                "control": {
                    "readable_regex": "Distro Name (e.g. es7-x86-64)",
                    "type": "entry",
                    "regex": ".*"
                }
            },
            {
                "name": "groups",
                "readable_name": "Member of Group",
                "operators": [
                    "eq",
                    "neq"
                ],
                "control": {
                    "type": "dropdown",
                    "list": [
                        {
                            "name": "None",
                            "id": -1
                        },
                        {
                            "name": "samgroup3",
                            "id": 428285
                        },
                        {
                            "name": "samgroup2",
                            "id": 428284
                        },
                        {
                            "name": "samgroup",
                            "id": 428283
                        }
                    ]
                }
            },
            {
                "name": "ip",
                "readable_name": "IP Address",
                "operators": [
                    "eq",
                    "neq",
                    "match",
                    "nmatch"
                ],
                "control": {
                    "readable_regex": "192.168.1.1",
                    "type": "entry",
                    "regex": ".*"
                }
            },
            {
                "name": "last_connect",
                "readable_name": "Last Connection",
                "operators": [
                    "date-lt",
                    "date-gt",
                    "date-eq",
                    "date-neq"
                ],
                "control": {
                    "readable_regex": "YYYY/MM/DD",
                    "type": "datefield",
                    "regex": "^[0-9]+$"
                }
            },
            {
                "name": "last_scanned",
                "readable_name": "Last Scanned",
                "operators": [
                    "date-lt",
                    "date-gt",
                    "date-eq",
                    "date-neq"
                ],
                "control": {
                    "readable_regex": "YYYY/MM/DD",
                    "type": "datefield",
                    "regex": "^[0-9]+$"
                }
            },
            {
                "name": "name",
                "readable_name": "Name",
                "operators": [
                    "eq",
                    "neq",
                    "match",
                    "nmatch"
                ],
                "control": {
                    "readable_regex": "TEXT",
                    "type": "entry",
                    "regex": ".*"
                }
            },
            {
                "name": "platform",
                "readable_name": "Platform",
                "operators": [
                    "eq",
                    "neq",
                    "match",
                    "nmatch"
                ],
                "control": {
                    "readable_regex": "Platform Name (e.g. Linux)",
                    "type": "entry",
                    "regex": ".*"
                }
            },
            {
                "name": "plugin_feed_id",
                "readable_name": "Last Plugin Update",
                "operators": [
                    "date-lt",
                    "date-gt",
                    "date-eq",
                    "date-neq"
                ],
                "control": {
                    "readable_regex": "YYYY/MM/DD",
                    "type": "datefield",
                    "regex": "^[0-9]{4}/[0-9]{2}/[0-9]{2}$"
                }
            },
            {
                "name": "status",
                "readable_name": "Status",
                "operators": [
                    "eq",
                    "neq"
                ],
                "control": {
                    "type": "dropdown",
                    "list": [
                        "Online",
                        "Offline",
                        "Initializing"
                    ]
                }
            },
            {
                "name": "uuid",
                "readable_name": "UUID",
                "operators": [
                    "eq",
                    "neq"
                ],
                "control": {
                    "readable_regex": "agent uuid",
                    "type": "entry",
                    "regex": ".*"
                }
            }
        ],
        "sort": {
            "sortable_fields": [
                "core_version",
                "distro",
                "ip",
                "last_connect",
                "last_scanned",
                "name",
                "platform",
                "plugin_feed_id"
            ]
        }
    },
    'ASSETS': {},
    'AUDIT_LOGS': {},
    'CREDENTIALS': {
        "wildcard_fields": [
            "name",
            "description",
            "type"
        ],
        "filters": [
            {
                "name": "name",
                "readable_name": "Credential Name",
                "control": {
                    "readable_regex": "TEXT",
                    "type": "entry",
                    "regex": ".*"
                },
                "operators": [
                    "eq",
                    "neq",
                    "match",
                    "nmatch"
                ]
            },
            {
                "name": "type",
                "readable_name": "Credential Type",
                "control": {
                    "type": "dropdown_multi",
                    "list": [
                        {
                            "id": "Windows",
                            "name": "Windows"
                        }
                    ]
                },
                "operators": [
                    "eq",
                    "neq"
                ]
            },
            {
                "name": "created_date",
                "readable_name": "Created Date",
                "control": {
                    "type": "datefield",
                    "regex": "^[0-9]{4}/[0-9]{2}/[0-9]{2}$",
                    "readable_regex": "YYYY/MM/DD"
                },
                "operators": [
                    "date-lt",
                    "date-gt",
                    "date-eq",
                    "date-neq"
                ]
            }
        ],
        "sort": {
            "sortable_fields": [
                "name",
                "type",
                "created_date"
            ]
        }
    },
    'EDITORS': {},
    'EXCLUSIONS': {},
    'FOLDERS': {},
    'NETWORKS': {},
    'PLUGIN_FAMILIES': {},
    'PLUGINS': {
        "fields": [
            "id",
            "name",
            "last_updated"
        ],
        "filters": [
            {
                "name": "id",
                "logical_type": "Integer",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists",
                    "between"
                ]
            },
            {
                "name": "name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_updated",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            }
        ],
        "sortable_fields": [
            "id",
            "name",
            "last_updated"
        ]
    },
    'POLICIES': {},
    'REMEDIATION_SCANS': {},
    'SCANNER_GROUPS': {
        "fields": [
            "id",
            "name",
            "type",
            "scanner_id",
            "owner_id",
            "default_permission",
            "creation_date",
            "last_modification_date"
        ],
        "filters": [
            {
                "name": "id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists",
                    "contains"
                ]
            },
            {
                "name": "type",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists",
                    "contains"
                ]
            },
            {
                "name": "scanner_id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "owner_id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "default_permission",
                "logical_type": "Integer",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "creation_date",
                "logical_type": "Date",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between"
                ]
            },
            {
                "name": "last_modification_date",
                "logical_type": "Date",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between"
                ]
            }
        ],
        "sortable_fields": [
            "id",
            "name",
            "type",
            "scanner_id",
            "owner_id",
            "default_permission",
            "creation_date",
            "last_modification_date"
        ]
    },
    'SCANNERS': {},
    'SCANS': {
        "fields": [
            "owner_uuid",
            "created",
            "modified",
            "container_uuid",
            "uuid",
            "name",
            "type",
            "launch_type",
            "schedule_uuid",
            "scanner_uuid",
            "use_tag_rules_as_targets",
            "is_auto_routed",
            "is_pci",
            "is_public",
            "alt_targets_used",
            "is_filtered",
            "is_filter_scheduled",
            "template_uuid",
            "status",
            "job_uuid",
            "terminal_status",
            "last_transition",
            "target_count",
            "is_legacy",
            "schedule_id",
            "is_archived",
            "network_uuid"
        ],
        "filters": [
            {
                "name": "owner_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "created",
                "logical_type": "DateTime",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "modified",
                "logical_type": "DateTime",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "container_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "type",
                "logical_type": "String",
                "types": [
                    "error",
                    "ps",
                    "remote",
                    "sc",
                    "pvs",
                    "lce",
                    "agent",
                    "webapp",
                    "industrial_security"
                ],
                "operators": [
                    "eq",
                    "neq"
                ]
            },
            {
                "name": "launch_type",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "schedule_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "scanner_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "use_tag_rules_as_targets",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "is_auto_routed",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "is_pci",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "is_public",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "alt_targets_used",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "is_filtered",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "is_filter_scheduled",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "template_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "status",
                "logical_type": "String",
                "status": [
                    "initializing",
                    "pending",
                    "running",
                    "pausing",
                    "paused",
                    "resuming",
                    "stopping",
                    "processing",
                    "queued",
                    "completed",
                    "aborted",
                    "canceled",
                    "imported"
                ],
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "job_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "terminal_status",
                "logical_type": "String",
                "status": [
                    "initializing",
                    "pending",
                    "running",
                    "pausing",
                    "paused",
                    "resuming",
                    "stopping",
                    "processing",
                    "queued",
                    "completed",
                    "aborted",
                    "canceled",
                    "imported"
                ],
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_transition",
                "logical_type": "DateTime",
                "operators": [
                    "lt",
                    "gt",
                    "lte",
                    "gte",
                    "between",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "target_count",
                "logical_type": "Long",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "is_legacy",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "schedule_id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "is_archived",
                "logical_type": "boolean",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "network_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            }
        ],
        "sortable_fields": [
            "owner_uuid",
            "created",
            "modified",
            "container_uuid",
            "name",
            "type",
            "launch_type",
            "schedule_uuid",
            "scanner_uuid",
            "use_tag_rules_as_targets",
            "is_auto_routed",
            "is_pci",
            "is_public",
            "alt_targets_used",
            "is_filtered",
            "is_filter_scheduled",
            "template_uuid",
            "status",
            "job_uuid",
            "terminal_status",
            "last_transition",
            "target_count",
            "is_legacy",
            "schedule_id",
            "is_archived",
            "network_uuid"
        ]
    },
    'TAG_CATEGORIES': {},
    'TAGS': {
        "filters": [{
            "control": {
                "readable_regex": "e.g. 123e4567e89b12d3a456426655440000",
                "type": "entry",
                "regex": ".*"
            },
            "name": "tenable_uuid",
            "readable_name": "Tenable UUID",
            "operators": [
                "eq",
                "neq"
            ]
        },
            {
                "control": {
                    "readable_regex": "e.g. 01:23:45:67:89:AB",
                    "type": "entry",
                    "regex": "^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
                },
                "name": "mac_address",
                "readable_name": "MAC Address",
                "operators": [
                    "eq",
                    "neq"
                ]
            }
        ]
    },
    'VULNERABILITIES': {},
}

WAS_DEFINITIONS = {
    'CONFIGURATIONS': {},
    'FOLDERS': {},
    'PLUGINS': {},
    'VULNERABILITIES': {},
    'SCAN_VULNERABILITIES': {},
    'SCANS': {},
    'TEMPLATES': {},
    'USER_TEMPLATES': {},
}

MSSP_DEFINITIONS = {
    'ACCOUNTS': {
        "fields": [
            "id",
            "container_name",
            "licensed_assets",
            "licensed_assets_limit",
            "licensed_apps",
            "site_id",
            "lms_customer_id",
            "custom_name",
            "sso_username"
        ],
        "filters": [
            {
                "name": "id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "container_name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "licensed_assets",
                "logical_type": "Long",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "licensed_assets_limit",
                "logical_type": "Long",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "licensed_apps",
                "logical_type": "Long",
                "operators": []
            },
            {
                "name": "site_id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "lms_customer_id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "custom_name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "sso_username",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            }
        ],
        "sortable_fields": [
            "id",
            "container_name",
            "licensed_assets",
            "licensed_assets_limit",
            "site_id",
            "lms_customer_id",
            "custom_name",
            "sso_username"
        ]
    },
    'LOGOS': {
        "wild_card_fields": [
            "id",
            "container_uuid",
            "name",
            "filename"
        ],
        "filters": [
            {
                "name": "id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "container_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists",
                    "wc"
                ]
            },
            {
                "name": "filename",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists",
                    "wc"
                ]
            }
        ],
        "sortable_fields": [
            "id",
            "container_uuid",
            "name",
            "filename"
        ]
    },
}

PLATFORM_DEFINITIONS = {
    'CONNECTORS': {
        "fields": [
            "connector_uuid",
            "container_uuid",
            "network_uuid",
            "state",
            "name",
            "schedule",
            "connector_params",
            "cloud_service",
            "data_type",
            "status_message",
            "last_seen_updated",
            "last_operation_begin",
            "last_operation_end",
            "last_operation_end_full",
            "next_available_on",
            "next_available_on_full_sync",
            "created",
            "updated",
            "last_event_seen"
        ],
        "filters": [
            {
                "name": "connector_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "container_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "network_uuid",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "incremental_mode",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "state",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "schedule",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "connector_params",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "cloud_service",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "data_type",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "status_message",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "wc",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_seen_updated",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_operation_begin",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_operation_end",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_operation_end_full",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "next_available_on",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "next_available_on_full_sync",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "created",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "updated",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            },
            {
                "name": "last_event_seen",
                "logical_type": "Datetime",
                "operators": [
                    "between",
                    "lt",
                    "lte",
                    "gt",
                    "gte",
                    "exists",
                    "nexists"
                ]
            }
        ],
        "sortable_fields": [
            "connector_uuid",
            "name",
            "state",
            "last_event_seen",
            "created",
            "updated",
            "cloud_service",
            "data_type",
            "incremental_mode"
        ]
    },
    'GROUPS': {
        "fields": [
            "id",
            "container_id",
            "name",
            "permissions",
            "user_count"
        ],
        "filters": [
            {
                "name": "id",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt"
                ]
            },
            {
                "name": "name",
                "logical_type": "String",
                "operators": [
                    "eq",
                    "neq",
                    "lt",
                    "gt"
                ]
            }
        ],
        "sort": [
            "NA"
        ]
    }
}
