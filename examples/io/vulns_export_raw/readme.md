# Vuln Export RAW Generator

Generates a folder called 'vulns' and saves vulns export chunks to this folder, along with pyTenable DEBUG logs, and zips results. Supports parameters
such as a Vulns Export UUID, plugin ids. 
## Install

```bash
pip install -r requirements.txt
```

## Usage

Export all vulnerabilities with default settings:

```bash
./rawexport.py 
```

Exports all plugin 1560001,156001 results since 90 days ago and writes results to the /tmp directory. 

```bash
./rawexport.py /tmp -p 156000,156001 -a 90
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
