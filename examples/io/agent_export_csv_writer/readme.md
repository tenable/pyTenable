# Agent CSV File Generator

Generates a CSV of agents with the ability to filter by agent health

## Install

```bash
pip install -r requirements.txt
```

## Usage
Export all agents and write results to agents.csv

```bash
./agentexport.py --access-key <access-key> --secret-key <secret-key> agents.csv
```

Export unhealthy agents and write results to agents.csv

```bash
./agentexport.py --access-key <access-key> --secret-key <secret-key> --health 'WARNING,CRITICAL' agents.csv
```

Export healthy agents write results to agents.csv

```bash
./agentexport.py --access-key <access-key> --secret-key <secret-key> --health 'HEALTHY' agents.csv
```

Export unknown agents and write results to agents.csv

```bash
./agentexport.py --access-key <access-key> --secret-key <secret-key> --health 'UNKNOWN' agents.csv
```

In-tool help:

```
Usage: agentexport.py [OPTIONS] OUTPUT

  Agent -> CSV Writer

  Exports agents to a CSV in the current directory.

Options:
  -s, --access-key TEXT  Tenable VM API Access Key
  -a, --secret-key TEXT  Tenable VM API Secret Key
  -e, --health TEXT      Comma separated list of agent health
  -d, --debug            Enable debugging
  --help                 Show this message and exit.
```
