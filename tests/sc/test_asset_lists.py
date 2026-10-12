"""
test file to test various scenarios in sc asset lists
"""

import os
import uuid

import pytest
import responses
from responses import matchers

from tenable.errors import UnexpectedValueError
from ..checker import check, single


def test_asset_lists_dynamic_rules_constructor_passthrough(tsc):
    """
    test asset lists for dynamic rules constructor pass through.
    """
    data = {'test': 'value'}
    assert data == tsc.asset_lists._dynamic_rules_constructor(data)


def test_asset_lists_dynamic_rules_constructor_typerror(tsc):
    """
    test asset lists for dynamic rules constructor type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._dynamic_rules_constructor(1)


def test_asset_lists_dynamic_rules_constructor_plugin_constraint_type_error(tsc):
    """
    test asset lists for dynamic rules constructor 'plugin_constraint' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._dynamic_rules_constructor(
            ('ip', 'contains', '192.168.', 'dummy')
        )


def test_asset_lists_dynamic_rules_constructor_basic_pass(tsc):
    """
    test asset lists for dynamic rules constructor basic pass
    """
    rule = tsc.asset_lists._dynamic_rules_constructor(
        (
            'any',
            ('dns', 'contains', 'something'),
            ('ip', 'contains', '192.168.'),
            ('severity', 'eq', 1),
        )
    )
    assert rule == {
        'operator': 'any',
        'children': [
            {
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'dns',
                'value': 'something',
            },
            {
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'ip',
                'value': '192.168.',
            },
            {
                'type': 'clause',
                'operator': 'eq',
                'filterName': 'severity',
                'value': {'id': 1},
            },
        ],
    }


def test_asset_lists_dynamic_rules_constructor_recursion_pass(tsc):
    """
    test asset lists for dynamic rules constructor recursion pass
    """
    rule = tsc.asset_lists._dynamic_rules_constructor(
        (
            'any',
            ('dns', 'contains', 'something'),
            ('ip', 'contains', '192.168.'),
            ('severity', 'eq', 1),
            ('all', ('dns', 'contains', 'a'), ('dns', 'contains', 'b')),
        )
    )
    assert rule == {
        'operator': 'any',
        'children': [
            {
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'dns',
                'value': 'something',
            },
            {
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'ip',
                'value': '192.168.',
            },
            {
                'type': 'clause',
                'operator': 'eq',
                'filterName': 'severity',
                'value': {'id': 1},
            },
            {
                'type': 'group',
                'operator': 'all',
                'children': [
                    {
                        'type': 'clause',
                        'operator': 'contains',
                        'filterName': 'dns',
                        'value': 'a',
                    },
                    {
                        'type': 'clause',
                        'operator': 'contains',
                        'filterName': 'dns',
                        'value': 'b',
                    },
                ],
            },
        ],
    }


def test_asset_lists_dynamic_rules_constructor_single_pluginid_constraint(tsc):
    """
    test asset lists for dynamic rules constructor single plugin id constraint
    """
    rule = tsc.asset_lists._dynamic_rules_constructor(
        ('any', ('plugintext', 'contains', 'stuff', 19506))
    )
    assert rule == {
        'operator': 'any',
        'children': [
            {
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'plugintext',
                'value': 'stuff',
                'pluginIDConstraint': '19506',
            }
        ],
    }


def test_asset_lists_dynamic_rules_constructor_multi_pluginid_constraint(tsc):
    """
    test asset lists for dynamic rules constructor multi plugin id constraint
    """
    rule = tsc.asset_lists._dynamic_rules_constructor(
        ('any', ('plugintext', 'contains', 'stuff', [19506, 10180]))
    )
    assert rule == {
        'operator': 'any',
        'children': [
            {
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'plugintext',
                'value': 'stuff',
                'pluginIDConstraint': '19506,10180',
            }
        ],
    }


def test_asset_lists_constructor_type_typeerror(tsc):
    """
    test asset lists for constructor type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(type=1)


def test_asset_lists_constructor_type_unexpectedvalueerror(tsc):
    """
    test asset lists for constructor unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.asset_lists._constructor(type='something')


def test_asset_lists_constructor_prep_typeerror(tsc):
    """
    test asset lists for constructor prep type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(prep='nope')


def test_asset_lists_constructor_name_typeerror(tsc):
    """
    test asset lists for constructor name type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(name=1)


def test_asset_lists_constructor_description_typeerror(tsc):
    """
    test asset lists for constructor description type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(description=1)


def test_asset_lists_constructor_context_typeerror(tsc):
    """
    test asset lists for constructor context type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(context=1)


def test_asset_lists_constructor_tags_typeerror(tsc):
    """
    test asset lists for constructor tags type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(tags=1)


def test_asset_lists_constructor_template_typeerror(tsc):
    """
    test asset lists for constructor template type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(template='one')


def test_asset_lists_constructor_filename_typeerror(tsc):
    """
    test asset lists for constructor filename type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(filename=1)


@responses.activate
def test_asset_lists_constructor_data_fields_typeerror(tsc):
    """
    test asset lists for constructor 'data fields' type error
    """
    responses.post(
        'https://nourl/rest/file/upload',
        json={'error_code': 0, 'response': {'filename': 'scfile_VKzbkj'}},
    )
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(data_fields=1)
    with open('file.xml', 'w+') as file:
        with pytest.raises(TypeError):
            tsc.asset_lists._constructor(data_fields=1, fobj=file)
    os.remove('file.xml')


def test_asset_lists_constructor_combinations_typeerror(tsc):
    """
    test asset lists for constructor combinations type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(combinations=1)


def test_asset_lists_constructor_combinations_tuple_typeerror(tsc):
    """
    test asset lists for constructor 'combinations tuple' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(combinations=(1, 2, 3, 4))
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(combinations=(1,))


def test_asset_lists_constructor_rules_typeerror(tsc):
    """
    test asset lists for constructor rules type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(rules=1)


def test_asset_lists_constructor_dns_names_typeerror(tsc):
    """
    test asset lists for constructor 'dns names' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(dns_names=1)


def test_asset_lists_constructor_dns_names_item_typeerror(tsc):
    """
    test asset lists constructor for 'dns names item' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(dns_names=[1])


def test_asset_lists_constructor_dn_requirements_unmet(tsc):
    """
    test asset lists constructor for 'dns requirements unmet' type error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.asset_lists._constructor(dn='domething')


def test_asset_lists_constructor_dn_typeerror(tsc):
    """
    test asset lists constructor for dns type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(dn=1, search_string='a', ldap_id=1)


def test_asset_lists_constructor_search_string_typeerror(tsc):
    """
    test asset lists constructor for 'search string' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(dn='a', search_string=1, ldap_id=1)


def test_asset_lists_constructor_ldap_id_typeerror(tsc):
    """
    test asset lists constructor for 'ldap id' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(dn='a', search_string='a', ldap_id='one')


def test_asset_lists_constructor_ips_typeerror(tsc):
    """
    test asset lists constructor for ips type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(ips=1)


def test_asset_lists_constructor_ips_list_item_typeerror(tsc):
    """
    test asset lists constructor for 'ips list item' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(
            ips=[
                1,
            ]
        )


def test_asset_lists_constructor_filters_typeerror(tsc):
    """
    test asset lists constructor for filters type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(filters=1)


def test_asset_lists_constructor_filters_item_typeerror(tsc):
    """
    test asset lists constructor for 'filters item' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(
            filters=[
                1,
            ]
        )


def test_asset_lists_constructor_filters_tuple_name_typeerror(tsc):
    """
    test asset lists constructor for 'filters tuple name' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(filters=[(1, 'eq', 'something')])


def test_asset_lists_constructor_filters_tuple_operator_typeerror(tsc):
    """
    test asset lists constructor for 'filters tuple operator' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(filters=[('name', 1, 'something')])


def test_asset_lists_constructor_filters_tuple_value_typeerror(tsc):
    """
    test asset lists constructor for 'filters tuple value' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(filters=[('name', 'eq', 1)])


def test_asset_lists_constructor_tool_typeerror(tsc):
    """
    test asset lists constructor for tool type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(tool=1)


def test_asset_lists_constructor_source_type_typeerror(tsc):
    """
    test asset lists constructor for 'source type' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(source_type=1)


def test_asset_lists_constructor_start_offset_typeerror(tsc):
    """
    test asset lists constructor for 'start offset' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(start_offset='one')


def test_asset_lists_constructor_end_offset_typeerror(tsc):
    """
    test asset lists constructor for 'end offset' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(end_offset='one')


def test_asset_lists_constructor_view_typeerror(tsc):
    """
    test asset lists constructor for view type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(view=1)


def test_asset_lists_constructor_lce_id_typeerror(tsc):
    """
    test asset lists constructor for 'lce id' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(lce_id='one')


def test_asset_lists_constructor_sort_field_typeerror(tsc):
    """
    test asset lists constructor for 'sort field' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(sort_field=1)


def test_asset_lists_constructor_sort_dir_typeerror(tsc):
    """
    test asset lists constructor for 'sort dir' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(sort_dir=1)


def test_asset_lists_constructor_sort_field_unexpectedvalueerror(tsc):
    """
    test asset lists constructor for 'sort field' unexpected value error
    """
    with pytest.raises(UnexpectedValueError):
        tsc.asset_lists._constructor(sort_dir='something')


def test_asset_lists_constructor_scan_id_typeerror(tsc):
    """
    test asset lists constructor for 'scan id' type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists._constructor(scan_id='one')


def test_asset_lists_constructor_success(tsc):
    """
    test asset lists constructor for success
    """
    resp = tsc.asset_lists._constructor(
        name='name',
        description='description',
        type='upload',
        prep=True,
        context='context',
        tags='tag',
        template=1,
        filename='fobj',
        data_fields=list(),
        combinations=dict(),
        rules=dict(),
        dns_names=['name1', 'name2'],
        dn='company.tld',
        search_string='*',
        ldap_id=1,
        ips=[
            '192.168.0.1',
        ],
        source_type='type',
        exclude_managed_ips=True,
        filters=[('name', 'eq', 'value')],
        tool='sumip',
        start_offset=0,
        end_offset=1000,
        view='view',
        lce_id=1,
        sort_field='field',
        sort_dir='asc',
        scan_id=1,
    )
    assert resp == {
        'name': 'name',
        'description': 'description',
        'type': 'upload',
        'prepare': 'true',
        'context': 'context',
        'tags': 'tag',
        'template': {'id': 1},
        'filename': 'fobj',
        'assetDataFields': [],
        'combinations': {},
        'rules': {},
        'sourceType': 'type',
        'definedDNSNames': 'name1,name2',
        'definedLDAPQuery': {
            'searchBase': 'company.tld',
            'searchString': '*',
            'ldap': {'id': 1},
        },
        'definedIPs': '192.168.0.1',
        'excludeManagedIPs': 'true',
        'filters': [{'filterName': 'name', 'operator': 'eq', 'value': 'value'}],
        'tool': 'sumip',
        'startOffset': 0,
        'endOffset': 1000,
        'view': 'view',
        'lce': {'id': 1},
        'sortField': 'field',
        'sortDir': 'ASC',
        'scanID': 1,
    }


@pytest.fixture
def asset_list():
    """
    test fixture for asset list
    """
    return {
        'id': '35',
        'name': 'Example',
        'type': 'static',
        'description': '',
        'tags': '',
        'context': '',
        'status': '0',
        'createdTime': '1560968580',
        'modifiedTime': '1560968580',
        'ipCount': -1,
        'canUse': 'true',
        'canManage': 'true',
    }


@responses.activate
def test_asset_lists_create_success(tsc):
    """
    test asset lists create for success
    """
    responses.post(
        'https://nourl/rest/asset',
        json={
            'type': 'regular',
            'response': {
                'id': '35',
                'name': 'Example',
                'type': 'static',
                'description': '',
                'tags': '',
                'context': '',
                'status': '0',
                'createdTime': '1560968580',
                'modifiedTime': '1560968580',
                'typeFields': {'definedIPs': '192.168.0.1'},
                'repositories': [
                    {
                        'ipCount': '-1',
                        'repository': {'id': '1', 'name': 'Default', 'description': ''},
                    }
                ],
                'ipCount': -1,
                'groups': [],
                'assetDataFields': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1560968580,
        },
    )
    asset_list = tsc.asset_lists.create(
        'Example',
        'static',
        ips=[
            '192.168.0.1',
        ],
    )
    assert isinstance(asset_list, dict)
    check(asset_list, 'id', str)
    check(asset_list, 'name', str)
    check(asset_list, 'type', str)
    check(asset_list, 'description', str)
    check(asset_list, 'tags', str)
    check(asset_list, 'context', str)
    check(asset_list, 'status', str)
    check(asset_list, 'createdTime', str)
    check(asset_list, 'modifiedTime', str)
    check(asset_list, 'typeFields', dict)
    for key in asset_list['typeFields']:
        check(asset_list['typeFields'], key, str)
    check(asset_list, 'ipCount', int)
    check(asset_list, 'repositories', list)
    for repository in asset_list['repositories']:
        check(repository, 'ipCount', str)
        check(repository, 'repository', dict)
        check(repository['repository'], 'id', str)
        check(repository['repository'], 'name', str)
        check(repository['repository'], 'description', str)
    check(asset_list, 'assetDataFields', list)
    check(asset_list, 'groups', list)
    check(asset_list, 'canUse', str)
    check(asset_list, 'canManage', str)
    check(asset_list, 'creator', dict)
    check(asset_list['creator'], 'id', str)
    check(asset_list['creator'], 'firstname', str)
    check(asset_list['creator'], 'lastname', str)
    check(asset_list['creator'], 'username', str)
    check(asset_list, 'owner', dict)
    check(asset_list['owner'], 'id', str)
    check(asset_list['owner'], 'firstname', str)
    check(asset_list['owner'], 'lastname', str)
    check(asset_list['owner'], 'username', str)
    check(asset_list, 'ownerGroup', dict)
    check(asset_list['ownerGroup'], 'id', str)
    check(asset_list['ownerGroup'], 'name', str)
    check(asset_list['ownerGroup'], 'description', str)


@responses.activate
def test_asset_lists_delete_success(tsc, asset_list):
    """
    test asset lists delete for success
    """
    responses.delete(
        'https://nourl/rest/asset/35',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1560968580,
        },
    )
    tsc.asset_lists.delete(int(asset_list['id']))


@responses.activate
def test_asset_lists_details_success_for_fields(tsc, asset_list):
    """
    test asset lists details success for fields
    """
    responses.get(
        'https://nourl/rest/asset/35',
        json={
            'type': 'regular',
            'response': {
                'id': '35',
                'name': 'Example',
                'type': 'static',
                'description': '',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1626785131,
        },
        match=[
            matchers.query_param_matcher(
                {'fields': 'id,name,type,description', 'orgID': '1'}
            )
        ],
    )
    asset = tsc.asset_lists.details(
        int(asset_list['id']), 1, fields=['id', 'name', 'type', 'description']
    )
    assert isinstance(asset, dict)
    check(asset, 'id', str)
    check(asset, 'name', str)
    check(asset, 'type', str)
    check(asset, 'description', str)


@responses.activate
def test_asset_lists_details_success(tsc, asset_list):
    """
    test asset lists details for success
    """
    responses.get(
        'https://nourl/rest/asset/1',
        json={
            'type': 'regular',
            'response': {
                'id': '1',
                'name': 'Example',
                'type': 'static',
                'description': '',
                'tags': '',
                'context': '',
                'status': '0',
                'createdTime': '1626785130',
                'modifiedTime': '1626785130',
                'ioSyncStatus': 'Not Synced',
                'ioFirstSyncTime': '-1',
                'ioLastSyncSuccess': '-1',
                'ioLastSyncFailure': '-1',
                'ioSyncErrorDetails': None,
                'typeFields': {'definedIPs': '192.168.0.1'},
                'repositories': [
                    {
                        'ipCount': '-1',
                        'repository': {
                            'id': '5',
                            'name': 'Ministry of Magic - Hogwarts',
                            'description': '',
                        },
                    }
                ],
                'ipCount': -1,
                'groups': [],
                'assetDataFields': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '1',
                    'username': 'secmanager',
                    'firstname': '',
                    'lastname': '',
                },
                'owner': {
                    'id': '1',
                    'username': 'secmanager',
                    'firstname': '',
                    'lastname': '',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1626785131,
        },
        match=[matchers.query_param_matcher({'orgID': '1'})],
    )
    asset = tsc.asset_lists.details(1, 1)
    assert isinstance(asset, dict)
    check(asset, 'id', str)
    check(asset, 'name', str)
    check(asset, 'type', str)
    check(asset, 'description', str)
    check(asset, 'tags', str)
    check(asset, 'context', str)
    check(asset, 'status', str)
    check(asset, 'createdTime', str)
    check(asset, 'modifiedTime', str)
    check(asset, 'typeFields', dict)
    for key in asset['typeFields']:
        check(asset['typeFields'], key, str)
    check(asset, 'ipCount', int)
    check(asset, 'repositories', list)
    for repository in asset['repositories']:
        check(repository, 'ipCount', str)
        check(repository, 'repository', dict)
        check(repository['repository'], 'id', str)
        check(repository['repository'], 'name', str)
        check(repository['repository'], 'description', str)
    check(asset, 'assetDataFields', list)
    check(asset, 'groups', list)
    check(asset, 'canUse', str)
    check(asset, 'canManage', str)
    check(asset, 'creator', dict)
    check(asset['creator'], 'id', str)
    check(asset['creator'], 'firstname', str)
    check(asset['creator'], 'lastname', str)
    check(asset['creator'], 'username', str)
    check(asset, 'owner', dict)
    check(asset['owner'], 'id', str)
    check(asset['owner'], 'firstname', str)
    check(asset['owner'], 'lastname', str)
    check(asset['owner'], 'username', str)
    check(asset, 'ownerGroup', dict)
    check(asset['ownerGroup'], 'id', str)
    check(asset['ownerGroup'], 'name', str)
    check(asset['ownerGroup'], 'description', str)


@responses.activate
def test_asset_lists_edit_success(tsc, asset_list):
    """
    test asset lists edit for success
    """
    responses.patch(
        'https://nourl/rest/asset/35',
        json={
            'type': 'regular',
            'response': {
                'id': '39',
                'name': 'Updated',
                'type': 'static',
                'description': '',
                'tags': '',
                'context': '',
                'status': '0',
                'createdTime': '1560971662',
                'modifiedTime': '1560971662',
                'typeFields': {'definedIPs': '192.168.0.1'},
                'repositories': [
                    {
                        'ipCount': '-1',
                        'repository': {'id': '1', 'name': 'Default', 'description': ''},
                    }
                ],
                'ipCount': -1,
                'groups': [],
                'assetDataFields': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1560971662,
        },
    )
    asset = tsc.asset_lists.edit(int(asset_list['id']), name='Updated')
    assert isinstance(asset, dict)
    check(asset, 'id', str)
    check(asset, 'name', str)
    check(asset, 'type', str)
    check(asset, 'description', str)
    check(asset, 'tags', str)
    check(asset, 'context', str)
    check(asset, 'status', str)
    check(asset, 'createdTime', str)
    check(asset, 'modifiedTime', str)
    check(asset, 'typeFields', dict)
    for key in asset['typeFields']:
        check(asset['typeFields'], key, str)
    check(asset, 'ipCount', int)
    check(asset, 'repositories', list)
    for repository in asset['repositories']:
        check(repository, 'ipCount', str)
        check(repository, 'repository', dict)
        check(repository['repository'], 'id', str)
        check(repository['repository'], 'name', str)
        check(repository['repository'], 'description', str)
    check(asset, 'assetDataFields', list)
    check(asset, 'groups', list)
    check(asset, 'canUse', str)
    check(asset, 'canManage', str)
    check(asset, 'creator', dict)
    check(asset['creator'], 'id', str)
    check(asset['creator'], 'firstname', str)
    check(asset['creator'], 'lastname', str)
    check(asset['creator'], 'username', str)
    check(asset, 'owner', dict)
    check(asset['owner'], 'id', str)
    check(asset['owner'], 'firstname', str)
    check(asset['owner'], 'lastname', str)
    check(asset['owner'], 'username', str)
    check(asset, 'ownerGroup', dict)
    check(asset['ownerGroup'], 'id', str)
    check(asset['ownerGroup'], 'name', str)
    check(asset['ownerGroup'], 'description', str)


@responses.activate
def test_asset_lists_list_success_for_fields(tsc):
    """
    test asset lists "list success for fields"
    """
    responses.get(
        'https://nourl/rest/asset',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {'id': '0', 'name': 'All Defined Ranges'},
                    {'id': '2', 'name': 'Systems that have been Scanned'},
                ],
                'manageable': [
                    {'id': '1', 'name': 'Systems Discovered Passively'},
                    {'id': '2', 'name': 'Systems that have been Scanned'},
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1560973013,
        },
        match=[matchers.query_param_matcher({'fields': 'id,name'})],
    )
    asset_list = tsc.asset_lists.list(fields=['id', 'name'])
    assert isinstance(asset_list, dict)
    check(asset_list, 'usable', list)
    for usable in asset_list['usable']:
        check(usable, 'id', str)
        check(usable, 'name', str)
    check(asset_list, 'manageable', list)
    for manageable in asset_list['manageable']:
        check(manageable, 'id', str)
        check(manageable, 'name', str)


@responses.activate
def test_asset_lists_list_success(tsc):
    """
    test asset lists 'list success'
    """
    responses.get(
        'https://nourl/rest/asset',
        json={
            'type': 'regular',
            'response': {
                'usable': [
                    {
                        'id': '0',
                        'name': 'All Defined Ranges',
                        'description': 'All defining ranges of the Group in whose context this Asset is being evaluated.',
                        'type': 'static',
                        'status': '0',
                    }
                ],
                'manageable': [
                    {
                        'id': '1',
                        'name': 'Systems Discovered Passively',
                        'description': 'This asset uses passive plugins for OS detection and hop detection to identify hosts on the network.',
                        'type': 'dynamic',
                        'status': '0',
                    }
                ],
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1560973013,
        },
    )
    asset_list = tsc.asset_lists.list()
    assert isinstance(asset_list, dict)
    check(asset_list, 'usable', list)
    for usable in asset_list['usable']:
        check(usable, 'id', str)
        check(usable, 'name', str)
        check(usable, 'description', str)
        check(usable, 'status', str)
    check(asset_list, 'manageable', list)
    for manageable in asset_list['manageable']:
        check(manageable, 'id', str)
        check(manageable, 'name', str)
        check(manageable, 'description', str)
        check(manageable, 'status', str)


@responses.activate
def test_asset_lists_refresh_success(tsc, asset_list):
    """
    test asset lists refresh for success
    """
    responses.post(
        'https://nourl/rest/asset/35/refresh',
        json={
            'type': 'regular',
            'response': {'orgID': 1, 'repIDs': [{'id': 1}], 'id': '50'},
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1561038822,
        },
    )
    resp = tsc.asset_lists.refresh(int(asset_list['id']), 1, 1)
    assert isinstance(resp, dict)
    check(resp, 'orgID', int)
    check(resp, 'repIDs', list)


@pytest.mark.datafiles(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '..',
        'test_files',
        'asset_list.xml',
    )
)
@responses.activate
def test_asset_lists_import_definition_success(tsc, datafiles):
    """
    test asset lists import definition for success
    """
    responses.post(
        'https://nourl/rest/file/upload',
        json={
            'type': 'regular',
            'response': {
                'filename': 'SW6CHj',
                'originalFilename': 'asset_list.xml',
                'content': '',
                'context': '',
            },
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1561038575,
        },
    )
    responses.post(
        'https://nourl/rest/asset/import',
        json={
            'type': 'regular',
            'response': {
                'id': '46',
                'name': 'Import Example',
                'type': 'static',
                'description': '',
                'tags': '',
                'context': '',
                'status': '0',
                'createdTime': '1561038575',
                'modifiedTime': '1561038575',
                'ipCount': -1,
                'canUse': 'true',
                'canManage': 'true',
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1561038575,
        },
    )
    with open(os.path.join(str(datafiles), 'asset_list.xml'), 'rb') as fobj:
        tsc.asset_lists.import_definition(fobj, name='name')


@responses.activate
def test_asset_lists_export_definition_success(tsc, asset_list):
    """
    test asset lists export definition for success
    """
    responses.get(
        'https://nourl/rest/asset/35/export',
        body='<?xml version="1.0" encoding="UTF-8"?>\n<assets><asset><name>Example</name><type>static</type></asset></assets>',
        content_type='text/xml',
        headers={'Content-Disposition': 'attachment; filename="asset.47.1.xml"'},
    )
    with open('asset_list_export.xml', 'wb') as fobj:
        tsc.asset_lists.export_definition(int(asset_list['id']), fobj)
    os.remove('asset_list_export.xml')


@responses.activate
def test_asset_lists_export_definition_success_no_file(tsc):
    """
    test asset lists export definition success with no file
    """
    responses.get(
        'https://nourl/rest/asset/1000007/export',
        body='No Content',
        content_type='text/xml',
        headers={'content-disposition': 'attachment; filename="policy.1000014.1.xml"'},
    )
    with open('1000007.xml', 'wb'):
        tsc.asset_lists.export_definition(1000007)
    os.remove('1000007.xml')


@pytest.mark.skip(reason='No LDAP Service to query against')
def test_asset_lists_ldap_query_success(tsc):
    """
    test asset lists ldap query for success
    """
    tsc.asset_lists.ldap_query(1, 'company.tld', '*')


@responses.activate
def test_asset_lists_tags_success(tsc):
    """
    test asset lists tags success
    """
    responses.get(
        'https://nourl/rest/asset/tag',
        json={
            'type': 'regular',
            'response': [],
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1561038622,
        },
    )
    tags = tsc.asset_lists.tags()
    for tag in tags:
        single(tag, str)


def test_asset_lists_share_id_typeerror(tsc):
    """
    test asset lists for share id type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists.share('one')


def test_asset_lists_share_group_id_typeerror(tsc):
    """
    test asset lists share for group id type error
    """
    with pytest.raises(TypeError):
        tsc.asset_lists.share(1, 'one')


@responses.activate
def test_asset_lists_share_success(tsc, asset_list, group):
    """
    test asset lists share for success
    """
    responses.post(
        'https://nourl/rest/asset/35/share',
        json={
            'type': 'regular',
            'response': {
                'id': '48',
                'name': 'Example',
                'type': 'static',
                'description': '',
                'tags': '',
                'context': '',
                'status': '0',
                'createdTime': '1561038636',
                'modifiedTime': '1561038636',
                'typeFields': {'definedIPs': '192.168.0.1'},
                'repositories': [
                    {
                        'ipCount': '-1',
                        'repository': {'id': '1', 'name': 'Default', 'description': ''},
                    }
                ],
                'ipCount': -1,
                'groups': [],
                'assetDataFields': [],
                'canUse': 'true',
                'canManage': 'true',
                'creator': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'owner': {
                    'id': '2',
                    'username': 'api',
                    'firstname': 'api',
                    'lastname': 'user',
                },
                'ownerGroup': {
                    'id': '0',
                    'name': 'Full Access',
                    'description': 'Full Access group',
                },
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1561038636,
        },
    )
    asset = tsc.asset_lists.share(int(asset_list['id']), int(group['id']))
    assert isinstance(asset, dict)
    check(asset, 'id', str)
    check(asset, 'name', str)
    check(asset, 'type', str)
    check(asset, 'description', str)
    check(asset, 'tags', str)
    check(asset, 'context', str)
    check(asset, 'status', str)
    check(asset, 'createdTime', str)
    check(asset, 'modifiedTime', str)
    check(asset, 'typeFields', dict)
    for key in asset['typeFields']:
        check(asset['typeFields'], key, str)
    check(asset, 'ipCount', int)
    check(asset, 'repositories', list)
    for repository in asset['repositories']:
        check(repository, 'ipCount', str)
        check(repository, 'repository', dict)
        check(repository['repository'], 'id', str)
        check(repository['repository'], 'name', str)
        check(repository['repository'], 'description', str)
    check(asset, 'assetDataFields', list)
    check(asset, 'groups', list)
    check(asset, 'canUse', str)
    check(asset, 'canManage', str)
    check(asset, 'creator', dict)
    check(asset['creator'], 'id', str)
    check(asset['creator'], 'firstname', str)
    check(asset['creator'], 'lastname', str)
    check(asset['creator'], 'username', str)
    check(asset, 'owner', dict)
    check(asset['owner'], 'id', str)
    check(asset['owner'], 'firstname', str)
    check(asset['owner'], 'lastname', str)
    check(asset['owner'], 'username', str)
    check(asset, 'ownerGroup', dict)
    check(asset['ownerGroup'], 'id', str)
    check(asset['ownerGroup'], 'name', str)
    check(asset['ownerGroup'], 'description', str)


@responses.activate
def test_asset_lists_create_asset_list_check_uuid(tsc):
    responses.post(
        'https://nourl/rest/asset',
        json={
            'type': 'regular',
            'response': {
                'id': '71',
                'name': 'tio_test2',
                'type': 'dynamic',
                'description': '',
                'tags': '',
                'context': '',
                'status': '0',
                'createdTime': '1628680863',
                'modifiedTime': '1628680863',
                'ioSyncStatus': 'Not Synced',
                'ioFirstSyncTime': '-1',
                'ioLastSyncSuccess': '-1',
                'ioLastSyncFailure': '-1',
                'ioSyncErrorDetails': None,
                'ipCount': 0,
                'canUse': 'true',
                'canManage': 'true',
            },
            'error_code': 0,
            'error_msg': '',
            'timestamp': 1628680863,
        },
    )
    responses.delete(
        'https://nourl/rest/asset/71',
        json={
            'type': 'regular',
            'response': '',
            'error_code': 0,
            'error_msg': '',
            'warnings': [],
            'timestamp': 1628680863,
        },
    )
    asset_list = tsc.asset_lists.create(
        'tio_test2', 'dynamic', rules=('any', ('uuid', 'eq', str(uuid.uuid4())))
    )
    tsc.asset_lists.delete(int(asset_list['id']))
