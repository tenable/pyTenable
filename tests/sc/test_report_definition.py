'''
test file to test various scenarios in sc report_definition
'''
import pytest
from ..checker import check, single

def test_report_definition_id_typeerror(sc):
    with pytest.raises(TypeError):
        sc.report_definition.launch(id='one')

def test_report_definition_id_item_typeerror(sc):
    with pytest.raises(TypeError):
        sc.report_definition.launch(id=['one'])

