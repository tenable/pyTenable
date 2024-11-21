'''
test file to test various scenarios in sc report_definition
'''
import pytest
from ..checker import check, single

def test_report_definition_id_typeerror(security_center):
    with pytest.raises(TypeError):
        security_center.report_definition.launch(id='one')

def test_report_definition_id_item_typeerror(security_center):
    with pytest.raises(TypeError):
        security_center.report_definition.launch(id=['one'])

