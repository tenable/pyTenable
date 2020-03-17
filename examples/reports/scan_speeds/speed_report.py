#!/usr/bin/env python
from tenable.reports import NessusReportv2
import click, re

@click.command()
@click.argument('report', type=click.File('r'))
def run(report):
    '''
    Per-host Scan Duration Reporting Tool
    '''
    redur = re.compile('Scan duration : (\d+) sec')
    nessus = NessusReportv2(report)
    for v in nessus:
        if v['pluginID'] == 19506:
            res = redur.findall(v['plugin_output'])
            if len(res) > 0:
                print('{} Took {} seconds to complete.'.format(
                    v['host-ip'],
                    res[0]
                ))

if __name__ == '__main__':
    run()