from tenable.io.v3.was.scans.schema import ScanReportSchema, ScanStatusSchema


def test_scan_status_schema():
    '''
    Tests ScanStatusSchema
    '''
    schema = ScanStatusSchema()
    payload = {
        'requested_action': 'stop'
    }
    assert payload == schema.dump(schema.load(payload))


def test_scan_report_schema():
    '''
    Tests ScanReportSchema
    '''
    schema = ScanReportSchema()
    payload = {
        'content_type': 'text/csv'
    }
    assert payload == schema.dump(schema.load(payload))
