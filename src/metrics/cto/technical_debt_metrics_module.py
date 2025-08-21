
# Technical Debt Tracking & Remediation Metrics Module
techdebt_metric_definitions = [
    { 'metric': 'Technical Debt Score', 'description': 'Weighted indicator of tech debt severity' },
    { 'metric': 'Remediation Progress (%)', 'description': 'Percent completed of debt work plan' },
    # ... continued for all metrics ...
]

import pandas as pd

techdebt_records = [
    ('Old ERP System', 'Technical Debt Score', 7.9),
    ('Legacy Email Server', 'Remediation Progress (%)', '36.3%'),
]

df_debt = pd.DataFrame(techdebt_records, columns=['Component','Metric','Value'])

# Dashboard logic: flag high technical debt or slow progress
def flag_high_debt(df):
    severe = df[(df['Metric'] == 'Technical Debt Score') & (df['Value'] > 7)]
    slow_remed = df[(df['Metric'] == 'Remediation Progress (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 100) < 30)]
    critical_impact = df[(df['Metric'] == 'Debt Impact Rating') & (df['Value'] == 'Critical')]
    return pd.concat([severe,slow_remed,critical_impact])
# Usage
issues = flag_high_debt(df_debt)
print(issues)
