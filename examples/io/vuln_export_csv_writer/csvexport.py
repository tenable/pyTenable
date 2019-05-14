#!/usr/bin/env python
from tenable.io import TenableIO
from csv import DictWriter
import collections, click, logging


def flatten(d, parent_key='', sep='.'):
    '''
    Flattens a nested dict.  Shamelessly ripped from 
    `this <https://stackoverflow.com/a/6027615>`_ Stackoverflow answer.
    '''
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def export_vulns_to_csv(fobj, vulns, *fields):
    '''
    Generates a CSV file from the fields specified and will pass the keywords
    on to the vuln export.

    Args:
        fobj (str): The file object of the csv file to write.
        *fields (list): A listing of fields to export.
    
    Returns:
        None
    
    Examples:
        Basic Export:

        >>> export_vulns_to_csv('example.csv')

        Choosing the Fields to Export for high and critical vulns:
        
        >>> fields = ['plugin.id', 'plugin.name', 'asset.uuid']
        >>> vulns = tio.exports.vulns()
        >>> with open('example.csv', 'w') as report:
        ...     export_vulns_to_csv(report, vulns, *fields)
    '''
    if not fields:
        fields = [
            'asset.fqdn', 
            'asset.hostname', 
            'asset.operating_system',
            'asset.uuid',
            'first_found',
            'last_found',
            'plugin.id',
            'plugin.name',
            'plugin.cve',
            'plugin.cvss_base_score',
            'plugin.csvv_temporal_score',
            'port.port',
            'port.protocol',
            'severity',
            'state'
        ]
    
    # Instantiate the dictionary writer, pass it the fields that we would like
    # to have recorded to the file, and inform the writer that we want it to
    # ignore the rest of the fields that may be passed to it.
    writer = DictWriter(fobj, fields, extrasaction='ignore')
    writer.writeheader()
    counter = 0
    for vuln in vulns:
        counter += 1

        # We need the vulnerability dictionary flattened out and all of the
        # lists converted into a pipe-delimited string.
        flat = flatten(vuln)
        for k, v in flat.items():
            if isinstance(v, list):
                flat[k] = '|'.join([str(i) for i in v])
        
        # Write the vulnerability to the CSV File.
        writer.writerow(flat)
    return counter


@click.command()
@click.argument('output', type=click.File('w'))
@click.option('--tio-access-key', 'akey', help='Tenable.io API Access Key')
@click.option('--tio-secret-key', 'skey', help='Tenable.io API Secret Key')
@click.option('--severity', 'sevs', multiple=True, help='Vulnerability Severity')
@click.option('--last-found', type=click.INT, 
    help='Vulnerability Last Found Timestamp')
@click.option('--cidr', help='Restrict export to this CIDR range')
@click.option('--tag', 'tags', multiple=True, nargs=2, type=(str, str),
    help='Tag Key/Value pair to restrict the export to.')
@click.option('--field', '-f', 'fields', multiple=True, 
    help='Field to export to CSV')
@click.option('--verbose', '-v', envvar='VERBOSITY', default=0,
    count=True, help='Logging Verbosity')
def cli(output, akey, skey, sevs, last_found, cidr, tags, fields, verbose):
    '''
    Export -> CSV Writer

    Generates a CSV File from the vulnerability export using the fields
    specified.
    '''
    # Setup the logging verbosity.
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
    
    # Instantiate the Tenable.io instance & initiate the vulnerability export.
    tio = TenableIO(akey, skey)
    vulns = tio.exports.vulns(last_found=last_found, severity=list(sevs), 
        cidr_range=cidr, tags=list(tags))
    
    # Pass everything to the CSV generator.
    total = export_vulns_to_csv(output, vulns, *fields)
    click.echo('Processed {} Vulnerabilities'.format(total))


if __name__ == '__main__':
    cli()