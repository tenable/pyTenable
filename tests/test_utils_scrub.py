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
