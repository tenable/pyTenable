import os
import pytest
from ..checker import check, single
from tenable.errors import APIError, UnexpectedValueError
from tests.pytenable_log_handler import log_exception


def test_asset_lists_dynamic_rules_constructor_passthrough(sc):
    data = {'test': 'value'}
    assert data == sc.asset_lists._dynamic_rules_constructor(data)


def test_asset_lists_dynamic_rules_constructor_typerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._dynamic_rules_constructor(1)


def test_asset_lists_dynamic_rules_constructor_plugin_constraint_type_error(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._dynamic_rules_constructor(('ip', 'contains', '192.168.', 'dummy'))


def test_asset_lists_dynamic_rules_constructor_basic_pass(sc):
    rule = sc.asset_lists._dynamic_rules_constructor(
        ('any', ('dns', 'contains', 'something'),
         ('ip', 'contains', '192.168.'),
         ('severity', 'eq', 1)))
    assert rule == {
        'operator': 'any',
        'children': [{
            'type': 'clause',
            'operator': 'contains',
            'filterName': 'dns',
            'value': 'something'
        }, {
            'type': 'clause',
            'operator': 'contains',
            'filterName': 'ip',
            'value': '192.168.'
        }, {
            'type': 'clause',
            'operator': 'eq',
            'filterName': 'severity',
            'value': {'id': 1}
        }]
    }


def test_asset_lists_dynamic_rules_constructor_recursion_pass(sc):
    rule = sc.asset_lists._dynamic_rules_constructor(
        ('any', ('dns', 'contains', 'something'),
         ('ip', 'contains', '192.168.'),
         ('severity', 'eq', 1),
         ('all', ('dns', 'contains', 'a'),
          ('dns', 'contains', 'b')
          )
         ))
    assert rule == {
        'operator': 'any',
        'children': [{
            'type': 'clause',
            'operator': 'contains',
            'filterName': 'dns',
            'value': 'something'
        }, {
            'type': 'clause',
            'operator': 'contains',
            'filterName': 'ip',
            'value': '192.168.'
        }, {
            'type': 'clause',
            'operator': 'eq',
            'filterName': 'severity',
            'value': {'id': 1}
        }, {
            'type': 'group',
            'operator': 'all',
            'children': [{
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'dns',
                'value': 'a'
            }, {
                'type': 'clause',
                'operator': 'contains',
                'filterName': 'dns',
                'value': 'b'
            }]
        }]
    }


def test_asset_lists_dynamic_rules_constructor_single_pluginid_constraint(sc):
    rule = sc.asset_lists._dynamic_rules_constructor(
        ('any', ('plugintext', 'contains', 'stuff', 19506)))
    assert rule == {
        'operator': 'any',
        'children': [{
            'type': 'clause',
            'operator': 'contains',
            'filterName': 'plugintext',
            'value': 'stuff',
            'pluginIDConstraint': '19506'
        }]
    }


def test_asset_lists_dynamic_rules_constructor_multi_pluginid_constraint(sc):
    rule = sc.asset_lists._dynamic_rules_constructor(
        ('any', ('plugintext', 'contains', 'stuff', [19506, 10180])))
    assert rule == {
        'operator': 'any',
        'children': [{
            'type': 'clause',
            'operator': 'contains',
            'filterName': 'plugintext',
            'value': 'stuff',
            'pluginIDConstraint': '19506,10180'
        }]
    }


def test_asset_lists_constructor_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(type=1)


def test_asset_lists_constructor_type_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.asset_lists._constructor(type='something')


def test_asset_lists_constructor_prep_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(prep='nope')


def test_asset_lists_constructor_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(name=1)


def test_asset_lists_constructor_description_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(description=1)


def test_asset_lists_constructor_context_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(context=1)


def test_asset_lists_constructor_tags_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(tags=1)


def test_asset_lists_constructor_template_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(template='one')


def test_asset_lists_constructor_filename_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filename=1)


def test_asset_lists_constructor_data_fields_typeerror(sc, vcr):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(data_fields=1)
    with vcr.use_cassette('test_files_upload_clear_success'):
        with open("file.xml", "w+") as file:
            with pytest.raises(TypeError):
                sc.asset_lists._constructor(data_fields=1, fobj=file)
        os.remove("file.xml")


def test_asset_lists_constructor_combinations_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(combinations=1)


def test_asset_lists_constructor_combinations_tuple_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(combinations=(1, 2, 3, 4))
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(combinations=(1,))


def test_asset_lists_constructor_rules_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(rules=1)


def test_asset_lists_constructor_dns_names_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(dns_names=1)


def test_asset_lists_constructor_dns_names_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(dns_names=[1])


def test_asset_lists_constructor_dn_requirements_unmet(sc):
    with pytest.raises(UnexpectedValueError):
        sc.asset_lists._constructor(dn='domething')


def test_asset_lists_constructor_dn_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(dn=1, search_string='a', ldap_id=1)


def test_asset_lists_constructor_search_string_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(dn='a', search_string=1, ldap_id=1)


def test_asset_lists_constructor_ldap_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(dn='a', search_string='a', ldap_id='one')


def test_asset_lists_constructor_ips_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(ips=1)


def test_asset_lists_constructor_ips_list_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(ips=[1, ])



def test_asset_lists_constructor_filters_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filters=1)


def test_asset_lists_constructor_filters_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filters=[1, ])



def test_asset_lists_constructor_filters_tuple_name_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filters=[(1, 'eq', 'something')])


def test_asset_lists_constructor_filters_tuple_operator_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filters=[('name', 1, 'something')])


def test_asset_lists_constructor_filters_tuple_value_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filters=[('name', 'eq', 1)])


def test_asset_lists_constructor_tool_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(tool=1)


def test_asset_lists_constructor_source_type_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(source_type=1)


def test_asset_lists_constructor_start_offset_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(start_offset='one')


def test_asset_lists_constructor_end_offset_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(end_offset='one')


def test_asset_lists_constructor_view_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(view=1)


def test_asset_lists_constructor_lce_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(lce_id='one')


def test_asset_lists_constructor_sort_field_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(sort_field=1)


def test_asset_lists_constructor_sort_dir_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(sort_dir=1)


def test_asset_lists_constructor_sort_field_unexpectedvalueerror(sc):
    with pytest.raises(UnexpectedValueError):
        sc.asset_lists._constructor(sort_dir='something')


def test_asset_lists_constructor_scan_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(scan_id='one')


def test_asset_lists_constructor_success(sc):
    resp = sc.asset_lists._constructor(
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
        ips=['192.168.0.1', ],
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
        scan_id=1
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
        'scanID': 1
    }


@pytest.fixture
def asset_list(request, sc, vcr):
    with vcr.use_cassette('test_asset_lists_create_success'):
        asset_list = sc.asset_lists.create('Example', 'static', ips=['192.168.0.1', ])

    def teardown():
        try:
            with vcr.use_cassette('test_asset_lists_delete_success'):
                sc.asset_lists.delete(int(asset_list['id']))
        except APIError as error:
            log_exception(error)

    request.addfinalizer(teardown)
    return asset_list


@pytest.mark.vcr()
def test_asset_lists_create_success(sc, asset_list):
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


@pytest.mark.vcr()
def test_asset_lists_delete_success(sc, asset_list):
    sc.asset_lists.delete(int(asset_list['id']))


@pytest.mark.vcr()
def test_asset_lists_details_success_for_fields(sc, asset_list):
    asset = sc.asset_lists.details(int(asset_list['id']),
                                   fields=['id', 'name', 'type', 'description'])
    assert isinstance(asset, dict)
    check(asset, 'id', str)
    check(asset, 'name', str)
    check(asset, 'type', str)
    check(asset, 'description', str)


@pytest.mark.vcr()
def test_asset_lists_details_success(sc, asset_list):
    asset = sc.asset_lists.details(int(asset_list['id']))
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


@pytest.mark.vcr()
def test_asset_lists_edit_success(sc, asset_list):
    asset = sc.asset_lists.edit(int(asset_list['id']), name='Updated')
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


@pytest.mark.vcr()
def test_asset_lists_list_success_for_fields(sc):
    asset_list = sc.asset_lists.list(fields=['id', 'name'])
    assert isinstance(asset_list, dict)
    check(asset_list, 'usable', list)
    for usable in asset_list['usable']:
        check(usable, 'id', str)
        check(usable, 'name', str)
    check(asset_list, 'manageable', list)
    for manageable in asset_list['manageable']:
        check(manageable, 'id', str)
        check(manageable, 'name', str)


@pytest.mark.vcr()
def test_asset_lists_list_success(sc):
    asset_list = sc.asset_lists.list()
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


@pytest.mark.vcr()
def test_asset_lists_refresh_success(admin, asset_list):
    resp = admin.asset_lists.refresh(int(asset_list['id']), 1, 1)
    assert isinstance(resp, dict)
    check(resp, 'orgID', int)
    check(resp, 'repIDs', list)


@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'asset_list.xml'))
def test_asset_lists_import_definition_success(sc, datafiles):
    with open(os.path.join(str(datafiles), 'asset_list.xml'), 'rb') as fobj:
        sc.asset_lists.import_definition(fobj, name='name')


@pytest.mark.vcr()
def test_asset_lists_export_definition_success(sc, asset_list):
    with open('asset_list_export.xml', 'wb') as fobj:
        sc.asset_lists.export_definition(int(asset_list['id']), fobj)
    os.remove('asset_list_export.xml')


@pytest.mark.vcr()
def test_asset_lists_export_definition_success_no_file(sc):
    with open('1000007.xml', 'wb'):
        sc.asset_lists.export_definition(1000007)
    os.remove('1000007.xml')


@pytest.mark.skip(reason='No LDAP Service to query against')
@pytest.mark.vcr()
def test_asset_lists_ldap_query_success(sc):
    resp = sc.asset_lists.ldap_query(1, 'company.tld', '*')


@pytest.mark.vcr()
def test_asset_lists_tags_success(sc):
    tags = sc.asset_lists.tags()
    for tag in tags:
        single(tag, str)


@pytest.mark.vcr()
def test_asset_lists_share_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists.share('one')


@pytest.mark.vcr()
def test_asset_lists_share_group_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists.share(1, 'one')


@pytest.mark.vcr()
def test_asset_lists_share_success(sc, asset_list, group):
    asset = sc.asset_lists.share(int(asset_list['id']), int(group['id']))
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
