
# Asset Lifecycle Management Metrics Module
asset_metric_definitions = [
    { 'metric': 'Maintenance Schedule', 'description': 'Next scheduled asset maintenance date' },
    { 'metric': 'Replacement Due Flag', 'description': 'Indicator for replacement readiness' },
    # ... continued for all metrics ...
]

import pandas as pd

asset_records = [
    ('Dell Server R740', 'Maintenance Schedule', '2025-03-15'),
    ('Staff Laptop A14', 'Replacement Due Flag', 'Yes'),
]

df_asset = pd.DataFrame(asset_records, columns=['Asset','Metric','Value'])

# Dashboard logic: flag assets with overdue maintenance/replacement
def flag_asset_issues(df):
    overdue = df[(df['Metric'] == 'Replacement Due Flag') & (df['Value'] == 'Yes')]
    maintenance = df[(df['Metric'] == 'Maintenance Schedule') & (pd.to_datetime(df['Value']) < pd.Timestamp('2025-08-19'))]
    return pd.concat([overdue,maintenance])
# Usage
issues = flag_asset_issues(df_asset)
print(issues)
