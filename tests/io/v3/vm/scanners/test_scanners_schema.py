'''
Testing the Scanner schemas
'''
from tenable.io.v3.vm.scanners.schema import ScannerEditSchema


def test_scanner_edit_schema():
    '''
    Test the vulnerability finding schema
    '''
    payload = {
        'force_plugin_update': True,
        'force_ui_update': False,
        'finish_update': True,
        'registration_code': 'random_code',
        'aws_update_interval': 60,
    }
    test_resp = {
        'force_plugin_update': 1,
        'finish_update': 1,
        'registration_code': 'random_code',
        'aws_update_interval': 60,
    }
    schema = ScannerEditSchema()
    assert test_resp == schema.dump(schema.load(payload))
