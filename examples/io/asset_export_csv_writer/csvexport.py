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


def export_assets_to_csv(fobj, assets, *fields):
    '''
    Generates a CSV file from the fields specified and will pass the keywords
    on to the asset export.

    Args:
        fobj (str): The file object of the csv file to write.
        *fields (list): A listing of fields to export.

    Returns:
        None

    Examples:
        Basic Export:

        >>> export_assets_to_csv('example.csv')

        Choosing the Fields to Export for assets:

        >>> fields = ['plugin.id', 'plugin.name', 'asset.uuid']
        >>> vulns = tio.exports.assets()
        >>> with open('example.csv', 'w') as report:
        ...     export_assets_to_csv(report, vulns, *fields)
    '''
    if not fields:
        fields = [
            'id',
            'fqdns',
            'hostnames',
            'ipv4s',
            'ipv6s',
            'mac_addresses',
            'system_types',
            'created_at',
            'last_scan_time',
            'last_seen',
            'last_authenticated_scan_date',
            'last_licensed_scan_date',
            'updated_at',
            'tags',
        ]

    # Instantiate the dictionary writer, pass it the fields that we would like
    # to have recorded to the file, and inform the writer that we want it to
    # ignore the rest of the fields that may be passed to it.
    writer = DictWriter(fobj, fields, extrasaction='ignore')
    writer.writeheader()
    counter = 0
    for asset in assets:
        counter += 1

        # We need the vulnerability dictionary flattened out and all of the
        # lists converted into a pipe-delimited string.
        flat = flatten(asset)
        for k, v in flat.items():
            if isinstance(v, list):
                flat[k] = '|'.join([str(i) for i in v])
            if k == 'tags':
                flat[k] = '|'.join(['{}:{}'.format(i['key'], i['value']) for i in v])

        # Write the vulnerability to the CSV File.
        writer.writerow(flat)
    return counter


@click.command()
@click.argument('output', type=click.File('w'))
@click.option('--tio-access-key', 'akey', help='Tenable.io API Access Key')
@click.option('--tio-secret-key', 'skey', help='Tenable.io API Secret Key')
@click.option('--field', '-f', 'fields', multiple=True,
    help='Field to export to CSV')
@click.option('--verbose', '-v', envvar='VERBOSITY', default=0,
    count=True, help='Logging Verbosity')
@click.option('--created-at', 'created_at', type=click.INT,
    help='Returns assets created after the specified unix timestamp')
@click.option('--updated-at', 'updated_at', type=click.INT,
    help='Returns assets updated after the specified unix timestamp')
@click.option('--terminated-at', 'terminated_at', type=click.INT,
    help='Returns assets termninated after the specified unix timestamp')
@click.option('--deleted-at', 'deleted_at', type=click.INT,
    help='Returns assets deleted after the specified unix timestamp')
@click.option('--last-authenticated-scan-time', 'last_authenticated_scan_time',
    type=click.INT,
    help='Returns assets that have authenticated results after the specified unix timestamp')
@click.option('--last-assessed', 'last_assessed', type=click.INT,
    help='Returns assets assessed after the specified unix timestamp')
@click.option('--has-plugin-results', 'has_plugin_results', type=click.BOOL,
    help='Returns only assets with plugin results')
@click.option('--tag', 'tags', multiple=True, nargs=2, type=(str, str),
    help='Tag Key/Value pair to restrict the export to.')
@click.option('--source', 'sources', multiple=True, help='Asset Source Data')
@click.option('--chunk-size', 'chunk_size', type=click.INT,
    help='The chunk size to use for exporting the data.')
def cli(output, akey, skey, fields, verbose, **kwargs):
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

    kwargs['sources'] = list(kwargs['sources'])
    kwargs['tags'] = list(kwargs['tags'])
    filters = dict()
    for key in kwargs.keys():
        if kwargs[key]:
            filters[key] = kwargs[key]

    # Instantiate the Tenable.io instance & initiate the vulnerability export.
    tio = TenableIO(akey, skey)
    assets = tio.exports.assets(**filters)

    # Pass everything to the CSV generator.
    total = export_assets_to_csv(output, assets, *fields)
    click.echo('Processed {} Assets'.format(total))


if __name__ == '__main__':
    cli()