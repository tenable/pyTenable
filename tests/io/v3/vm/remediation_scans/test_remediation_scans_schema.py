'''
Testing schema for remediation scans
'''

from tenable.io.v3.vm.remediation_scans.schema import \
    RemScansDocumentCreateSchema


def test_scan_document_create():
    '''
    Test schema for create document
    '''
    data = {
        'name': 'test',
        'template': 'advanced',
        'scanner': 'test',
        'targets': ['127.0.0.1', '0.0.0.0'],
        'credentials': {},
        'compliance': {},
        'enabled_plugins': [111, 124, 234]
    }

    validated_data = {
        'template': 'advanced',
        'name': 'test',
        'credentials': {},
        'scanner': 'test',
        'enabled_plugins': [111, 124, 234],
        'compliance': {},
        'targets': '127.0.0.1,0.0.0.0'
    }
    context_data = dict()
    context_data['templates_choices'] = ['advanced']
    context_data['scanners_choices'] = ['test']
    schema = RemScansDocumentCreateSchema(context=context_data)
    payload = schema.dump(schema.load(data))
    assert payload == validated_data
