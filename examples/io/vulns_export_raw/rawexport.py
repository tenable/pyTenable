#!/usr/bin/python3

from tenable.io import TenableIO
import json
import os
import click 
import logging
import time
import shutil

@click.command()
@click.option('--access-key', '-a', help='Tenable.io API Access Key')
@click.option('--secret-key', '-s', help='Tenable.io API Secret Key')
@click.option('--days-since', '-d', type=click.INT, default=90, help='Vulnerability last indexed_at in days')
@click.option('--plugins', '-p', default=None, type=click.STRING, help='Comma separated list of plugin(s)')
@click.option('--include-unlicensed', '-l', is_flag=True, help='Export findings from unlicensed assets')
@click.option('--uuid', '-u', default=None, help='Vuln Export Uuid')
@click.option('--working-dir', '-w', type=click.Path(exists=True), default=os.getcwd(), help='Output directory to write vulns and debug')
@click.option('--threads', '-t', type=click.INT, default=4, help='Number of CPU threads')
@click.option('--zip', '-z', is_flag=True, help='Zip results')
def cli(access_key, secret_key, days_since, plugins, include_unlicensed, uuid, working_dir, threads, zip):
    '''
    Export -> RAW Writer

    Exports raw export chunks to a <current-time>-vulns directory. 
    '''

    # Define output directory that will store the chunk export and pytenable logs.
    current_time = int(time.time())
    dir_name = f'{current_time}-vulns'
    output_dir = os.path.join(working_dir, dir_name)
 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Enable logging 
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(output_dir, 'pytenable.logs')),
            logging.StreamHandler()
        ]
    )
    
    # Function that writes vuln chunks to the output directory.
    def write_chunk(data,
                    export_uuid: str,
                    export_type: str,
                    export_chunk_id: int
                     ):
        fn = os.path.join(output_dir, f'{export_type}-{export_uuid}-{export_chunk_id}.json')
        with open(fn, 'w') as fobj:
            json.dump(data, fobj)

    # Convert the days_ago vartaible to unix timestamp 
    indexed_at = current_time - (days_since * 24 * 60 * 60) 

    # Initalize TenableIO
    tio = TenableIO(access_key, secret_key)

    # If export uuid is set: 
    if uuid:
        export = tio.exports.vulns(uuid=uuid)
    
    else:   
        # Apply plugins filter
        if plugins:
            plugin_id = plugins.split(",")
            export = tio.exports.vulns(plugin_id=plugin_id, indexed_at=indexed_at, include_unlicensed=include_unlicensed, state=['OPEN', 'REOPENED', 'FIXED'])
        else:   
            export = tio.exports.vulns(indexed_at=indexed_at, include_unlicensed=include_unlicensed, state=['OPEN', 'REOPENED', 'FIXED']) 

    # Export vulns
    export.run_threaded(write_chunk, num_threads=threads)

    if zip: 
        shutil.make_archive(output_dir, 'zip', output_dir)

if __name__ == '__main__':
    cli()
