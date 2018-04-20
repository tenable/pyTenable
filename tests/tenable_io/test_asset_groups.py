from .fixtures import *
from tenable.errors import *

@pytest.fixture
def assetgroup(request, api):
    group = api.asset_groups.create(str(uuid.uuid4()), ['192.168.0.1'])
    def teardown():
        try:
            api.asset_groups.delete(group['id'])
        except NotFoundError:
            pass
    request.addfinalizer(teardown)
    return group

def test_create_name_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.create(False, [])

def test_create_type_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.create('nope', [], type=1)

def test_create_type_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.asset_groups.create('nope', [], type='nope')

def test_create_acls_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.create('nope', [], acls='nope')

def test_create_members_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.asset_groups.create('nope', [])

def test_create(api, assetgroup):
    pass

def test_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.delete('nope')

def test_delete(api, assetgroup):
    pass

def test_details_id_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.details('nope')

def test_details(api, assetgroup):
    group = api.asset_groups.details(assetgroup['id'])
    assert isinstance(group, dict)
    assert group['id'] == assetgroup['id']

def test_edit_id_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.delete('nope')

def test_edit_name_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.edit(1, 1)

def test_edit_acls_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.edit(1, acls=False)

def test_edit_type_typeerror(api):
    with pytest.raises(TypeError):
        api.asset_groups.edit(1, type=False)

def test_edit_type_unexpectedvalue(api):
    with pytest.raises(UnexpectedValueError):
        api.asset_groups.edit(1, type='nope')

def test_edit(api, assetgroup):
    members = assetgroup['members'].split(',')
    members.append('192.168.0.2')
    mod = api.asset_groups.edit(assetgroup['id'], members=members)
    assert mod['members'] == ', '.join(members)

def test_list(api):
    assert isinstance(api.asset_groups.list(), list)