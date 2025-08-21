
# Security Metrics & Incident Response Module
security_metric_definitions = [
    { 'metric': 'Open Vulnerabilities Count', 'description': 'Unresolved security threats' },
    { 'metric': 'Mean Time to Respond (MTTR)', 'description': 'Hours to containment/remediation' },
    # ... continued ...
]

import pandas as pd

security_records = [
    ('ERP System', 'Open Vulnerabilities Count', 7),
    ('Email Suite', 'Mean Time to Respond (MTTR)', 18.2),
]

df_security = pd.DataFrame(security_records, columns=['Asset','Metric','Value'])

# Dashboard logic: flag high-severity, slow response, or low coverage 
def flag_security_issues(df):
    critical_vuln = df[(df['Metric'] == 'Critical Vulnerabilities %') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) > 25)]
    slow_mttr = df[(df['Metric'] == 'Mean Time to Respond (MTTR)') & (df['Value'] > 24)]
    incomplete_cov = df[(df['Metric'] == 'Endpoint Protection Coverage') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 85)]
    return pd.concat([critical_vuln,slow_mttr,incomplete_cov])
# Usage
issues = flag_security_issues(df_security)
print(issues)
