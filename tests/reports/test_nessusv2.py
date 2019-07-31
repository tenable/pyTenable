from tenable.reports.nessusv2 import NessusReportv2
from ..checker import check
import datetime, sys, pytest, os

@pytest.mark.datafiles(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', 'test_files', 'example.nessus'))
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