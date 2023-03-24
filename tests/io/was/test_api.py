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
