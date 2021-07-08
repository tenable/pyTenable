'''
test uploads
'''
import pytest
from ..checker import single


def test_uploads_docker_push_name_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.uploads.docker_push(1)


def test_uploads_docker_push_tag_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.uploads.docker_push('example', tag=1)


def test_uploads_docker_push_cs_name_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.uploads.docker_push('example', tag='latest', cs_name=1)


def test_uploads_docker_push_cs_tag_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.uploads.docker_push('example', tag='latest', cs_tag=1)


@pytest.mark.skip(reason="Can't VCR because of docker.")
def test_uploads_docker_push(image_id):
    '''test to check the type of image_id'''
    single(image_id, str)
