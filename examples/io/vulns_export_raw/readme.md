# Vuln Export RAW Generator

Generates a folder called '<current_time>-vulns' and saves vulns export chunks to this folder, along with pyTenable DEBUG logs, and zips results. Supports parameters
such as a Vulns Export UUID, plugin ids, include-unlicensed, and days-since.
## Install

```bash
pip install -r requirements.txt
```

## Usage

Export all vulnerabilities with default settings:

```bash
./rawexport.py --access-key <ACCESS_KEY> --secret-key <SECRET_KEY>
```

Exports all plugin 187240 and 172360 since 180 days ago and write and archive the results to the /tmp directory 

```bash
./rawexport.py --access-key <ACCESS_KEY> --secret-key <SECRET_KEY> -w /tmp -p 187240,172360 -d 180 -z
```

In-tool help:

```
Usage: rawexport.py [OPTIONS] OUTPUT

  Export -> RAW Writer

  Exports raw export chunks to a <current-time>-vulns directory.

Options:
  -a, --access-key TEXT     Tenable.io API Access Key
  -s, --secret-key TEXT     Tenable.io API Secret Key
  -d, --days-since INTEGER    Vulnerability last indexed_at in days
  -p, --plugins TEXT        Comma separated list of plugin(s)
  -l, --include-unlicensed  Export findings from unlicensed assets
  -u, --uuid TEXT           Vuln Export Uuid
  -w, --working-dir PATH    Output directory to write vulns and debug
  -t, --threads INTEGER     Number of CPU threads
  -z, --zip                 Zip results
  --help                    Show this message and exit.
```
