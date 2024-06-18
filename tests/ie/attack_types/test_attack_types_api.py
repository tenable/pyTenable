import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_attack_types_list(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/attack-types',
                  json=[{
                      "id": 1,
                      "name": "test",
                      "yaraRules": "attack type rules",
                      "description": "attack type description",
                      "workloadQuota": 3,
                      "mitreAttackDescription": "mitre_attack_description",
                      "criticity": "critical",
                      "resources": [{
                          "name": "resource name",
                          "url": "https://test.domain.com",
                          "type": "resource type"
                      }],
                      "vectorTemplate": "vector_template",
                      "vectorTemplateReplacements": [{
                          "name": "user",
                          "valueType": "string"
                      }]
                  }]
                  )
    resp = api.attack_types.list()
    assert isinstance(resp, list)
    assert len(resp) == 1
    assert resp[0]['id'] == 1
    assert resp[0]['name'] == 'test'
    assert resp[0]['yara_rules'] == 'attack type rules'
    assert resp[0]['mitre_attack_description'] == 'mitre_attack_description'

