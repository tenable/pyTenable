#!/usr/bin/env python
import typing
import uuid
from csv import DictWriter
from pathlib import Path
from rich.console import Console
from rich.table import Table
from restfly.utils import dict_flatten, dict_merge, trunc
from tenable.io import TenableIO
import arrow
import typer
import tomlkit

if typing.TYPE_CHECKING:
    from tenable.io.exports.iterator import ExportsIterator


__version__ = '1.0.0'
app = typer.Typer(add_completion=False)
console = Console()


def tvm_data(assets_iter: 'ExportsIterator',
             vulns_iter: 'ExportsIterator',
             asset_fields: list[str],
             reports: list[dict],
             ) -> dict:
    # Yes this is expensive on memory, however it's the only way to get the
    # other asset attributes available within the finding without building a
    # database to match everything up into.
    if not asset_fields:
        asset_fields = []
    assets = {}
    for asset in assets_iter:
        # The base asset dictionary that we will be passing on to the findings
        adict = {
            'tags': [f'{t["key"]}:{t["value"]}' for t in asset['tags']],
            'reports': [],
        }

        # for every additional field that was passed, we will attempt to pull
        # the field from the asset (if it exists) and add it to the asset
        # object.
        for field in asset_fields:
            if field in asset.keys():
                adict[field] = asset[field]

        # Next we will mark the asset with the reports that it will be a member
        # of.  It seems a lot more efficient to do this here than to check per
        # finding.
        for report in reports:
            matched = 0
            for tag in report['tags']:
                if tag in adict['tags']:
                    matched += 1
            if (
                (matched > 0 and report.get('match') == 'any') # any of the tags
                or (matched == len(report['tags'])) # all of the tags
            ):
                adict['reports'].append(report['name'])
        assets[asset['id']] = adict

    for finding in vulns_iter:
        # Merge the relevant asset's data into the finding object.
        finding['asset'] = dict_merge(finding['asset'],
                                      assets[finding['asset']['uuid']]
                                      )

        # Flatten the data structure into a flat dictionary.
        f = dict_flatten(finding)

        # Calculate the age of the finding.
        last_found = arrow.get(f.get('last_found'))
        first_found = arrow.get(f.get('first_found'))
        f['age'] = (last_found - first_found).days

        # Return the augmented finding to the caller.
        yield f


@app.command()
def reports(report_path: Path = Path('reports'),
            config_file: Path = Path('reports.toml'),
            ):
    """
    Generates the reports as defined by the configuration file.
    """

    # Open the configuration file and load the config into memory
    with config_file.open('r', encoding='utf-8') as cobj:
        config = tomlkit.load(cobj)

    # Ensure that the folder exists and create it if it doesn't.  Then we will
    # check to see if the path exists and is a folder, if not, we will bail.
    report_path.mkdir(parents=True, exist_ok=True)
    if not (report_path.exists() and report_path.is_dir()):
        console.print('FATAL :: Invalid report path')
        raise typer.Exit(code=1)

    # Get the field , reports, and other definitions necessary    fields = config['fields']
    reports = config['report']
    fields = config['field']

    # Get the severity field and default to medium, high, and critical if
    # unspecified.
    severity = config['tenable'].get('severity',
                                     ['medium', 'high', 'critical']
                                     )

    # Construct the since timestamp based on the age config parameter.
    since = int(arrow.now()
                     .shift(days=-config['tenable'].get('age', 90))
                     .floor('day')
                     .timestamp()
                )

    # Get the list of asset fields from the field definitions.
    afields = [f['value'][6:] for f in fields if f['value'][:5] == 'asset']

    # Open all the report files.
    rdict = {}
    for report in reports:
        robj = {
            'fobj': report_path.joinpath(report['filename'])\
                               .open('w', encoding='utf-8')
        }
        robj['csv'] = DictWriter(robj['fobj'],
                                 fieldnames=[f['name'] for f in fields]
                                 )
        robj['csv'].writeheader()
        rdict[report['name']] = robj

    tvm = TenableIO(access_key=config['tenable'].get('access_key'),
                    secret_key=config['tenable'].get('secret_key'),
                    vendor='Tenable',
                    product='CSV Report Builder',
                    build=__version__
                    )

    # Start the asset and vuln exports jobs
    assets = tvm.exports.assets(updated_at=since)
    vulns = tvm.exports.vulns(since=since,
                              severity=severity,
                              include_unlicensed=True,
                              )

    # Iterate over each finding from the merged asset/vuln findings.
    with console.status('Building the Reports...'):
        for finding in tvm_data(assets, vulns, afields, reports):
            row = {}

            # construct the row based on the field configuration.
            for field in fields:
                value = finding.get(field['value'], '')
                if isinstance(value, list):
                    value = ', '.join(value)
                else:
                    value = str(value)
                row[field['name']] = trunc(value, limit=32767)

            # add the row to each report that the asset is defined within.
            for report_name in finding['asset.reports']:
                rdict[report_name]['csv'].writerow(row)

        for name, report in rdict.items():
            report['fobj'].close()


if __name__ == '__main__':
    app()
