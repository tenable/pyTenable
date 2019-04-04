# Vuln Export CSV File Generator

Generates a CSV File from the vulnerability export.  Specific fields can be
specified from the vulnerability documents using dot notation.

## Install

```bash
pip install -r requirements.txt
```

## Usage

Export all vulnerabilities with default settings:

```bash
./csvexport.py example.csv
```

Export only the high and critical vulnerabilities and output the plugin.id, 
plugin.name, and asset.uuid attributes:

```bash
./csvexport.py -f plugin.id -f asset.uuid -f plugin.name \
    --severity high --severity critical example2.csv
```

In-tool help:

```
Usage: csvexport.py [OPTIONS] OUTPUT

  Export -> CSV Writer

  Generates a CSV File from the vulnerability export using the fields
  specified.

Options:
  --tio-access-key TEXT  Tenable.io API Access Key
  --tio-secret-key TEXT  Tenable.io API Secret Key
  --severity TEXT        Vulnerability Severity
  --last-found INTEGER   Vulnerability Last Found Timestamp
  --cidr TEXT            Restrict export to this CIDR range
  --tag <TEXT TEXT>...   Tag Key/Value pair to restrict the export to.
  --field TEXT           Field to export to CSV
  -v, --verbose          Logging Verbosity
  --help                 Show this message and exit.
```