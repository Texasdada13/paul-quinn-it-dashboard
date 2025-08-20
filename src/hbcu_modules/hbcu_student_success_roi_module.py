
# HBCU Student Success ROI Metrics Module
roi_metric_definitions = [
    { 'metric': 'Graduation Rate', 'description': 'Percent students graduating after tech adoption' },
    { 'metric': 'Economic Mobility Index', 'description': 'Earnings/wage growth post graduation' },
    # ... continued ...
]

import pandas as pd

roi_records = [
    ('Technology-Linked Graduation Rate', '78%'),
    ('Economic Mobility Index', '23% increase over 3 years'),
]

df_roi = pd.DataFrame(roi_records, columns=['Metric','Value'])

# Flag low ROI or tech engagement
def flag_low_success(df):
    grad = df.loc[df['Metric'] == 'Technology-Linked Graduation Rate', 'Value'].str.replace('%','').astype(float)
    mobility = df.loc[df['Metric'] == 'Economic Mobility Index', 'Value'].str.extract(r'(\d+)')[0].astype(float)
    grad_issues = df.loc[grad < 70]
    mobility_issues = df.loc[mobility < 10]
    return pd.concat([grad_issues,mobility_issues])
# Usage
issues = flag_low_success(df_roi)
print(issues)
