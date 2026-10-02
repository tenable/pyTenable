#!/usr/bin/env python
import logging
from csv import DictWriter
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Annotated

from rich.console import Console
from typer import Option, run

from tenable.io import TenableIO
from tenable.io.exports.iterator import ExportsIterator
from tenable.utils import dict_flatten

DEFAULT_FIELDS = (
    'asset.fqdn,asset.hostname,asset.operating_system,asset.uuid,'
    'first_found,last_found,plugin.id,plugin.name,plugin.cve,'
    'plugin.cvss_base_score,plugin.cvss_temporal_score,port.port,'
    'port.protocol,severity,state'
)


class Severity(str, Enum):
    INFO = 'info'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class LogLevel(str, Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'


console = Console()


def export_vulns_to_csv(fname: Path, vulns: ExportsIterator, fields: list[str]):
    # Instantiate the dictionary writer, pass it the fields that we would like
    # to have recorded to the file, and inform the writer that we want it to
    # ignore the rest of the fields that may be passed to it.
    writer = DictWriter(fname.open('w'), fields, extrasaction='ignore')
    writer.writeheader()
    counter = 0
    for vuln in vulns:
        counter += 1

        # We need the vulnerability dictionary flattened out and all of the
        # lists converted into a pipe-delimited string.
        flat = dict_flatten(vuln)
        for k, v in flat.items():
            if isinstance(v, list):
                v = '|'.join([str(i) for i in v])
            if str(v).startswith(('=', '-', '+', '@', '\t', '\n')):
                v = f"'{v}'"
            flat[k] = str(v)

        # Write the vulnerability to the CSV File.
        writer.writerow(flat)
    return counter


def cli(
    report: Annotated[Path, Option('-r', '--report', help='Report file name')] = Path(
        'report.csv'
    ),
    access_key: Annotated[
        str | None, Option(envvar='TIO_ACCESS_KEY', help='TVM Access Key')
    ] = None,
    secret_key: Annotated[
        str | None, Option(envvar='TIO_SECRET_KEY', help='TVM Secret Key')
    ] = None,
    severity: Annotated[
        list[Severity] | None,
        Option('-s', '--severity', help='Severity levels to export'),
    ] = None,
    since: Annotated[
        datetime | None, Option(help='Only Fetch findings observed since this date')
    ] = None,
    cidr: Annotated[str | None, Option(help='Restrict results to this CIDR')] = None,
    tags: Annotated[
        list[str] | None,
        Option(
            '-t',
            '--tag',
            help='Asset tag to restrict to. Tags must be in Category:Value format.',
        ),
    ] = None,
    fields: Annotated[
        str, Option(help='list of fields to report; comma-separated')
    ] = DEFAULT_FIELDS,
    log_level: LogLevel = LogLevel.INFO,
):
    """
    Export -> CSV Writer

    Generates a CSV File from the vulnerability export using the fields
    specified.
    """
    logging.basicConfig(level=log_level.value.upper())
    if since is None:
        since = datetime.now() - timedelta(days=30)

    if severity is None:
        severity = [Severity.MEDIUM, Severity.HIGH, Severity.CRITICAL]

    if tags is not None:
        t = []
        for tag in tags:
            try:
                cat, value = tag.split(':')
                t.append((cat, value))
            except ValueError as err:
                raise ValueError(f'{tag} is not a valid tag.') from err
        tags = t

    # Instantiate the Tenable.io instance & initiate the vulnerability export.
    tio = TenableIO(access_key, secret_key)
    vulns = tio.exports.vulns(
        since=int(since.timestamp()),
        severity=[s.value for s in severity],
        cidr_range=cidr,
        tags=tags,
    )

    # Pass everything to the CSV generator.
    with console.status('Exporting findings and writing them to the report...'):
        total = export_vulns_to_csv(report, vulns, fields)
    console.print(f'Processed {total} Vulnerabilities')


if __name__ == '__main__':
    run(cli)
