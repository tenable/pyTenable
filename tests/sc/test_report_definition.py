'''
test file to test various scenarios in sc report_definition
'''
import pytest
from ..checker import check

def test_report_definition_id_typeerror(security_center):
    '''
    validate id is int not string
    '''
    with pytest.raises(TypeError):
        security_center.report_definition.launch(id='one')

def test_report_definition_id_item_typeerror(security_center):
    '''
    validate id is int not list
    '''
    
    with pytest.raises(TypeError):
        security_center.report_definition.launch(id=['one'])

@pytest.mark.vcr()
def test_report_definition_launch_success(security_center):
    '''
    validate launch is successful and returns running report ID
    '''
    report = security_center.report_definition.launch(id=1)
    assert isinstance(report, dict)
    check(report['reportResult'], 'id', str)
    check(report['reportResult'], 'name', str)
    check(report['reportResult'], 'status', str)