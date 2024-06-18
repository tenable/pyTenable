'''tests for checker APIs'''
import responses

from tests.ie.conftest import RE_BASE


@responses.activate
def test_checker_list(api):
    '''testing the list response with the actual list response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/checkers',
                  json=[{
                      "id": 0,
                      "codename": "C-toto-s",
                      "categoryId": 0,
                      "remediationCost": 0,
                      "name": "test",
                      "description": "desc",
                      "execSummary": "summary",
                      "vulnerabilityDetail": {
                          "detail": "vuln_detail"
                      },
                      "attackerKnownTools": [{
                          "name": "test",
                          "url": "test@tenable.com",
                          "author": "Mac"
                      }],
                      "resources": [{
                          "name": "cyberc",
                          "url": "cyberc@tenable.com",
                          "type": "book"
                      }],
                      "recommendation": {
                          "name": "recommended_name",
                          "description": "about",
                          "execSummary": "summary",
                          "detail": "details",
                          "resources": [{
                              "name": "cyberc1",
                              "url": "cyberc1@tenable.com",
                              "type": "book1"
                          }]
                      }
                  }]
                  )
    resp = api.checker.list()
    assert isinstance(resp, list)
    assert resp[0]['name'] == 'test'
    assert resp[0]['attacker_known_tools'][0]['author'] == 'Mac'
    assert resp[0]['resources'][0]['name'] == 'cyberc'
    assert resp[0]['recommendation']['name'] == 'recommended_name'


@responses.activate
def test_checker_details(api):
    '''testing the details response with the actual details response'''
    responses.add(responses.GET,
                  f'{RE_BASE}/checkers/2',
                  json={
                      "id": 2,
                      "codename": "C-toto-s",
                      "categoryId": 0,
                      "remediationCost": 0,
                      "name": "test",
                      "description": "desc",
                      "execSummary": "summary",
                      "vulnerabilityDetail": {
                          "detail": "vuln_detail"
                      },
                      "attackerKnownTools": [{
                          "name": "test",
                          "url": "test@tenable.com",
                          "author": "Mac"
                      }],
                      "resources": [{
                          "name": "cyberc",
                          "url": "cyberc@tenable.com",
                          "type": "book"
                      }],
                      "recommendation": {
                          "name": "recommended_name",
                          "description": "about",
                          "execSummary": "summary",
                          "detail": "details",
                          "resources": [{
                              "name": "cyberc1",
                              "url": "cyberc1@tenable.com",
                              "type": "book1"
                          }]
                      }
                  }
                  )
    resp = api.checker.details(checker_id='2')
    assert isinstance(resp, dict)
    assert resp['name'] == 'test'
    assert resp['attacker_known_tools'][0]['author'] == 'Mac'
    assert resp['resources'][0]['name'] == 'cyberc'
    assert resp['recommendation']['name'] == 'recommended_name'
