from .fixtures import *
from tenable.errors import *

def test_status_id_typeerror(api):
    with pytest.raises(TypeError):
        api.compliance.status(id=1)

def test_status_name_typeerror(api):
    with pytest.raises(TypeError):
        api.compliance.status(name=1)

def test_status_repo_typeerror(api):
    with pytest.raises(TypeError):
        api.compliance.status(name='nginx', repo=1)

def test_status_tag_typeerror(api):
    with pytest.raises(TypeError):
        api.compliance.status(name='nginx', repo='library', tag=1)

def test_status(api, image_id):
    s = api.compliance.status(id=image_id)
    assert isinstance(s, dict)
    # Need to validate output here....