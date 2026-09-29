#!/usr/bin/env python
import os
from pathlib import Path
from typing import Annotated, Literal

import arrow
from rich.console import Console
from typer import Option, run

from tenable.io import TenableIO

console = Console()


def download_scans(
    access_key: Annotated[
        str | None, Option(envvar='TIO_ACCESS_KEY', help='TVM Access Key')
    ] = None,
    secret_key: Annotated[
        str | None, Option(envvar='TIO_SECRET_KEY', help='TVM Secret Key')
    ] = None,
    search: Annotated[str, Option('--search', '-s', help='Scan Name search')] = '',
    path: Annotated[Path, Option('-p', '--path', help='Download path')] = Path('.'),
    filters: Annotated[
        list[tuple[str, str, str]] | None,
        Option(
            '--filter',
            '-f',
            help='Filter the output using the specified name, operator, and value.\nExample: -f plugin.id eq 19506',
        ),
    ] = None,
    format: Annotated[
        Literal['csv', 'nessus'], Option(help='Report format type')
    ] = 'nessus',
    filter_type: Annotated[
        Literal['and', 'or'], Option(help='filter grouping type')
    ] = 'and',
):
    """
    Attempts to download the latest completed scan from tenable.io and stores
    the file in the path specified.  The exported scan will be filtered based
    on the filters specified.
    """
    tio = TenableIO(access_key, secret_key)
    if filters is None:
        filters = []

    # Get the list of scans that match the name filter defined.
    scans = [s for s in tio.scans.list() if search.lower() in s['name'].lower()]
    for scan in scans:
        details = tio.scans.results(scan['id'])

        # get the list of scan histories that are in a completed state.
        completed = [
            h for h in details.get('history', list()) if h.get('status') == 'completed'
        ]

        # download the latest completed scan using the scan name && history id
        # and store the file in the path specified using the filename format:
        # scan-{SCAN_NAME}-{HISTORY_ID}.{FORMAT}
        if len(completed) > 0:
            history = completed[0]
            name = scan['name'].replace(' ', '_')
            hid = history['uuid']
            fname = path.joinpath(f'scan-{name}-{hid}.{format}')
            with (
                open(fname, 'wb') as report_file,
                console.status(f'Downloading {name}:{hid} to {fname}'),
            ):
                tio.scans.export(
                    scan['id'],
                    *filters,
                    history_id=hid,
                    fobj=report_file,
                    filter_type=filter_type,
                    format=format,
                )


if __name__ == '__main__':
    run(download_scans)
