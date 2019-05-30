from tenable.errors import *
from ..checker import check, single
import pytest

@pytest.mark.vcr()
def test_usage_stats(api):
    s = api.usage.stats()
    assert isinstance(s, dict)
    check(s, 'id', int)
    check(s, 'repositoryCount', int)
    check(s, 'pushCount', int)
    check(s, 'pullCount', int)
    check(s, 'imagesCount', int)
    check(s, 'policiesCount', int)
    check(s, 'osCount', dict)
    for k in s['osCount'].keys():
        single(s['osCount'][k], int)
    check(s, 'imagesSummary', dict)
    check(s['imagesSummary'], 'total', int)
    check(s['imagesSummary'], 'latest', int)
    check(s['imagesSummary'], 'highRisk', int)
    check(s, 'runningContainers', dict)
    check(s['runningContainers'], 'total', int)
    check(s['runningContainers'], 'unscanned', int)
    check(s['runningContainers'], 'highRisk', int)