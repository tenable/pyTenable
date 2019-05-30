from tenable.errors import *
from ..checker import check, single
from tenable.cs.repositories import RepositoryIterator
import pytest

@pytest.mark.vcr()
def test_repositories_list_contains_typeerror(api):
    with pytest.raises(TypeError):
        api.repositories.list(contains=1)

@pytest.mark.vcr()
def test_repositories_list_image_typeerror(api):
    with pytest.raises(TypeError):
        api.repositories.list(image=1)

@pytest.mark.vcr()
def test_repositories_list_limit_typerror(api):
    with pytest.raises(TypeError):
        api.repositories.list(limit='onezeroone')

@pytest.mark.vcr()
def test_repositories_list_offset_typerror(api):
    with pytest.raises(TypeError):
        api.repositories.list(offset='onezeroone')

@pytest.mark.vcr()
def test_repositories_list_pages_typerror(api):
    with pytest.raises(TypeError):
        api.repositories.list(pages='onezeroone')

@pytest.mark.vcr()
def test_repositories_list_with_data(api):
    repos = api.repositories.list()
    assert isinstance(repos, RepositoryIterator)
    r = repos.next()
    assert isinstance(r, dict)
    check(r, 'name', str)
    check(r, 'imagesCount', int)
    check(r, 'labelsCount', int)
    check(r, 'vulnerabilitiesCount', int)
    check(r, 'malwareCount', int)
    check(r, 'pullCount', int)
    check(r, 'pushCount', int)
    check(r, 'totalBytes', int)

@pytest.mark.vcr()
def test_repositories_details_name_typerror(api):
    with pytest.raises(TypeError):
        api.repositories.details(1)

@pytest.mark.vcr()
def test_repositories_details_success(api):
    repos = api.repositories.list()
    i = repos.next()
    r = api.repositories.details(i['name'])
    assert isinstance(r, dict)
    check(r, 'name', str)
    check(r, 'imagesCount', int)
    check(r, 'labelsCount', int)
    check(r, 'vulnerabilitiesCount', int)
    check(r, 'malwareCount', int)
    check(r, 'pullCount', int)
    check(r, 'pushCount', int)
    check(r, 'totalBytes', int)

@pytest.mark.vcr()
def test_repositories_delete_name_typeerror(api):
    with pytest.raises(TypeError):
        api.repositories.delete(1)

@pytest.mark.vcr()
@pytest.mark.skip('We don\'t want to actually delete a repository')
def test_repositories_delete(api):
    repos = api.repositories.list()
    r = repos.next()
    api.repositories.delete(r['name'])