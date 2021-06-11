'''
Understanding Tenable Report Formats
------------------------------------

Nessus, SecurityCenter, Tenable.io, and other Tenable applications produce data
in several formats.  While most of these formats are meant to be consumable by
the user directly (such as PDF, CSV, and HTML reports), some of these formats
are meant to be used for machine to machine transfers.  The most notable example
of this is the Nessus version 2 file format.

The Nessus version 2 format is a XML-based format that allows for a wide range
of flexibility in providing different and varied sets of data within a singular
report.  While not very data dense (reports can get quite large in size), it's
easily compressible and well understood.

.. automodule:: tenable.reports.nessusv2
'''
from .nessusv2 import NessusReportv2
