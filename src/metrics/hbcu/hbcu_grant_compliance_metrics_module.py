
# HBCU Grant Compliance Tracking Metrics Module
compliance_metric_definitions = [
    { 'metric': 'Compliance Rate by Grant Type', 'description': 'Federal/foundation grants fully compliant' },
    { 'metric': 'Audit Exception Rate', 'description': 'Percent audits with material exceptions' },
    # ... continued ...
]

import pandas as pd

compliance_records = [
    ('Compliance Rate by Grant Type', 'Federal: 96%, Foundation: 92%'),
    ('Audit Exception Rate', '8%'),
]

df_compliance = pd.DataFrame(compliance_records, columns=['Metric','Value'])

# Flag late, inaccurate, or at-risk grants
def flag_noncompliance(df):
    inaccurate = df[(df['Metric'] == 'Grant Report Accuracy Rate') & (df['Value'].apply(lambda x: float(x.replace('%','')) if isinstance(x,str) else 100) < 95)]
    exception = df[(df['Metric'] == 'Audit Exception Rate') & (df['Value'].apply(lambda x: float(x.replace('%','')) if isinstance(x,str) else 0) > 10)]
    at_risk = df[(df['Metric'] == 'Grant Risk Score') & (df['Value'].isin(['High','Moderate']))]
    return pd.concat([inaccurate,exception,at_risk])
# Usage
issues = flag_noncompliance(df_compliance)
print(issues)
