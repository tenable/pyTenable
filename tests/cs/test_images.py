from tenable.errors import *
from ..checker import check, single
from tenable.cs.images import ImageIterator
import pytest

@pytest.mark.vcr()
def test_images_list_has_malware_typeerror(api):
    with pytest.raises(TypeError):
        api.images.list(has_malware='nope')

@pytest.mark.vcr()
def test_images_list_image_id_typeerror(api):
    with pytest.raises(TypeError):
        api.images.list(image_id=1)

@pytest.mark.vcr()
def test_images_list_name_typerror(api):
    with pytest.raises(TypeError):
        api.images.list(name=1)

@pytest.mark.vcr()
def test_images_list_limit_typeerror(api):
    with pytest.raises(TypeError):
        api.images.list(limit='zero')

@pytest.mark.vcr()
def test_images_list_offset_typerror(api):
    with pytest.raises(TypeError):
        api.images.list(offset='zero')

@pytest.mark.vcr()
def test_images_list_os_typeerror(api):
    with pytest.raises(TypeError):
        api.images.list(os=1)

@pytest.mark.vcr()
def test_images_list_repository_typeerror(api):
    with pytest.raises(TypeError):
        api.images.list(repository=1)

@pytest.mark.vcr()
def test_images_list_score_operator_typerror(api):
    with pytest.raises(TypeError):
        api.images.list(score_operator=1)

@pytest.mark.vcr()
def test_images_list_score_operator_unexpectedvalueerror(api):
    with pytest.raises(UnexpectedValueError):
        api.images.list(score_operator='nope')

@pytest.mark.vcr()
def test_images_list_score_value_typerror(api):
    with pytest.raises(TypeError):
        api.images.list(score_value='zero')

@pytest.mark.vcr()
def test_images_list_tag_typeerror(api):
    with pytest.raises(TypeError):
        api.images.list(tag=1)

@pytest.mark.vcr()
def test_images_list_success(api):
    images = api.images.list()
    assert isinstance(images, ImageIterator)
    i = images.next()
    check(i, 'repoId', str)
    check(i, 'repoName', str)
    check(i, 'name', str)
    check(i, 'tag', str)
    check(i, 'digest', str)
    check(i, 'hasReport', bool)
    check(i, 'hasInventory', bool)
    check(i, 'status', str)
    check(i, 'lastJobStatus', str)
    check(i, 'pullCount', str)
    check(i, 'pushCount', str)
    check(i, 'source', str)
    check(i, 'createdAt', 'datetime')
    check(i, 'updatedAt', 'datetime')
    check(i, 'finishedAt', 'datetime')
    check(i, 'imageHash', str)
    check(i, 'size', str)
    check(i, 'layers', list)
    for l in i['layers']:
        check(l, 'size', int)
        check(l, 'digest', str)
    check(i, 'os', str)
    check(i, 'osVersion', str)

@pytest.mark.vcr()
def test_images_details_repository_typeerror(api):
    with pytest.raises(TypeError):
        api.images.details(1, 'no', 'no')

@pytest.mark.vcr()
def test_images_details_image_typeerror(api):
    with pytest.raises(TypeError):
        api.images.details('no', 1, 'no')

@pytest.mark.vcr()
def test_images_details_tag_typeerror(api):
    with pytest.raises(TypeError):
        api.images.details('no', 'no', 1)

@pytest.mark.vcr()
def test_images_details_success(api):
    i = api.images.details('library', 'alpine', '3.1')
    assert isinstance(i, dict)
    check(i, 'repository', str)
    check(i, 'name', str)
    check(i, 'tag', str)
    check(i, 'digest', str)
    check(i, 'status', str)
    check(i, 'riskScore', int)
    check(i, 'numberOfVulns', int)
    check(i, 'numberOfMalware', int)
    check(i, 'uploadedAt', 'datetime')
    check(i, 'lastScanned', 'datetime')
    check(i, 'size', str)
    check(i, 'layers', list)
    for l in i['layers']:
        check(l, 'size', int)
        check(l, 'digest', str)
    check(i, 'reportUrl', str)

@pytest.mark.vcr()
def test_images_delete_repository_typeerror(api):
    with pytest.raises(TypeError):
        api.images.details(1, 'no', 'no')

@pytest.mark.vcr()
def test_images_delete_image_typeerror(api):
    with pytest.raises(TypeError):
        api.images.details('no', 1, 'no')

@pytest.mark.vcr()
def test_images_delete_tag_typeerror(api):
    with pytest.raises(TypeError):
        api.images.details('no', 'no', 1)

@pytest.mark.vcr()
@pytest.mark.skip('We don\'t want to actually delete the image')
def test_images_delete_success(api):
    api.images.delete('library', 'alpine', '3.1')