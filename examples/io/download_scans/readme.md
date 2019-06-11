# Scan Export Downloader

Downloads scans based on the specified parameters.

## Install

```bash
pip install -r requirements.txt
```

## Usage

In-tool help:

```
Usage: download_scans.py [OPTIONS]

  Attempts to download the latest completed scan from tenable.io and stores
  the file in the path specified.  The exported scan will be filtered based
  on the filters specified.

Options:
  --tio-access-key TEXT           Tenable.io API Access Key
  --tio-secret-key TEXT           Tenable.io API Secret Key
  -p, --download-path PATH        The path to where the downloaded report
                                  files will reside.
  -s, --search TEXT               The search filter to use on the scan names.
  -f, --filter <TEXT TEXT TEXT>...
                                  Filter the output using the specified name,
                                  operator, and value such as: -f plugin.id eq
                                  19506
  -r, --report-format [csv|nessus]
                                  The report format. Acceptable values are
                                  "csv" and "nessus".
  --filter-type [and|or]          Should the filters all match ("and") or any
                                  of them match ("or").
  --help                          Show this message and exit.
```