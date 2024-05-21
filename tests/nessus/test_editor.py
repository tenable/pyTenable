import pytest
import responses
from io import BytesIO


@responses.activate
def test_export_audit(nessus):
    test_file = BytesIO(b'something to see here')
    responses.add(responses.GET,
                  'https://localhost:8834/editor/policy/1/audits/1/prepare',
                  json={'token': 'absdef123'}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/absdef123/status',
                  json={'status': 'ready', 'message': 'something'}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/absdef123/download',
                  body=test_file.read()
                  )
    with BytesIO() as example_file:
        nessus.editor.export_audit('policy', 1, 1, fobj=example_file)
        test_file.seek(0)
        assert example_file.read() == test_file.read()


@responses.activate
def test_template_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/editor/scan/templates/abcdef',
                  json={'test': 'abc'}
                  )
    resp = nessus.editor.template_details('scan', 'abcdef')
    assert resp == {'test': 'abc'}


@responses.activate
def test_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/editor/scan/abcdef',
                  json={'test': 'abc'}
                  )
    resp = nessus.editor.details('scan', 'abcdef')
    assert resp == {'test': 'abc'}


@responses.activate
def test_template_list(nessus):
    tmpl = {'example': True, 'string': 'value'}
    responses.add(responses.GET,
                  'https://localhost:8834/editor/policy/templates',
                  json={'templates': [tmpl for _ in range(20)]}
                  )
    resp = nessus.editor.template_list('policy')
    assert isinstance(resp, list)
    for item in resp:
        assert item == tmpl


@responses.activate
def test_plugin_description(nessus):
    responses.add(
        responses.GET,
        'https://localhost:8834/editor/policy/1/families/1/plugins/1',
        json={'plugindescription': {'test': 'abc'}}
    )
    resp = nessus.editor.plugin_description('1', '1', '1')
    assert resp == {'test': 'abc'}
