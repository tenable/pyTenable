"""
test plugins
"""
import re

import pytest
import responses

BASE_URL = "https://cloud.tenable.com/api/v3/plugins"


@pytest.mark.skip("API method NotImplemented in v3")
def test_families(api):
    """
    Test Plugin families API
    """
    pass


@pytest.mark.skip("API method NotImplemented in v3")
def test_list(api):
    """Test Plugin list API"""
    pass


@responses.activate
def test_family_details(api):
    """
    Test Plugins family_details API
    """
    test_response: dict = {
        "id": 1,
        "name": "Web Servers",
        "plugins": [
            {
                "id": 15713,
                "name": "04WebServer Multiple Vulnerabilities (XSS, DoS, more)"
            },
            {
                "id": 11591,
                "name": "12Planet Chat Server Administration Authentication"
                        "Cleartext Credential Disclosure"
            }
        ]
    }
    family_id: int = 1
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/families/{family_id}'),
        json=test_response
    )
    family_details_response = api.v3.vm.plugins.family_details(family_id)
    assert isinstance(family_details_response, dict)


@responses.activate
def test_family_details_with_status_code(api):
    """
    Test Plugins family_details API with response status
    """
    family_id: int = 0
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/families/{family_id}')
    )
    family_details_response = api.v3.vm.plugins.family_details(family_id)
    assert family_details_response.status_code == 200


@responses.activate
def test_plugin_details(api):
    """
    Test case for plugin_details api
    """
    test_reponse: dict = {
        "attributes": [
            {
                "attribute_name": "fname",
                "attribute_value": "04webserver.nasl"
            },
            {
                "attribute_name": "plugin_name",
                "attribute_value": "04WebServer Multiple "
                                   "Vulnerabilities (XSS, DoS, more)"
            }
        ],
        "family_name": "Web Servers",
        "id": 15713,
        "name": "04WebServer Multiple Vulnerabilities (XSS, DoS, more)"
    }
    plugin_id: int = 15713
    responses.add(
        responses.GET,
        re.compile(f'{BASE_URL}/plugin/{plugin_id}'),
        json=test_reponse
    )
    plugin_detail_response = api.v3.vm.plugins.plugin_details(plugin_id)
    assert isinstance(plugin_detail_response, dict)


@responses.activate
def test_plugin_details_with_status_code(api):
    """
    Test case for plugin_details api with response status
    """
    plugin_id: int = 123
    responses.add(responses.GET, re.compile(f'{BASE_URL}/plugin/{plugin_id}'))
    plugin_detail_response = api.v3.vm.plugins.plugin_details(plugin_id)
    assert plugin_detail_response.status_code == 200
