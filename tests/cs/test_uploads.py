from tenable.errors import *
from ..checker import check, single
import pytest

def test_uploads_docker_push_name_typeerror(api):
    with pytest.raises(TypeError):
        api.uploads.docker_push(1)

def test_uploads_docker_push_tag_typeerror(api):
    with pytest.raises(TypeError):
        api.uploads.docker_push('example', tag=1)

def test_uploads_docker_push_cs_name_typeerror(api):
    with pytest.raises(TypeError):
        api.uploads.docker_push('example', tag='latest', cs_name=1)

def test_uploads_docker_push_cs_tag_typeerror(api):
    with pytest.raises(TypeError):
        api.uploads.docker_push('example', tag='latest', cs_tag=1)

@pytest.mark.skip(reason="Can't VCR because of docker.")
def test_uploads_docker_push(api, image_id):
    single(image_id, str)