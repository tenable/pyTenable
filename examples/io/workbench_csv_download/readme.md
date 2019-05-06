# CSV Download Tool

The CSV Export tool is a simple python script to download a CSV report based
on the filterset provided.

## Usage

Download the CSV report of critical an exploitable vulnerabilities:

```bash
csvdownload -f severity:eq:Critical \
    -f plugin.attributes.exploit_available:eq:true \
    --csv-file crit_and_exploit.csv
```

Download the CSV report for a unsupported operating systems:

```bash
csvdownload -f plugin.name:match:Unsupported --csv-file unsupported.csv
```

Download the Nessus Scan Report for all hosts:

```bash
csvdownload -f plugin.id:eq:19506 -f severity:eq:Info --csv-file scan_reports.csv
```

Download a report of the High & Critical Vulns and email that off to someone

```bash
csvdownload -f severity:eq:High -f severity:eq:Critical --filter-type or \
    --csv-file high_and_crit.csv
mail -s 'High & Critical Vulns Report' user@company.tld -A high_and_crit.csv
```

The in-tool help document:

```
➜ ./csvdownload.py -h
usage: csvdownload.py [-h] [--tio-access-key TIO_ACCESS_KEY]
                      [--tio-secret-key TIO_SECRET_KEY] [-f FILTERS]
                      [--filter-type {and,or}]
                      [--report-type {diff,exec_summary,vuln_by_host,vuln_by_plugin,vuln_hosts_summary}]
                      [--csv-file FILENAME]

optional arguments:
  -h, --help            show this help message and exit
  --tio-access-key TIO_ACCESS_KEY
                        Tenable.io Access Key
  --tio-secret-key TIO_SECRET_KEY
                        Tenable.io Secret Key
  -f FILTERS, --filter FILTERS
                        Filter for the advanced filters in the IO vuln
                        workbench. can be specified multiple times.
  --filter-type {and,or}
                        Are filters inclusive or exclusive?
  --report-type {diff,exec_summary,vuln_by_host,vuln_by_plugin,vuln_hosts_summary}
                        The type of CSV Report to run
  --csv-file FILENAME   The CSV filename to use
```
