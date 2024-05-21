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


def test_exception_raised_on_wrong_filters__single_with_and_filter(api: TenableIO):
    """
    Test to ensure exception is raised when user attempts to pass `and_filter` with `single_filter`
    """
    with pytest.raises(AttributeError):
        findings_iterator = api.was.export(
            single_filter=("scans_started_at", "gte", "2100/03/23"),
            and_filter=[
                ("scans_started_at", "gte", "2023/03/23"),
                ("scans_status", "contains", ["completed"])
            ]
        )


def test_exception_raised_on_wrong_filters__single_with_or_filter(api: TenableIO):
    """
    Test to ensure exception is raised when user attempts to pass `or_filter` with `single_filter`
    """
    with pytest.raises(AttributeError):
        findings_iterator = api.was.export(
            single_filter=("scans_started_at", "gte", "2100/03/23"),
            or_filter=[
                ("scans_started_at", "gte", "2023/03/23"),
                ("scans_status", "contains", ["completed"])
            ]
        )
