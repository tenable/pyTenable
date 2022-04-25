import pytest
import responses


RULE = {
    'id': 1,
    'plugin_id': 19506,
    'date': '',
    'host': '192.168.1.1',
    'type': 'recast_critical',
    'owner': 'admin',
    'owner_id': 1
}


@responses.activate
def test_plugin_rules_create(nessus):
    responses.add(responses.POST,
                  'https://localhost:8834/plugin-rules'
                  )
    nessus.plugin_rules.create(plugin_id=19506,
                               type='exclude',
                               host='192.168.1.1',
                               date=1645164000
                               )


@responses.activate
def test_plugin_rules_delete(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/plugin-rules/1'
                  )
    nessus.plugin_rules.delete(1)


@responses.activate
def test_plugin_rules_delete_many(nessus):
    responses.add(responses.DELETE,
                  'https://localhost:8834/plugin-rules'
                  )
    nessus.plugin_rules.delete_many([1, 2, 3])


@responses.activate
def test_plugin_rules_edit(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/plugin-rules/1',
                  json=RULE
                  )
    responses.add(responses.PUT,
                  'https://localhost:8834/plugin-rules/1',
                  json=RULE
                  )
    nessus.plugin_rules.edit(1, host='192.168.1.1')


@responses.activate
def test_plugin_rules_list(nessus):
    responses.add(responses.GET,
                  'https://localhost:8834/plugin-rules',
                  json={'plugin_rules': [RULE for I in range(20)]}
                  )
    resp = nessus.plugin_rules.list()
    assert isinstance(resp, list)
    for item in resp:
        assert item == RULE