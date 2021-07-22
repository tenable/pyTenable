'''
test repositories
'''
import pytest
from tenable.cs.repositories import RepositoryIterator
from ..checker import check


@pytest.mark.vcr()
def test_repositories_list_contains_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.repositories.list(contains=1)


@pytest.mark.vcr()
def test_repositories_list_image_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.repositories.list(image=1)


@pytest.mark.vcr()
def test_repositories_list_limit_typerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.repositories.list(limit='onezeroone')


@pytest.mark.vcr()
def test_repositories_list_offset_typerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.repositories.list(offset='onezeroone')


@pytest.mark.vcr()
def test_repositories_list_pages_typerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.repositories.list(pages='onezeroone')


@pytest.mark.vcr()
def test_repositories_list_with_data(api):
    '''test to get the list of repositories list with the data'''
    repos = api.repositories.list()
    assert isinstance(repos, RepositoryIterator)
    repo = repos.next()
    assert isinstance(repo, dict)
    check(repo, 'name', str)
    check(repo, 'imagesCount', int)
    check(repo, 'labelsCount', int)
    check(repo, 'vulnerabilitiesCount', int)
    check(repo, 'malwareCount', int)
    check(repo, 'pullCount', int)
    check(repo, 'pushCount', int)
    check(repo, 'totalBytes', int)


@pytest.mark.vcr()
def test_repositories_details_name_typerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.repositories.details(1)


@pytest.mark.vcr()
def test_repositories_details_success(api):
    '''test to get the details of the repositories'''
    repos = api.repositories.list()
    repo = repos.next()
    repo_details = api.repositories.details(repo['name'])
    assert isinstance(repo_details, dict)
    check(repo_details, 'name', str)
    check(repo_details, 'imagesCount', int)
    check(repo_details, 'labelsCount', int)
    check(repo_details, 'vulnerabilitiesCount', int)
    check(repo_details, 'malwareCount', int)
    check(repo_details, 'pullCount', int)
    check(repo_details, 'pushCount', int)
    check(repo_details, 'totalBytes', int)


@pytest.mark.vcr()
def test_repositories_delete_name_typeerror(api):
    '''test to raise the exception when the parameter passed is not as the expected type'''
    with pytest.raises(TypeError):
        api.repositories.delete(1)


@pytest.mark.vcr()
@pytest.mark.skip('We don\'t want to actually delete a repository')
def test_repositories_delete(api):
    '''test to delete the repositories'''
    repos = api.repositories.list()
    repo = repos.next()
    api.repositories.delete(repo['name'])
