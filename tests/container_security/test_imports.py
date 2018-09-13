from .fixtures import *
from tenable.errors import *
from uuid import UUID

def test_list(api, import_id):
    resp = api.imports.list()
    assert isinstance(resp, list)
    ## Output validation here....

def test_test_id_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.test('nothing')

def test_test(api, import_id):
    resp = api.imports.test(import_id)
    assert isinstance(resp, dict)
    assert 'status' in resp
    assert 'id' in resp
    assert isinstance(resp['status'], str)
    assert isinstance(resp['id'], str)
    assert UUID(resp['id'])

def test_create_host_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host=1,
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='dr',
        )

def test_create_port_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port='something',
            username='someone',
            password='secret_squirrel',
            privider='dr',
        )

def test_create_username_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username=1,
            password='secret_squirrel',
            privider='dr',
        )

def test_create_password_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password=1,
            privider='dr',
        )

def test_create_provider_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider=1,
        )

def test_create_provider_invalidinput(api):
    with pytest.raises(InvalidInput):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='jfrog',
        )

def test_create_ssl_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='dr',
            ssl='yes'
        )

def test_create_active_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='dr',
            active='yes'
        )

def test_create(api):
    resp = api.imports.create(
        host='registry.hub.docker.com',
        port=443,
        username='someone',
        password='secret_squirrel',
        privider='dr',
    )
    assert isinstance(resp, dict)
    assert 'status' in resp
    assert 'id' in resp
    assert isinstance(resp['status'], str)
    assert isinstance(resp['id'], str)
    assert UUID(resp['id'])

def test_update_host_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host=1,
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='dr',
        )

def test_update_port_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port='something',
            username='someone',
            password='secret_squirrel',
            privider='dr',
        )

def test_update_username_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username=1,
            password='secret_squirrel',
            privider='dr',
        )

def test_update_password_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password=1,
            privider='dr',
        )

def test_update_provider_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider=1,
        )

def test_update_provider_invalidinput(api):
    with pytest.raises(InvalidInput):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='jfrog',
        )

def test_update_ssl_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='dr',
            ssl='yes'
        )

def test_update_active_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            privider='dr',
            active='yes'
        )

def test_create(api, import_id):
    resp = api.imports.create(import_id,
        host='registry.hub.docker.com',
        port=443,
        username='someone',
        password='secret_squirrel',
        privider='dr',
    )
    assert isinstance(resp, dict)
    assert 'status' in resp
    assert 'id' in resp
    assert isinstance(resp['status'], str)
    assert isinstance(resp['id'], str)
    assert UUID(resp['id'])

def test_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.delete('no')

def test_delete(api, import_id):
    api.imports.delete(import_id)

def test_run_id_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.run('nothing')

def test_run(api, import_id):
    resp = api.imports.run(import_id)
    assert isinstance(resp, dict)
    assert 'status' in resp
    assert 'id' in resp
    assert isinstance(resp['status'], str)
    assert isinstance(resp['id'], str)
    assert UUID(resp['id'])