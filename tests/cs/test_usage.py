'''
test usage
'''
import pytest
from ..checker import check, single


@pytest.mark.vcr()
def test_usage_stats(api):
    '''test to get the usage statistics for container security'''
    stats = api.usage.stats()
    assert isinstance(stats, dict)
    check(stats, 'id', int)
    check(stats, 'repositoryCount', int)
    check(stats, 'pushCount', int)
    check(stats, 'pullCount', int)
    check(stats, 'imagesCount', int)
    check(stats, 'policiesCount', int)
    check(stats, 'osCount', dict)
    for key in stats['osCount'].keys():
        single(stats['osCount'][key], int)
    check(stats, 'imagesSummary', dict)
    check(stats['imagesSummary'], 'total', int)
    check(stats['imagesSummary'], 'latest', int)
    check(stats['imagesSummary'], 'highRisk', int)
    check(stats, 'runningContainers', dict)
    check(stats['runningContainers'], 'total', int)
    check(stats['runningContainers'], 'unscanned', int)
    check(stats['runningContainers'], 'highRisk', int)
