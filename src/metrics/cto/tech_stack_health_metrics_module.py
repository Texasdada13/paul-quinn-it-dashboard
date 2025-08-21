
# Technology Stack Health Monitoring Metrics Module
stack_metric_definitions = [
    { 'metric': 'Performance Health Score', 'description': 'Composite tech health rating (1-10)' },
    { 'metric': 'Patch/Update Status', 'description': 'Is tech up-to-date?' },
    # ... continued for all metrics ...
]

import pandas as pd

stack_records = [
    ('Nginx Web Proxy', 'Performance Health Score', 8.2),
    ('Okta SSO', 'Patch/Update Status', 'No'),
]

df_stack = pd.DataFrame(stack_records, columns=['Component','Metric','Value'])

# Dashboard alert logic: flag any with poor health (<7), overdue patch, or support risk
def flag_at_risk_stack(df):
    unhealthy = df[(df['Metric'] == 'Performance Health Score') & (df['Value'] < 7)]
    unpatched = df[(df['Metric'] == 'Patch/Update Status') & (df['Value'] == 'No')]
    eol_risk = df[(df['Metric'] == 'End-of-Life Risk Flag') & (df['Value'] == 'Yes')]
    return pd.concat([unhealthy,unpatched,eol_risk])
# Usage
risk_components = flag_at_risk_stack(df_stack)
print(risk_components)
