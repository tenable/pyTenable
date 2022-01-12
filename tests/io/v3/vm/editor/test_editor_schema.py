'''
Test Editor Schema
'''
from tenable.io.v3.vm.editor.schema import EditorSchema, EditorTemplateSchema


def test_editor_schema():
    '''
    Test editor schema
    '''
    payload = {
        'etype': 'policy'
    }
    schema = EditorSchema()
    response = schema.dump(schema.load(payload))
    assert response == payload


def test_editor_template_schema():
    '''
    Test editor template schema
    '''
    payload = {
        'etype': 'remediation'
    }
    schema = EditorTemplateSchema()
    response = schema.dump(schema.load(payload))
    assert response == payload
