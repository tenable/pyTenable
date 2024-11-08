import pytest
import responses
from tenable.asm import TenableASM


@responses.activate
def test_asm_smartfolder_list():
    folder = {
        'id': 1264,
        'name': 'Recently Added Assets',
        'hash': None,
        'description': 'SOMETHING',
        'filters': [
            {'column': 'bd.addedtoportfolio', 'type': 'less than', 'value': '7'}
        ],
        'notifications': [
            {
                'type': 'email',
                'enabled': True,
                'email': 'user@company'
            }
        ],
        'current_asset_count': 0,
        'updated_at': '2024-09-11T00:47:20.000Z',
        'stats': {
            'total': 0,
            'domaincount': 0,
            'subdomaincount': 0
        },
        'extra': {
            'columns': [
                'bd.record_type',
                'bd.hostname',
                'bd.ip_address',
                'bd.addedtoportfolio'
            ],
            'view': 'table'
        },
        'template_id': None,
        'shared_at': None,
        'expiration_days': 0
    }
    responses.get(
        'https://nourl/api/1.0/smartfolders',
        json=[folder for _ in range(100)]
    )
    asm = TenableASM(url='https://nourl', api_key='abcdef')
    for item in asm.smart_folders.list():
        assert dict(item) == folder
