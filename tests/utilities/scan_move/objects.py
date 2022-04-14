SCAN_ID = 11

SCAN = {
    "legacy": False,
    "permissions": 128,
    "type": "remote",
    "read": True,
    "last_modification_date": 1430934526,
    "creation_date": 1430933086,
    "status": "complted",
    "uuid": "fd7d0d8e-c0e1-4439-97a5-d5c3a5c2d369ab8f7ecb158c480e",
    "shared": False,
    "user_permissions": 128,
    "owner": "user2@example.com",
    "schedule_uuid": "b0eeabbe-a612-429a-a60e-0f68eafb8c36f60557ee0e264228",
    "timezone": None,
    "rrules": None,
    "starttime": None,
    "enabled": False,
    "control": False,
    "name": "KitchenSinkScan",
    "id": SCAN_ID
}

HISTORY_ID_1 = 10535505
HISTORY_ID_2 = 10535512
SCAN_HISTORIES = {
    "pagination": {
        "offset": 0,
        "total": 8,
        "sort": [
            {
                "order": "DESC",
                "name": "start_date"
            }
        ],
        "limit": 50
    },
    "history": [
        {
            "time_end": 1545945607,
            "scan_id": "fc9dc7c5-8eec-4d39-ad9c-20e833cca69b",
            "id": HISTORY_ID_2,
            "is_archived": True,
            "time_start": 1545945482,
            "visibility": "public",
            "targets": {},
            "status": "canceled"
        },
        {
            "time_end": 1545945457,
            "scan_id": "9e3a89e5-f3d0-4708-9ec9-403a34e7cd5e",
            "id": HISTORY_ID_1,
            "is_archived": True,
            "time_start": 1545945321,
            "visibility": "public",
            "targets": {},
            "status": "completed"
        }
    ]
}

FILE_ID = 778874546

EXPORT_RESP_DATA = {
    'file': FILE_ID,
    'temp_token':
        '995bdb656fc6dc5d76e18ccafe7fbd390618fcd0257e0e1aa121f4412a6f7ecc'
}

SCAN_FILTERS_RESP_DATA = {'filters': [
    {
        'name': 'host.id',
        'readable_name': 'Asset ID',
        'control': {
            'type': 'entry',
            'regex': '[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-'
                     '([0-9a-f]{4}-){3}[0-9a-f]{12})*',
            'readable_regex': '01234567-abcd-ef01-2345-6789abcdef01'
        },
        'operators': [
            'eq',
            'neq',
            'match',
            'nmatch'
        ],
        'group_name': 'None'
    },
    {
        'name': 'tracking.state',
        'readable_name': 'Vulnerability State',
        'control': {
            'type': 'dropdown',
            'list': [
                'New',
                'Fixed',
                'Active',
                'Resurfaced'
            ]
        },
        'operators': [
            'eq',
            'neq'
        ],
        'group_name': 'None'
    }
]}

FILE_UPLOAD_RESP_DATA = {
    'fileuploaded': 'scan_targets.txt'
}

IMPORT_RESP_DATA = {
    'scans': [{
        'timezone': None,
        'last_modification_date': '2019-12-31T20:50:23.635Z',
        'status': 'imported',
        'user_permissions': 128,
        'folder_id': '63d15524-fce5-4555-bcd1-5b3172f41925',
        'owner': 'user2@example.com',
        'control': None,
        'starttime': None,
        'id': 'e192840b-e7cc-4586-a482-4495758ed8560e3fa8eea4c7cb27',
        'rrules': None,
        'creation_date': '2019-12-31T20:50:23.635Z',
        'read': False,
        'name': 'KitchenSinkScan',
        'shared': False
    }]
}
