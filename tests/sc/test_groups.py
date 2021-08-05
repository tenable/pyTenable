'''
test file for testing various scenarios in security center groups
functionality
'''
import pytest

from ..checker import check


def test_groups_constructor_name_typeerror(security_center):
    '''
    test groups constructor name for type error
    '''
    with pytest.raises(TypeError):
        getattr(security_center.groups, '_constructor')(name=1)


def test_groups_constructor_description_typeerror(security_center):
    '''
    test groups constructor description for type error
    '''
    with pytest.raises(TypeError):
        getattr(security_center.groups, '_constructor')(description=1)


def test_groups_constructor_list_mapping_typeerror(security_center):
    '''
    test groups constructor 'list mapping' for type error
    '''
    items = ['viewable', 'repos', 'lce_ids', 'asset_lists', 'scan_policies',
             'query_ids', 'scan_creds', 'dashboards', 'report_cards', 'audit_files']
    for i in items:
        with pytest.raises(TypeError):
            getattr(security_center.groups, '_constructor')(**{i: 1})


def test_groups_constructor_list_item_mapping_typeerror(security_center):
    '''
    test groups constructor 'list item mapping' for type error
    '''
    items = ['viewable', 'repos', 'lce_ids', 'asset_lists', 'scan_policies',
             'query_ids', 'scan_creds', 'dashboards', 'report_cards', 'audit_files']
    for item in items:
        with pytest.raises(TypeError):
            getattr(security_center.groups, '_constructor')(**{item: ['one']})


def test_groups_constructor_success(security_center):
    '''
    test groups constructor for success
    '''
    group = getattr(security_center.groups, '_constructor')(
        name='Example',
        description='Stuff',
        viewable=[1, 2, 3],
        repos=[1],
        lce_ids=[1],
        asset_lists=[1, 2],
        scan_policies=[1],
        query_ids=[1],
        scan_creds=[1, 2, 3],
        dashboards=[1, 2],
        report_cards=[1],
        audit_files=[1, 2]
    )
    assert isinstance(group, dict)
    assert group == {
        'name': 'Example',
        'description': 'Stuff',
        'definingAssets': [{'id': 1}, {'id': 2}, {'id': 3}],
        'repositories': [{'id': 1}],
        'lces': [{'id': 1}],
        'assets': [{'id': 1}, {'id': 2}],
        'policies': [{'id': 1}],
        'queries': [{'id': 1}],
        'credentials': [{'id': 1}, {'id': 2}, {'id': 3}],
        'dashboardTabs': [{'id': 1}, {'id': 2}],
        'arcs': [{'id': 1}],
        'auditFiles': [{'id': 1}, {'id': 2}]
    }


@pytest.mark.vcr()
def test_groups_create_success(security_center, group):
    '''
    test groups create for success
    '''
    assert isinstance(group, dict)
    check(group, 'id', str)
    check(group, 'name', str)
    check(group, 'description', str)
    check(group, 'createdTime', str)
    check(group, 'modifiedTime', str)
    check(group, 'userCount', int)
    key_list = ['definingAssets', 'lces', 'repositories', 'assets', 'policies',
               'queries', 'credentials', 'dashboardTabs', 'arcs', 'auditFiles']
    for key in key_list:
        check(group, key, list)
        for group in group[key]:
            check(group, 'id', str)
            check(group, 'name', str)
            check(group, 'description', str)
            if key == 'lces':
                check(group, 'version', str)
            if key == 'repositories':
                check(group, 'lastVulnUpdate', str)
                check(group, 'type', str)
                check(group, 'dataFormat', str)


@pytest.mark.vcr()
def test_groups_edit_success(security_center, group):
    '''
    test groups edit for success
    '''
    group = security_center.groups.edit(int(group['id']), name='new name')
    assert isinstance(group, dict)
    check(group, 'id', str)
    check(group, 'name', str)
    check(group, 'description', str)
    check(group, 'createdTime', str)
    check(group, 'modifiedTime', str)
    check(group, 'userCount', int)
    key_list = ['definingAssets', 'lces', 'repositories', 'assets', 'policies',
               'queries', 'credentials', 'dashboardTabs', 'arcs', 'auditFiles']
    for key in key_list:
        check(group, key, list)
        for a_group in group[key]:
            check(a_group, 'id', str)
            check(a_group, 'name', str)
            check(a_group, 'description', str)
            if key == 'lces':
                check(a_group, 'version', str)
            if key == 'repositories':
                check(a_group, 'lastVulnUpdate', str)
                check(a_group, 'type', str)
                check(a_group, 'dataFormat', str)


@pytest.mark.vcr()
def test_groups_details_success_for_fields(security_center, group):
    '''
    test groups details success for fields
    '''
    group = security_center.groups.details(int(group['id']), fields=['id', 'name', 'description'])
    assert isinstance(group, dict)
    check(group, 'id', str)
    check(group, 'name', str)
    check(group, 'description', str)


@pytest.mark.vcr()
def test_groups_list_success_for_fields(security_center, group):
    '''
    test groups list success for fields
    '''
    groups = security_center.groups.list(fields=['id', 'name', 'description'])
    assert isinstance(groups, list)
    for group in groups:
        check(group, 'id', str)
        check(group, 'name', str)
        check(group, 'description', str)


@pytest.mark.vcr()
def test_groups_details_success(security_center, group):
    '''
    test groups details for success
    '''
    group_details = security_center.groups.details(int(group['id']))
    assert isinstance(group_details, dict)
    check(group_details, 'id', str)
    check(group_details, 'name', str)
    check(group_details, 'description', str)
    check(group_details, 'createdTime', str)
    check(group_details, 'modifiedTime', str)
    check(group_details, 'userCount', int)
    key_list = ['definingAssets', 'lces', 'repositories', 'assets', 'policies',
               'queries', 'credentials', 'dashboardTabs', 'arcs', 'auditFiles']
    for data in key_list:
        check(group_details, data, list)
        for info in group_details[data]:
            check(info, 'id', str)
            check(info, 'name', str)
            check(info, 'description', str)
            if data == 'lces':
                check(info, 'version', str)
            if data == 'repositories':
                check(info, 'lastVulnUpdate', str)
                check(info, 'type', str)
                check(info, 'dataFormat', str)


@pytest.mark.vcr()
def test_groups_delete_success(security_center, group):
    '''
    test groups delete for success
    '''
    security_center.groups.delete(int(group['id']))
