from tenable.errors import *
from ..checker import check
import pytest, os

def test_asset_lists_dynamic_rules_constructor_passthrough(sc):
    a = {'test': 'value'}
    assert a == sc.asset_lists._dynamic_rules_constructor(a)

def test_asset_lists_dynamic_rules_constructor_typerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._dynamic_rules_constructor(1)

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

def test_asset_lists_constructor_data_fields_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(data_fields=1)

def test_asset_lists_constructor_combinations_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(combinations=1)

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
        sc.asset_lists._constructor(ips=[1,])

def test_asset_lists_constructor_filters_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filters=1)

def test_asset_lists_constructor_filters_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.asset_lists._constructor(filters=[1,])

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
        ips=['192.168.0.1',],
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
def assetlist(request, sc, vcr):
    with vcr.use_cassette('test_asset_lists_create_success'):
        a = sc.asset_lists.create('Example', 'static', ips=['192.168.0.1',])
    def teardown():
        try:
            with vcr.use_cassette('test_asset_lists_delete_success'):
                sc.asset_lists.delete(int(a['id']))
        except APIError:
            pass
    request.addfinalizer(teardown)
    return a

@pytest.mark.vcr()
def test_asset_lists_create_success(sc, assetlist):
    assert isinstance(assetlist, dict)
    check(assetlist, 'id', str)
    check(assetlist, 'name', str)
    check(assetlist, 'type', str)
    check(assetlist, 'description', str)
    check(assetlist, 'tags', str)
    check(assetlist, 'context', str)
    check(assetlist, 'status', str)
    check(assetlist, 'createdTime', str)
    check(assetlist, 'modifiedTime', str)
    check(assetlist, 'typeFields', dict)
    for key in assetlist['typeFields']:
        check(assetlist['typeFields'], key, str)
    check(assetlist, 'ipCount', int)
    check(assetlist, 'repositories', list)
    for i in assetlist['repositories']:
        check(i, 'ipCount', str)
        check(i, 'repository', dict)
        check(i['repository'], 'id', str)
        check(i['repository'], 'name', str)
        check(i['repository'], 'description', str)
    check(assetlist, 'assetDataFields', list)
    check(assetlist, 'groups', list)
    check(assetlist, 'canUse', str)
    check(assetlist, 'canManage', str)
    check(assetlist, 'creator', dict)
    check(assetlist['creator'], 'id', str)
    check(assetlist['creator'], 'firstname', str)
    check(assetlist['creator'], 'lastname', str)
    check(assetlist['creator'], 'username', str)
    check(assetlist, 'owner', dict)
    check(assetlist['owner'], 'id', str)
    check(assetlist['owner'], 'firstname', str)
    check(assetlist['owner'], 'lastname', str)
    check(assetlist['owner'], 'username', str)
    check(assetlist, 'ownerGroup', dict)
    check(assetlist['ownerGroup'], 'id', str)
    check(assetlist['ownerGroup'], 'name', str)
    check(assetlist['ownerGroup'], 'description', str)

@pytest.mark.vcr()
def test_asset_lists_delete_success(sc, assetlist):
    sc.asset_lists.delete(int(assetlist['id']))

@pytest.mark.vcr()
def test_asset_lists_details_success(sc, assetlist):
    a = sc.asset_lists.details(int(assetlist['id']))
    assert isinstance(a, dict)
    check(a, 'id', str)
    check(a, 'name', str)
    check(a, 'type', str)
    check(a, 'description', str)
    check(a, 'tags', str)
    check(a, 'context', str)
    check(a, 'status', str)
    check(a, 'createdTime', str)
    check(a, 'modifiedTime', str)
    check(a, 'typeFields', dict)
    for key in a['typeFields']:
        check(a['typeFields'], key, str)
    check(a, 'ipCount', int)
    check(a, 'repositories', list)
    for i in a['repositories']:
        check(i, 'ipCount', str)
        check(i, 'repository', dict)
        check(i['repository'], 'id', str)
        check(i['repository'], 'name', str)
        check(i['repository'], 'description', str)
    check(a, 'assetDataFields', list)
    check(a, 'groups', list)
    check(a, 'canUse', str)
    check(a, 'canManage', str)
    check(a, 'creator', dict)
    check(a['creator'], 'id', str)
    check(a['creator'], 'firstname', str)
    check(a['creator'], 'lastname', str)
    check(a['creator'], 'username', str)
    check(a, 'owner', dict)
    check(a['owner'], 'id', str)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'lastname', str)
    check(a['owner'], 'username', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a['ownerGroup'], 'description', str)

@pytest.mark.vcr()
def test_asset_lists_edit_success(sc, assetlist):
    a = sc.asset_lists.edit(int(assetlist['id']), name='Updated')
    assert isinstance(a, dict)
    check(a, 'id', str)
    check(a, 'name', str)
    check(a, 'type', str)
    check(a, 'description', str)
    check(a, 'tags', str)
    check(a, 'context', str)
    check(a, 'status', str)
    check(a, 'createdTime', str)
    check(a, 'modifiedTime', str)
    check(a, 'typeFields', dict)
    for key in a['typeFields']:
        check(a['typeFields'], key, str)
    check(a, 'ipCount', int)
    check(a, 'repositories', list)
    for i in a['repositories']:
        check(i, 'ipCount', str)
        check(i, 'repository', dict)
        check(i['repository'], 'id', str)
        check(i['repository'], 'name', str)
        check(i['repository'], 'description', str)
    check(a, 'assetDataFields', list)
    check(a, 'groups', list)
    check(a, 'canUse', str)
    check(a, 'canManage', str)
    check(a, 'creator', dict)
    check(a['creator'], 'id', str)
    check(a['creator'], 'firstname', str)
    check(a['creator'], 'lastname', str)
    check(a['creator'], 'username', str)
    check(a, 'owner', dict)
    check(a['owner'], 'id', str)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'lastname', str)
    check(a['owner'], 'username', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a['ownerGroup'], 'description', str)

@pytest.mark.vcr()
def test_asset_lists_list_success(sc, assetlist):
    alist = sc.asset_lists.list()
    assert isinstance(alist, dict)
    check(alist, 'usable', list)
    for i in alist['usable']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
        check(i, 'status', str)
    check(alist, 'manageable', list)
    for i in alist['manageable']:
        check(i, 'id', str)
        check(i, 'name', str)
        check(i, 'description', str)
        check(i, 'status', str)

@pytest.mark.vcr()
def test_asset_lists_refresh_success(admin, assetlist):
    resp = admin.asset_lists.refresh(int(assetlist['id']), 1, 1)
    assert isinstance(resp, dict)
    check(resp, 'orgID', int)
    check(resp, 'repIDs', list)


@pytest.mark.vcr()
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'asset_list.xml'))
def test_asset_lists_import_definition_success(sc, assetlist, datafiles):
    with open(os.path.join(str(datafiles), 'asset_list.xml'), 'rb') as fobj:
        sc.asset_lists.import_definition(fobj)

@pytest.mark.vcr()
def test_asset_lists_export_definition_success(sc, assetlist):
    with open('asset_list_export.xml', 'wb') as fobj:
        sc.asset_lists.export_definition(int(assetlist['id']), fobj)
    os.remove('asset_list_export.xml')

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
def test_asset_lists_share_success(sc, assetlist, group):
    a = sc.asset_lists.share(int(assetlist['id']), int(group['id']))
    assert isinstance(a, dict)
    check(a, 'id', str)
    check(a, 'name', str)
    check(a, 'type', str)
    check(a, 'description', str)
    check(a, 'tags', str)
    check(a, 'context', str)
    check(a, 'status', str)
    check(a, 'createdTime', str)
    check(a, 'modifiedTime', str)
    check(a, 'typeFields', dict)
    for key in a['typeFields']:
        check(a['typeFields'], key, str)
    check(a, 'ipCount', int)
    check(a, 'repositories', list)
    for i in a['repositories']:
        check(i, 'ipCount', str)
        check(i, 'repository', dict)
        check(i['repository'], 'id', str)
        check(i['repository'], 'name', str)
        check(i['repository'], 'description', str)
    check(a, 'assetDataFields', list)
    check(a, 'groups', list)
    check(a, 'canUse', str)
    check(a, 'canManage', str)
    check(a, 'creator', dict)
    check(a['creator'], 'id', str)
    check(a['creator'], 'firstname', str)
    check(a['creator'], 'lastname', str)
    check(a['creator'], 'username', str)
    check(a, 'owner', dict)
    check(a['owner'], 'id', str)
    check(a['owner'], 'firstname', str)
    check(a['owner'], 'lastname', str)
    check(a['owner'], 'username', str)
    check(a, 'ownerGroup', dict)
    check(a['ownerGroup'], 'id', str)
    check(a['ownerGroup'], 'name', str)
    check(a['ownerGroup'], 'description', str)