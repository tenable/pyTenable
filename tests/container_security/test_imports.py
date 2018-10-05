from .fixtures import *
from tenable.errors import *
from uuid import UUID

def test_list(api, import_id):
    resp = api.imports.list()
    assert isinstance(resp, dict)
    ## Output validation here....

def test_test_id_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.test(1)

def test_test_id_typeerror(api):
    with pytest.raises(UnexpectedValueError):
        api.imports.test('nothing')

@pytest.mark.skip(reason="The documentation is broken for this call.")
def test_test(api, import_id):
    resp = api.imports.test(import_id)
    assert isinstance(resp, dict)
    check(resp, 'status', str)
    check(resp, 'id', 'uuid')

def test_create_host_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host=1,
            port=443,
            username='someone',
            password='secret_squirrel',
            provider='dr',
        )

def test_create_port_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port='something',
            username='someone',
            password='secret_squirrel',
            provider='dr',
        )

def test_create_username_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username=1,
            password='secret_squirrel',
            provider='dr',
        )

def test_create_password_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password=1,
            provider='dr',
        )

def test_create_provider_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            provider=1,
        )

def test_create_provider_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            provider='jfrog',
        )

def test_create_ssl_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.create(
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            provider='dr',
            ssl='yes'
        )

def test_create(api):
    resp = api.imports.create(
        host='registry.hub.docker.com',
        port=443,
        username='someone',
        password='secret_squirrel',
        provider='dr',
    )
    assert isinstance(resp, dict)
    check(resp, 'status', str)
    check(resp, 'id', 'uuid')

def test_update_host_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host=1,
            port=443,
            username='someone',
            password='secret_squirrel',
            provider='dr',
        )

def test_update_port_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port='something',
            username='someone',
            password='secret_squirrel',
            provider='dr',
        )

def test_update_username_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username=1,
            password='secret_squirrel',
            provider='dr',
        )

def test_update_password_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password=1,
            provider='dr',
        )

def test_update_provider_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            provider=1,
        )

def test_update_provider_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            provider='jfrog',
        )

def test_update_ssl_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.update(0,
            host='registry.hub.docker.com',
            port=443,
            username='someone',
            password='secret_squirrel',
            provider='dr',
            ssl='yes'
        )

def test_update(api, import_id):
    resp = api.imports.update(import_id,
        host='registry.hub.docker.com',
        port=443,
        username='someone',
        password='secret_squirrel',
        provider='dr',
    )
    assert isinstance(resp, dict)
    check(resp, 'status', str)
    check(resp, 'id', 'uuid')

def test_delete_id_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.delete(1)

def test_delete_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.imports.delete('no')

def test_delete(api, import_id):
    api.imports.delete(import_id)

def test_run_id_typeerror(api):
    with pytest.raises(TypeError):
        api.imports.run(123)

def test_run_id_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.imports.run('nothing')

def test_run(api, import_id):
    resp = api.imports.run(import_id)
    assert isinstance(resp, dict)
    check(resp, 'status', str)
    check(resp, 'id', 'uuid')