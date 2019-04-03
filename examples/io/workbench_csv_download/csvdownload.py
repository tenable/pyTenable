#!/usr/bin/env python
'''
The MIT License

Copyright 2019 Tenable, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import argparse, os
from tenable.io import TenableIO

def filterset(s):
    try:
        k,o, v = s.split(':')
        return (k, o, v)
    except:
        raise argparse.ArgumentTypeError('Filters must be name,operator,value')

parser = argparse.ArgumentParser()
parser.add_argument('--tio-access-key',
    dest='tio_access_key',
    help='Tenable.io Access Key',
    default=os.getenv('TIO_ACCESS_KEY'))
parser.add_argument('--tio-secret-key',
    dest='tio_secret_key',
    help='Tenable.io Secret Key',
    default=os.getenv('TIO_SECRET_KEY'))
parser.add_argument('-f', '--filter',
    dest='filters',
    action='append',
    type=filterset,
    help='Filter for the advanced filters in the IO vuln workbench.  can be specified multiple times.')
parser.add_argument('--filter-type',
    dest='filter_type',
    help='Are filters inclusive or exclusive?',
    choices=['and', 'or'])
parser.add_argument('--report-type',
    dest='report_type',
    help='The type of CSV Report to run',
    default='vuln_by_plugin',
    choices=['diff', 'exec_summary', 'vuln_by_host', 'vuln_by_plugin', 'vuln_hosts_summary'])
parser.add_argument('--csv-file',
    dest='filename',
    help='The CSV filename to use',
    default='report.csv')
args = parser.parse_args()

tio = TenableIO(args.tio_access_key, args.tio_secret_key)
if args.filters:
    with open(args.filename, 'wb') as fobj:
        tio.workbenches.export(*args.filters, 
            filter_type=args.filter_type, fobj=fobj, format='csv', 
            chapters=[args.report_type])
else:
    print('No Filters were supplied.  Will not run an empty export.')