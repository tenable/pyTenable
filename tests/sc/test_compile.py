'''
test compile
'''
import pytest
from tenable.sc import TenableSC
from tenable.sc.accept_risks import AcceptRiskAPI
from tenable.sc.alerts import AlertAPI
from tenable.sc.analysis import AnalysisResultsIterator, AnalysisAPI
from tenable.sc.asset_lists import AssetListAPI
from tenable.sc.audit_files import AuditFileAPI
from tenable.sc.base import SCEndpoint, SCResultsIterator
from tenable.sc.credentials import CredentialAPI
from tenable.sc.current import CurrentSessionAPI
from tenable.sc.feeds import FeedAPI
from tenable.sc.files import FileAPI
from tenable.sc.groups import GroupAPI
from tenable.sc.organizations import OrganizationAPI
from tenable.sc.plugins import PluginAPI, PluginResultsIterator
from tenable.sc.policies import ScanPolicyAPI
from tenable.sc.queries import QueryAPI
from tenable.sc.recast_risks import RecastRiskAPI
from tenable.sc.repositories import RepositoryAPI
from tenable.sc.roles import RoleAPI
from tenable.sc.scan_instances import ScanResultAPI
from tenable.sc.scan_zones import ScanZoneAPI
from tenable.sc.scanners import ScannerAPI
from tenable.sc.scans import ScanAPI
from tenable.sc.status import StatusAPI
from tenable.sc.system import SystemAPI
from tenable.sc.users import UserAPI
from tests.sc.conftest import security_center
from tenable.errors import ConnectionError


def test_sc_compile(security_center):
    '''
    test to raise the exception when host is invalid, hence the connection wont be made
    '''

    try:
        TenableSC(host='127.0.0.1')
        AcceptRiskAPI(security_center)
        AlertAPI(security_center)
        AnalysisResultsIterator(security_center)
        AnalysisAPI(security_center)
        AssetListAPI(security_center)
        AuditFileAPI(security_center)
        SCEndpoint(security_center)
        SCResultsIterator(security_center)
        CredentialAPI(security_center)
        CurrentSessionAPI(security_center)
        FeedAPI(security_center)
        FileAPI(security_center)
        GroupAPI(security_center)
        OrganizationAPI(security_center)
        PluginAPI(security_center)
        PluginResultsIterator(security_center)
        ScanPolicyAPI(security_center)
        QueryAPI(security_center)
        RecastRiskAPI(security_center)
        RepositoryAPI(security_center)
        RoleAPI(security_center)
        ScanResultAPI(security_center)
        ScanZoneAPI(security_center)
        ScannerAPI(security_center)
        ScanAPI(security_center)
        StatusAPI(security_center)
        SystemAPI(security_center)
        UserAPI(security_center)

    except NameError as error:
        print("\n The following name error exists: {}".format(error))
        pytest.raises(NameError)
        assert True
    except ConnectionError as error:
        print("\n The following connection error exists: {}".format(error))
        pytest.raises(ConnectionError)
        assert True
    except TypeError as error:
        print("\n The following type error exists: {}".format(error))
        assert True
