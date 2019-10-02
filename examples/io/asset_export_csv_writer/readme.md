# Vuln Export CSV File Generator

Generates a CSV File from the asset export.  Specific fields can be
specified from the asset documents using dot notation.

## Install

```bash
pip install -r requirements.txt
```

## Usage

Export all assets with default settings:

```bash
./csvexport.py example.csv
```

In-tool help:

```
Usage: csvexport.py [OPTIONS] OUTPUT

  Export -> CSV Writer

  Generates a CSV File from the vulnerability export using the fields
  specified.

Options:
  --tio-access-key TEXT           Tenable.io API Access Key
  --tio-secret-key TEXT           Tenable.io API Secret Key
  -f, --field TEXT                Field to export to CSV
  -v, --verbose                   Logging Verbosity
  --created-at INTEGER            Returns assets created after the specified
                                  unix timestamp
  --updated-at INTEGER            Returns assets updated after the specified
                                  unix timestamp
  --terminated-at INTEGER         Returns assets termninated after the
                                  specified unix timestamp
  --deleted-at INTEGER            Returns assets deleted after the specified
                                  unix timestamp
  --last-authenticated-scan-time INTEGER
                                  Returns assets that have authenticated
                                  results after the specified unix timestamp
  --last-assessed INTEGER         Returns assets assessed after the specified
                                  unix timestamp
  --has-plugin-results BOOLEAN    Returns only assets with plugin results
  --tag <TEXT TEXT>...            Tag Key/Value pair to restrict the export
                                  to.
  --source TEXT                   Asset Source Data
  --chunk-size INTEGER            The chunk size to use for exporting the
                                  data.
  --help                          Show this message and exit.
```