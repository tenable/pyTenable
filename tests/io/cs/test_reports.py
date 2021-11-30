'''
Test the CS Reports API
'''
import re
import pytest
import responses


@responses.activate
def test_cs_reports_endpoint(api):
    dummy = {'name': 'Example', 'repository': 'Repo', 'tag': 'TagName'}
    responses.add(responses.GET,
                  re.compile(('https://cloud.tenable.com/container-security'
                              '/api/v2/reports/'
                              r'([^/]+)/([^/]+)/([^/]+)'
                              )),
                  json=dummy
                  )
    assert api.cs.reports.report('repi', 'name', 'tag') == dummy
