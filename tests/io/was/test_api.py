import pytest

from tenable.io import TenableIO
from tenable.io.was.iterator import WasIterator


@pytest.mark.vcr()
def test_was_export(api: TenableIO):
    """
    Basic test to ensure WasIterator is returned and values are returned when the iterator is traversed.
    """
    findings_iterator = api.was.export(
        and_filter=[
            ("scans_started_at", "gte", "2023/03/23"),
            ("scans_status", "contains", ["completed"])
        ]
    )

    findings = [finding for finding in findings_iterator]

    assert isinstance(findings_iterator, WasIterator)
    assert len(findings) > 0

@pytest.mark.vcr()
def test_ensure_iterator_does_not_break_on_no_data_found(api: TenableIO):
    """
    Test to ensure iterator doesn't break on no data found
    """
    findings_iterator = api.was.export(
        and_filter=[
            ("scans_started_at", "gte", "2100/03/23"),
            ("scans_status", "contains", ["completed"])
        ]
    )

    findings = [finding for finding in findings_iterator]

    assert isinstance(findings_iterator, WasIterator)
    assert len(findings) == 0
