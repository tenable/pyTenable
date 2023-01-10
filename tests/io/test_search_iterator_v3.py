'''
Testing the search iterators for V3 endpoints
'''
import pytest
import json

from tenable.io.v3.base.iterators.explore_iterator import SearchIterator

ASSET_DATA = [
    {'types': ['webapp'], 'is_deleted': False, 'sources': ['WAS'], 'ssl_tls_enabled': False,
     'created': '2022-01-25T15:19:17.224Z', 'name': 'target9.pubtarg.bananas.com', 'is_licensed': False,
     'id': '0f19a1a4-d1df-4f8a-a2ec-9cd5f4f3f3c5', 'updated': '2022-01-25T15:21:29.692Z',
     'tags': [{'id': '6167eae5-808a-415a-8400-f3208e5382c5', 'category': 'ABCD', 'value': 'tag111', 'type': 'static'}]},
    {'types': ['webapp'], 'sources': ['WAS'], 'last_licensed_scan_time': '2022-01-25T15:17:50.322Z',
     'created': '2021-10-28T13:47:40.801Z', 'ipv4_addresses': ['44.241.194.21'],
     'homepage_screenshot_url': 'https://cloud.tenable.com/was/v2/attachments/54fd0e88-7377-4755-8e9b-7b944f671de9',
     'tags': [{'id': '6167eae5-808a-415a-8400-f3208e5382c5', 'category': 'ABCD', 'value': 'tag111', 'type': 'static'}],
     'display_ipv4_address': '44.241.194.21', 'first_observed': '2021-10-28T13:47:40.694Z',
     'display_operating_system': 'Linux Kernel 3.10 on CentOS Linux release 7', 'ssl_tls_enabled': False,
     'last_observed': '2022-01-25T15:17:50.322Z', 'name': 'target1.pubtarg.tenablesecurity.com',
     'id': '8a148a61-7f5f-4730-8ac0-ebcebcbd6a4d', 'updated': '2022-01-25T15:22:22.966Z'}

]


NULL_PAGINATION_RESPONSE = {"findings":[{"finding_id":"f08ca39b-7341-493d-9b13-38d916b0b526","id":"f08ca39b-7341-493d-9b13-38d916b0b526","severity":0,"state":"ACTIVE","output":"<output>","proof":"HTTP/2 302 ","definition":{"id":98050,"name":"Interesting Response","family":"Web Applications","severity":0,"description":"The scanner identified some responses with a status code other than the usual 200 (OK), 301 (Moved Permanently), 302 (Found) and 404 (Not Found) codes. These codes can provide useful insights into the behavior of the web application and identify any unexpected responses to be addressed.","see_also":["http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html","https://en.wikipedia.org/wiki/List_of_HTTP_status_codes"],"type":"REMOTE","plugin_published":"2017-03-31T00:00:00Z","plugin_updated":"2021-06-14T00:00:00Z","exploited_by_malware":False,"in_the_news":False,"vpr":{},"cvss2":{},"cvss3":{},"references":[{"type":"owasp_api_2019","ids":[]},{"type":"owasp_2010","ids":[]},{"type":"owasp_2013","ids":[]},{"type":"owasp_2017","ids":[]},{"type":"owasp_2021","ids":[]},{"type":"owasp_asvs","ids":[]},{"type":"cwe","ids":[]},{"type":"cve","ids":[]},{"type":"cpe","ids":[]},{"type":"wasc","ids":[]},{"type":"bid","ids":[]},{"type":"capec","ids":[]},{"type":"hipaa","ids":[]},{"type":"iso","ids":[]},{"type":"nist","ids":[]},{"type":"disa_stig","ids":[]},{"type":"pci_dss","ids":[]}],"exploit_frameworks":[{"type":"canvas","ids":[]},{"type":"metasploit","ids":[]},{"type":"d2_elliot","ids":[]},{"type":"exploithub","ids":[]},{"type":"core","ids":[]}]},"asset":{"id":"fdc75396-58ec-4238-a273-f680df71c74d","name":"target1.test.com","ipv4_addresses":["11.22.33.44"]}},{"finding_id":"f17dd97c-2b4c-4967-94e2-127365a04281","id":"f17dd97c-2b4c-4967-94e2-127365a04281","severity":0,"state":"ACTIVE","output":"<OUTPUT>","definition":{"id":98059,"name":"Technologies Detected","family":"Web Applications","severity":0,"description":"This is an informational plugin to inform the user what technologies the framework has detected on the target application, which can then be examined and checked for known vulnerable software versions","solution":"Only use components that do not have known vulnerabilities, only use components that when combined to not introduce a security vulnerability, and ensure that a misconfiguration does not cause any vulnerabilities","see_also":[],"type":"REMOTE","plugin_published":"2017-12-06T00:00:00Z","plugin_updated":"2017-12-11T00:00:00Z","exploited_by_malware":False,"in_the_news":False,"vpr":{},"cvss2":{},"cvss3":{},"references":[{"type":"owasp_api_2019","ids":[]},{"type":"owasp_2010","ids":[]},{"type":"owasp_2013","ids":[]},{"type":"owasp_2017","ids":[]},{"type":"owasp_2021","ids":[]},{"type":"owasp_asvs","ids":[]},{"type":"cwe","ids":[]},{"type":"cve","ids":[]},{"type":"cpe","ids":[]},{"type":"wasc","ids":[]},{"type":"bid","ids":[]},{"type":"capec","ids":[]},{"type":"hipaa","ids":[]},{"type":"iso","ids":[]},{"type":"nist","ids":[]},{"type":"disa_stig","ids":[]},{"type":"pci_dss","ids":[]}],"exploit_frameworks":[{"type":"canvas","ids":[]},{"type":"metasploit","ids":[]},{"type":"d2_elliot","ids":[]},{"type":"exploithub","ids":[]},{"type":"core","ids":[]}]},"asset":{"id":"49b16c8f-74fc-49e2-a945-02edca369bc5","name":"revoked.badssl.com","ipv4_addresses":[]}}],"pagination":None}


@pytest.mark.vcr()
def test_search_iterator_v3(api):
    '''
    Test for search iterator
    '''
    search_iterator = SearchIterator(
        api=api,
        _resource='assets',
        _path='api/v3/assets/search',
        _payload={
            "limit": 1,
            "filter": {
                "and": [
                    {
                        "operator": "eq",
                        "property": "tags",
                        "value": [
                            "6167eae5-808a-415a-8400-f3208e5382c5"
                        ]
                    },
                    {
                        "operator": "eq",
                        "property": "types",
                        "value": "webapp"
                    },
                    {
                        "operator": "neq",
                        "property": "types",
                        "value": "host"
                    }
                ]
            }
        }
    )
    assert ASSET_DATA.__contains__(next(search_iterator))
    assert ASSET_DATA.__contains__(next(search_iterator))

    with pytest.raises(StopIteration):
        next(search_iterator)


def test_search_iterator_v3_null_pagination(api):
    '''
    Test for null pagination in SearchIterator._process_response
    '''
    search_iterator = SearchIterator(
        api=api
    )
    class TempJson:
        def json(self):
            return json.loads(json.dumps({'findings': [{'id': 'abcdef'}],
                                          'pagination': None
                                          })
                              )
    search_iterator._resource = "findings"
    search_iterator._process_response(TempJson())
    assert search_iterator.total == None
    assert search_iterator._next_token == None
