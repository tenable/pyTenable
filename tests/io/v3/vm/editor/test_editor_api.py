from pathlib import Path

import pytest
import responses

from .objects import (CONFIGURATION_DETAILS, CONFIGURATION_ID, ETYPE,
                      FAMILY_ID, FILE_ID, OBJECT_ID, PLUGIN_DETAILS, PLUGIN_ID,
                      POLICY_ID, TEMPLATE_DETAILS, TEMPLATE_ID)

EDITOR_BASE_URL = 'https://cloud.tenable.com/api/v3/editor'

RESP_EXPECTED = {
    'settings': {
        'name': 'KitchenSinkScan',
        'acls': [
            {
                'permissions': 0,
                'owner': None,
                'display_name': None,
                'name': None,
                'id': None,
                'type': 'default'
            }
        ],
    },
    'id': '04a0d852-0dc2-4e62-874d-a81e33b4a9f24e51e1f403febe40'
}


@responses.activate
def test_obj_details(api):
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/{CONFIGURATION_ID}',
        json=CONFIGURATION_DETAILS
    )
    resp = api.v3.vm.editor.obj_details(ETYPE, CONFIGURATION_ID)
    assert resp == CONFIGURATION_DETAILS


@responses.activate
def test_search_templates(api):
    with pytest.raises(NotImplementedError):
        api.v3.vm.editor.search_templates()


@responses.activate
def test_template_details(api):
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/templates/{TEMPLATE_ID}',
        json=TEMPLATE_DETAILS
    )
    resp = api.v3.vm.editor.template_details(ETYPE, TEMPLATE_ID)
    assert resp == TEMPLATE_DETAILS


@responses.activate
def test_plugin_details(api):
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/policy/{POLICY_ID}/families/{FAMILY_ID}/plugins'
        f'/{PLUGIN_ID}',
        json=PLUGIN_DETAILS
    )
    resp = api.v3.vm.editor.plugin_details(POLICY_ID, FAMILY_ID, PLUGIN_ID)
    assert resp == PLUGIN_DETAILS['plugindescription']


@responses.activate
def test_audits(api):
    sample_report = Path(__file__).parent / Path('audit.txt')

    with open(sample_report, 'rb') as report:
        file_contents = report.read()

    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/{OBJECT_ID}/audits/{FILE_ID}',
        body=file_contents
    )

    received_report = Path(__file__).parent / Path('downloaded_audit.txt')
    with open(received_report, 'wb') as report:
        api.v3.vm.editor.audits(ETYPE, OBJECT_ID, FILE_ID, report)

    with open(received_report, 'rb') as report:
        assert report.read() == file_contents

    received_report.unlink()


@responses.activate
def test_details(api):
    responses.add(
        responses.GET,
        f'{EDITOR_BASE_URL}/{ETYPE}/{CONFIGURATION_ID}',
        json=CONFIGURATION_DETAILS
    )
    resp = api.v3.vm.editor.details(ETYPE, CONFIGURATION_ID)

    assert resp == RESP_EXPECTED
