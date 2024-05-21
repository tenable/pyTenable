import pytest
import responses
from responses import matchers
from io import BytesIO


@responses.activate
def test_policy_copy(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/policies/1/copy',
                  json={'something': 'value'}
                  )
    assert nessus.policies.copy(1) == {'something': 'value'}


@responses.activate
def test_policy_create(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/policies',
                  json={'example': 'value'},
                  match=[
                      matchers.json_params_matcher({
                          'uuid': 'abcdef',
                          'settings': {'name': 'example'}
                      })
                  ]
                  )
    assert nessus.policies.create(uuid='abcdef',
                                  settings={'name': 'example'}
                                  ) == {'example': 'value'}


@responses.activate
def test_policy_delete(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/policies/1'
                  )
    nessus.policies.delete(1)


@responses.activate
def test_policy_delete_many(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/policies',
                  json={'deleted': [1, 2, 3]},
                  match=[
                      matchers.json_params_matcher({
                          'ids': [1, 2, 3]
                      })
                  ]
                  )
    assert nessus.policies.delete_many([1, 2, 3]) == [1, 2, 3]


@responses.activate
def test_policy_details(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/policies/1',
                  json={'example': 'value'}
                  )
    assert nessus.policies.details(1) == {'example': 'value'}


@responses.activate
def test_policy_edit(nessus):
    responses.add(responses.PUT,
                  'https://localhost:8834/policies/1',
                  json={'example': 'value'},
                  match=[
                      matchers.json_params_matcher({
                          'uuid': 'abcdef',
                          'settings': {'name': 'example'}
                      })
                  ]
                  )
    assert nessus.policies.edit(1,
                                uuid='abcdef',
                                settings={'name': 'example'}
                                ) == {'example': 'value'}


@responses.activate
def test_policy_import(nessus):
    test_file = BytesIO(b'something to see here')
    responses.add(responses.POST,
                  'https://localhost:8834/file/upload',
                  json={'fileuploaded': 'example'}
                  )
    responses.add(responses.POST,
                  'https://localhost:8834/policies/import',
                  match=[
                      matchers.json_params_matcher({'file': 'example'})
                  ],
                  json={'example': 'value'}
                  )
    assert nessus.policies.import_policy(test_file) == {'example': 'value'}


@responses.activate
def test_policy_export(nessus):
    test_file = BytesIO(b'something to see here')
    responses.add(responses.GET,
                  'https://localhost:8834/policies/1/export/prepare',
                  json={'token': 'abcdef'}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/abcdef/status',
                  json={'status': 'ready'}
                  )
    responses.add(responses.GET,
                  'https://localhost:8834/tokens/abcdef/download',
                  body=test_file.read()
                  )
    test_file.seek(0)
    assert nessus.policies.export_policy(1).read() == test_file.read()


@responses.activate
def test_policy_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/policies',
                  json={'policies': [{'id': 1} for _ in range(20)]}
                  )
    resp = nessus.policies.list()
    assert isinstance(resp, list)
    for item in resp:
        assert item == {'id': 1}
