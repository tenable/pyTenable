"""Tests for the Tenable Vulnerability Management Recast Rules API."""

import pytest
import responses
from responses import matchers

from tenable.io import TenableIO
from tenable.errors import UnexpectedValueError


RULE_ID = '4c931fce-699c-4052-a43c-c953e71dd37b'
RULE_VALUE = {'filter': {'field': 'plugin_id', 'operator': 'eq', 'value': '19506'}}


@pytest.fixture
def api():
    return TenableIO('access', 'secret')


@responses.activate
def test_recast_rules_create(api):
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/v1/recast/rules',
        json={'id': RULE_ID},
        status=200,
        match=[
            matchers.json_params_matcher(
                {'resource_type': 'HOST', 'rule_value': RULE_VALUE}
            )
        ],
    )

    assert api.recast_rules.create('HOST', RULE_VALUE) == {'id': RULE_ID}


@responses.activate
def test_recast_rules_search(api):
    responses.add(
        responses.POST,
        'https://cloud.tenable.com/v1/recast/rules/search',
        json={'items': [{'id': RULE_ID}]},
        status=200,
        match=[
            matchers.json_params_matcher(
                {
                    'resource_type': ['HOST'],
                    'filter': {'field': 'plugin_id'},
                    'limit': 25,
                    'sort': ['created_at:desc'],
                    'next': 'cursor',
                }
            )
        ],
    )

    result = api.recast_rules.search(
        resource_type=['HOST'],
        filter={'field': 'plugin_id'},
        limit=25,
        sort=['created_at:desc'],
        next='cursor',
    )
    assert result == {'items': [{'id': RULE_ID}]}


@responses.activate
def test_recast_rules_details_edit_delete_and_filters(api):
    responses.add(
        responses.GET,
        f'https://cloud.tenable.com/v1/recast/rules/{RULE_ID}',
        json={'id': RULE_ID},
        status=200,
    )
    responses.add(
        responses.PUT,
        f'https://cloud.tenable.com/v1/recast/rules/{RULE_ID}',
        json={'id': RULE_ID, 'updated': True},
        status=200,
        match=[
            matchers.json_params_matcher(
                {'resource_type': 'HOST', 'rule_value': RULE_VALUE}
            )
        ],
    )
    responses.add(
        responses.DELETE,
        f'https://cloud.tenable.com/v1/recast/rules/{RULE_ID}',
        json={'deleted': True},
        status=200,
    )
    responses.add(
        responses.GET,
        'https://cloud.tenable.com/v1/recast/rules/filters',
        json={'filters': []},
        status=200,
    )

    assert api.recast_rules.details(RULE_ID) == {'id': RULE_ID}
    assert api.recast_rules.edit(RULE_ID, 'HOST', RULE_VALUE) == {
        'id': RULE_ID,
        'updated': True,
    }
    assert api.recast_rules.delete(RULE_ID) == {'deleted': True}
    assert api.recast_rules.filters() == {'filters': []}


def test_recast_rules_validate_arguments(api):
    with pytest.raises(UnexpectedValueError):
        api.recast_rules.create('INVALID', RULE_VALUE)

    with pytest.raises(ValueError):
        api.recast_rules.search(limit=501)
