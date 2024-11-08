import pytest


def test_import_io_pkg():
    from tenable.io import TenableIO


def test_import_sc_pkg():
    from tenable.sc import TenableSC


def test_import_ad_pkg():
    from tenable.ie import TenableIE


@pytest.mark.skip
def test_import_nessus_pkg():
    from tenable.nessus import Nessus


def test_import_dl_pkg():
    from tenable.dl import Downloads


def test_import_reports_pkg():
    from tenable.reports.nessusv2 import NessusReportv2


def test_import_ot_pkg():
    from tenable.ot import TenableOT
