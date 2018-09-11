from .fixtures import *
from tenable.errors import *

def test_list(api):
    assert isinstance(api.containers.list(), list)
    ## Validate output here....

def test_inventory_id_typeerror(api):
    with pytest.raises(TypeError):
        api.containers.inventory(True)

def test_inventory(api, image_id):
    assert isinstance(api.containers.inventory(image_id), dict)
    ## Validate output here....