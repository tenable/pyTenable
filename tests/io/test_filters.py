"""
test filters
"""

import responses

from tests.checker import check


@responses.activate
def test_agent_filters(tvm):
    """
    test to get agent filters
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/scans/agents',
        json={
            'wildcard_fields': ['core_version', 'distro', 'groups'],
            'filters': [
                {
                    'name': 'core_version',
                    'readable_name': 'Version',
                    'operators': ['eq', 'neq', 'match'],
                    'control': {
                        'readable_regex': 'X.Y.Z',
                        'type': 'entry',
                        'regex': '.*',
                    },
                }
            ],
            'sort': {'sortable_fields': ['core_version', 'distro', 'ip']},
        },
    )
    filters = tvm.filters.agents_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_workbench_vuln_filters(tvm):
    """
    test to get workbench vulnerabilities filters
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/vulnerabilities',
        json={
            'filters': [
                {
                    'name': 'host.id',
                    'readable_name': 'Asset ID',
                    'control': {
                        'type': 'entry',
                        'regex': '[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*',
                        'readable_regex': '01234567-abcd-ef01-2345-6789abcdef01',
                    },
                    'operators': ['eq', 'neq', 'match'],
                    'group_name': 'vulnerability',
                }
            ]
        },
    )
    filters = tvm.filters.workbench_vuln_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_workbench_asset_filters(tvm):
    """
    test to get workbench asset filters
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/workbenches/assets',
        json={
            'filters': [
                {
                    'name': 'acr_score',
                    'readable_name': 'ACR Score',
                    'operators': ['eq', 'gte', 'lte'],
                    'control': {
                        'type': 'entry',
                        'regex': '^([1-9]|10)$',
                        'readable_regex': 'NUMBER',
                    },
                }
            ]
        },
    )
    filters = tvm.filters.workbench_asset_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_scan_filters(tvm):
    """
    test to get scan filters
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/scans/reports',
        json={
            'filters': [
                {
                    'name': 'host.id',
                    'readable_name': 'Asset ID',
                    'control': {
                        'type': 'entry',
                        'regex': '[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}(,[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})*',
                        'readable_regex': '01234567-abcd-ef01-2345-6789abcdef01',
                    },
                    'operators': ['eq', 'neq', 'match'],
                    'group_name': 'vulnerability',
                }
            ]
        },
    )
    filters = tvm.filters.scan_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_access_group_asset_rules_filters(tvm):
    """
    test to get access group asset rules filters
    """
    responses.add(
        responses.GET,
        'https://nourl/access-groups/rules/filters',
        json={
            'rules': [
                {
                    'operators': ['eq'],
                    'name': 'aws_account',
                    'readable_name': 'AWS Account ID',
                    'placeholder': 'Ex: 12345',
                    'control': {'type': 'tag', 'regex': '^\\d+$'},
                }
            ]
        },
    )
    filters = tvm.filters.access_group_asset_rules_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_access_group_filters(tvm):
    """
    test to get access group filters
    """
    responses.add(
        responses.GET,
        'https://nourl/access-groups/filters',
        json={
            'wildcard_fields': ['name', 'created_by_name', 'updated_by_name'],
            'filters': [
                {
                    'operators': ['eq', 'match'],
                    'control': {'type': 'entry'},
                    'name': 'name',
                    'readable_name': 'Access Group Name',
                },
                {
                    'operators': ['date-lte', 'date-gte', 'date-eq'],
                    'control': {'type': 'datefield'},
                    'name': 'updated_at',
                    'readable_name': 'Last Modified',
                },
            ],
            'sort': {'sortable_fields': ['name', 'created_at', 'created_by_name']},
        },
    )
    filters = tvm.filters.access_group_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_access_group_asset_rules_filters_v2(tvm):
    """
    test to get access group asset rules filters v2
    """
    responses.add(
        responses.GET,
        'https://nourl/v2/access-groups/rules/filters',
        json={
            'rules': [
                {
                    'operators': ['eq'],
                    'name': 'aws_account',
                    'readable_name': 'AWS Account ID',
                    'placeholder': 'Ex: 12345',
                    'control': {'type': 'tag', 'regex': '.*'},
                }
            ]
        },
    )
    filters = tvm.filters.access_group_asset_rules_filters_v2()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_access_group_filters_v2(tvm):
    """
    test to get access group filters v2
    """
    responses.add(
        responses.GET,
        'https://nourl/v2/access-groups/filters',
        json={
            'wildcard_fields': ['name', 'created_by_name', 'updated_by_name'],
            'filters': [
                {
                    'operators': ['eq', 'match'],
                    'control': {'type': 'entry'},
                    'name': 'name',
                    'readable_name': 'Access Group Name',
                },
                {
                    'operators': ['date-lte', 'date-gte', 'date-eq'],
                    'control': {'type': 'datefield'},
                    'name': 'updated_at',
                    'readable_name': 'Last Modified',
                },
            ],
            'sort': {'sortable_fields': ['name', 'created_at', 'created_by_name']},
        },
    )
    filters = tvm.filters.access_group_filters_v2()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_asset_tag_filters(tvm):
    """
    test to get asset tag filters
    """
    responses.add(
        responses.GET,
        'https://nourl/tags/assets/filters',
        json={
            'filters': [
                {
                    'control': {
                        'readable_regex': 'e.g. 123e4567e89b12d3a456426655440000',
                        'type': 'entry',
                        'regex': '.*',
                    },
                    'name': 'tenable_uuid',
                    'readable_name': 'Tenable UUID',
                    'operators': ['eq', 'neq'],
                }
            ]
        },
    )
    filters = tvm.filters.asset_tag_filters()
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_use_cache_true_filters(tvm):
    """
    test to raise the exception use_cache filter is normalized
    """
    responses.add(
        responses.GET,
        'https://nourl/access-groups/rules/filters',
        json={
            'rules': [
                {
                    'operators': ['eq'],
                    'name': 'aws_account',
                    'readable_name': 'AWS Account ID',
                    'placeholder': 'Ex: 12345',
                    'control': {'type': 'tag', 'regex': '.*'},
                }
            ]
        },
    )
    filters = getattr(tvm.filters, '_use_cache')(
        'rules', 'access-groups/rules/filters', 'rules', True
    )
    assert isinstance(filters, dict)
    for data in filters:
        check(filters[data], 'choices', list, allow_none=True)
        check(filters[data], 'operators', list)
        check(filters[data], 'pattern', str, allow_none=True)


@responses.activate
def test_use_cache_false_filters(tvm):
    """
    test to raise the exception use_cache filter is not normalized
    """
    responses.add(
        responses.GET,
        'https://nourl/access-groups/rules/filters',
        json={
            'rules': [
                {
                    'operators': ['eq'],
                    'name': 'aws_account',
                    'readable_name': 'AWS Account ID',
                    'placeholder': 'Ex: 12345',
                    'control': {'type': 'tag', 'regex': '^\\d+$'},
                }
            ]
        },
    )
    filters = getattr(tvm.filters, '_use_cache')(
        'rules', 'access-groups/rules/filters', 'rules', False
    )
    assert isinstance(filters, list)
    for data in enumerate(filters):
        check(data[1], 'operators', list, allow_none=True)
        check(data[1], 'name', str, allow_none=True)
        check(data[1], 'readable_name', str, allow_none=True)
        check(data[1], 'control', dict, allow_none=True)


@responses.activate
def test_filters_credentials_false_filters(tvm):
    """
    test to raise the exception when the credentials filter is not normalized
    """
    responses.add(
        responses.GET,
        'https://nourl/filters/credentials',
        json={
            'filters': [
                {
                    'name': 'name',
                    'readable_name': 'Name',
                    'operators': ['eq', 'neq', 'match'],
                    'control': {'type': 'entry', 'regex': '.*'},
                }
            ]
        },
    )
    filters = tvm.filters.credentials_filters(normalize=False)
    assert isinstance(filters, list)
    for data in enumerate(filters):
        check(data[1], 'name', str, allow_none=True)
        check(data[1], 'readable_name', str, allow_none=True)
        check(data[1], 'operators', list, allow_none=True)
        check(data[1], 'control', dict, allow_none=True)


def test_normalize_name_only_choices(tvm):
    """
    test that _normalize handles list items that only carry a 'name' key
    (e.g. the target_group filter) instead of raising KeyError: 'id'
    """
    filterset = [
        {
            'name': 'target_group',
            'operators': ['eq', 'neq'],
            'control': {
                'type': 'dropdown_multi',
                'list': [{'name': 'mygroup'}],
            },
        }
    ]
    result = getattr(tvm.filters, '_normalize')(filterset)
    assert result['target_group']['choices'] == ['mygroup']
    assert result['target_group']['operators'] == ['eq', 'neq']
    assert result['target_group']['pattern'] is None
