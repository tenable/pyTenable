import pytest
from tenable.nessus.schema.scans import ScanExportSchema


def test_scan_export_echema():
    schema = ScanExportSchema()
    l = schema.load({'format': 'db',
                     'password': 'abc',
                     'template_id': 1
                     })
    assert schema.dump(l) == {'format': 'db',
                              'password': 'abc',
                              'template_id': 1
                              }
    assert schema.dump(schema.load({})) == {'format': 'nessus'}
