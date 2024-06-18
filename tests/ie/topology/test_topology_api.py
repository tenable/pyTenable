import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_topology_get_representation(api):
    responses.add(responses.GET,
                  f'{RE_BASE}/profiles/1/topology',
                  json={
                      "infrastructures": [{
                          "uid": "string",
                          "name": "some_name",
                          "known": True,
                          "directories": [{
                              "uid": "string",
                              "name": "string",
                              "known": True,
                              "id": 0
                          }]
                      }],
                      "trusts": [{
                          "from": "string",
                          "to": "string",
                          "hazardLevel": "regular",
                          "attributes": ["string"]
                      }]})
    resp = api.topology.details(profile_id='1')
    assert isinstance(resp, dict)
    assert isinstance(resp['infrastructures'], list)
    assert isinstance(resp['trusts'], list)
    assert resp['infrastructures'][0]['name'] == 'some_name'
    assert resp['trusts'][0]['hazard_level'] == 'regular'
