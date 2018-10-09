from .fixtures import *
from tenable.errors import *

def test_list(api):
    l = api.containers.list()
    assert isinstance(l, list)
    for i in l:
        check(i, 'size', str)
        check(i, 'status', str)
        check(i, 'repo_id', str)
        check(i, 'name', str)
        check(i, 'created_at', 'datetime')
        check(i, 'updated_at', 'datetime')
        check(i, 'platform', str)
        check(i, 'score', str)
        check(i, 'number_of_vulnerabilities', str)
        check(i, 'id', str)
        check(i, 'digest', str)
        check(i, 'repo_name', str)


def test_inventory_id_typeerror(api):
    with pytest.raises(TypeError):
        api.containers.inventory(True)

@pytest.mark.skip(reason='Doesn\'t seem to work.')
def test_inventory(api, image_id):
    assert isinstance(api.containers.inventory(image_id), dict)
    ## Validate output here....