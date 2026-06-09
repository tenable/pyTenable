import logging
from uuid import UUID

from tenable.utils import scrub


def test_scrub_string():
    assert 'test' == scrub('test')


def test_scrub_int():
    assert '1' == scrub(1)


def test_scrub_uuid():
    assert '12345678-1234-1234-1234-123456789012' == scrub(
        UUID('12345678-1234-1234-1234-123456789012')
    )


def test_scrub_remove_path_traversal():
    assert 'test' == scrub('../test')


def test_scrub_scan_id_formats():
    formats = [
        12345,
        '44346bcb-4afc-4db0-b283-2dd823fa8579'
        'SSEUF-ee904e9c-4fb6-4643-88a2-a4e388651568-C:e112bd1-754-946-e35-1a7bf1cbd33-pdf',
        'SSE-85b9353d-45f6-47ca-8510-abdb38bf1d5a-csv',
    ]
    for f in formats:
        assert str(f) == scrub(f)


def test_scrub_warning(caplog):
    caplog.set_level(logging.WARN)
    _ = scrub('This_is_unsafe!../')
    assert "Value 'This_is_unsafe!../' has unsafe chars, scrubbing to 'This_is_unsafe!'"
