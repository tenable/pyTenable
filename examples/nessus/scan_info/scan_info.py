#!/usr/bin/env python
from typing import List
from tenable.nessus import Nessus
from restfly.errors import UnauthorizedError
from rich import print
import typer


app = typer.Typer()


@app.command()
def run(url: str = typer.Option(None, help='Nessus Service URL'),
        access_key: str = typer.Option(None, help='Nessus API Access Key'),
        secret_key: str = typer.Option(None, help='Nessus API Secret Key'),
        restricted: List[int] = typer.Option([], '-s', '--scan',
                                             help='Limit to specified scans'),
        ):
    """
    Gets the basic scan information
    """
    nessus = Nessus(url=url,
                    access_key=access_key,
                    secret_key=secret_key,
                    box=True
                    )
    try:
        nessus.session.get()
    except UnauthorizedError:
        print(f'[red]Connection Error Talking to {nessus._url}')
        exit()

    for s in nessus.scans.list().scans:
        if restricted and s.id not in restricted:
            continue
        scan = nessus.scans.details(s.id)
        if not scan.info.status[-2:] == 'ed':
            print(f'Scan {s.id} is currently in an active state, skipping.')
            continue
        for item in scan.prioritization.plugins:
            for host in item.hosts:
                print(f'timestamp={scan.info.timestamp} '
                      f'plugin_id={item.pluginattributes.plugin_information.plugin_id} '
                      f'host_ip={host.ip}'
                      )

if __name__ == '__main__':
    app()
