from tenable.apa import TenableAPA
import datetime

# tapa = TenableAPA(access_key='ACCESS_KEY', secret_key='SECRET_KEY')

tapa = TenableAPA(access_key="13d039bc2b338dbf32ee9a619bdf1280ee53bf6ebde5aed19925aefedd122224",
                  secret_key='9197214820814ce3b9fccfa3f9bb1061a1e71c6587e3877b1f0b7f4bac24f620')

# Get attack path findings with attack path count of 10+ for a given CVE (such as CVE-2021-44228)

# findings = tapa.findings.list(
#     filter='{"operator": "and", "value": [{"operator": ">", "key": "vectorCount", "value": 10}, '
#            '{"operator": "==", "key": "cve", "value": "CVE-2021-44228"}]}')
# for f in findings:
#     print(f)
#
# # Get all attack path findings that were updated within the last weak
#
# today = datetime.date.today()
# seven_days_ago = today - datetime.timedelta(days=7)
# seven_days_ago_iso = str(seven_days_ago.isoformat())
#
# findings = tapa.findings.list(filter=f'{{"operator": ">", "key": "last_updated_at", "value": "{seven_days_ago_iso}"}}')
# for f in findings:
#     print(f)
#
# # Get all attack paths findings associated with password analysis IoE
#
# findings = tapa.findings.list(
#     filter='{"operator": "includes", "key": "detection_ids", "value": "C-PASSWORD-HASHES-ANALYSIS"}')
# for f in findings:
#     print(f)

# Get all attack paths findings with choke point priority of high and above

findings = tapa.findings.list(
    filter='{"operator": "or", "value": [{"operator": "==", "key": "priority", "value": "high"}, '
           '{"operator": "==", "key": "priority", "value": "critical"}]}')

for f in findings:
    print(f)
