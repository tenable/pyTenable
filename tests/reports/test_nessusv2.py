from tenable.reports.nessusv2 import NessusReportv2
from .fixtures import *
import datetime, sys

@pytest.mark.skipif(sys.version_info < (3,4),
                    reason="requires python3.4 or higher")
@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 
    'test_files', 
    'example.nessus'
))
def test_nessus_report_typeerror(datafiles):
    with open(os.path.join(str(datafiles), 'example.nessus')) as nobj:
        with pytest.raises(TypeError):
            for items in NessusReportv2(nobj):
                pass

@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 
    'test_files', 
    'example.nessus'
))
def test_nessus_report(datafiles):
    with open(os.path.join(str(datafiles), 'example.nessus'), 'rb') as nobj:
        for item in NessusReportv2(nobj):
            check(item, 'description', str)
            check(item, 'HOST_START', datetime.datetime)
            check(item, 'HOST_END', datetime.datetime)
            check(item, 'host-report-name', str)
            check(item, 'pluginFamily', str)
            check(item, 'pluginID', int)
            check(item, 'pluginName', str)
            check(item, 'plugin_modification_date', datetime.datetime)
            check(item, 'plugin_publication_date', datetime.datetime)
            check(item, 'plugin_type', str)
            check(item, 'protocol', str)
            check(item, 'port', int)
            check(item, 'risk_factor', str)
            check(item, 'severity', int)
            check(item, 'solution', str)
            check(item, 'synopsis', str)