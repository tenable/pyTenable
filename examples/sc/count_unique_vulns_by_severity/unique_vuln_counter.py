#!/usr/bin/env python
from tenable.sc import TenableSC

# Login to Tenable.sc
sc = TenableSC('ADDRESS')
sc.login('USERNAME', 'PASSWORD')

# Build the Counter Dictionary
sevs = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}

# Iterate through the Vulnerability Summary, counting up the vulns based on\
# criticality.
for vuln in sc.analysis.vulns(('severity', '=', '4,3,2,1'), tool='sumid'):
    if vuln['severity']['name'] in sevs:
        sevs[vuln['severity']['name']] += 1

# Output the final counts:
print('Crits : {Critical}\nHighs : {High}\nMediums : {Medium}\nLows : {Low}'.format(**sevs))