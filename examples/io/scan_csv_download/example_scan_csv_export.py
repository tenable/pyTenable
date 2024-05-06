#!/usr/bin/env python
"""
Export Scan Exmaple
"""
from typing import Optional, List, Tuple
from pathlib import Path
from tenable.io import TenableIO
import logging
import typer


def export_scan(scan_id: int,
                report: Optional[Path] = None,
                access_key: Optional[str] = None,
                secret_key: Optional[str] = None,
                filter_type: str = 'and',
                filters: List[str] = typer.Option(
                    [], '--filter', '-f'
                ),
                debug: bool = False
                ):
    """
    Export Scan ID using predefined filters
    """
    filters = [f.split(':') for f in filters]
    if debug:
        # If debug is enabled, then turn on debug logging to log
        # all output to the console.
        logging.basicConfig(level=logging.DEBUG)

    if not report:
        # If no report path is specified, then generate a default path using
        # the scan id in the current working path.
        report = Path(f'scan-{scan_id}.csv')

    tio = TenableIO(access_key=access_key, secret_key=secret_key)
    with report.open('wb') as fobj:
        tio.scans.export(scan_id,
                         fobj=fobj,
                         filters=filters,
                         filter_type=filter_type
                         )


if __name__ == '__main__':
    typer.run(export_scan)
