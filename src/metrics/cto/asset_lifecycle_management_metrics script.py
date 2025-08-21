import pandas as pd
import numpy as np
from datetime import timedelta

# CTO Metrics: Asset lifecycle management, maintenance schedules, replacement planning
asset_metrics = [
    ('Asset Name', 'Description of hardware/software asset'),
    ('Asset Type', 'Category: Server, Switch, Laptop, Application, HVAC, etc.'),
    ('Purchase Date', 'Original procurement/acquisition date'),
    ('Warranty Expiry', 'Warranty/support end date'),
    ('Current Condition', 'Rating descriptor: New, Good, Fair, Poor'),
    ('Maintenance Schedule', 'Next scheduled maintenance/check-up date'),
    ('Last Maintenance Date', 'Date of last routine or emergency service'),
    ('Usage Hours', 'Cumulative hours asset in use since purchase'),
    ('Age (years)', 'Asset age since purchase'),
    ('Replacement Threshold', 'Pre-defined age/condition required for replacement'),
    ('Replacement Due Flag', 'Scheduled or recommended replacement status'),
    ('Expected Replacement Date', 'Planned replacement or retirement date'),
    ('Estimated Residual Value ($)', 'Estimated resale or salvage value at end of life'),
    ('Maintenance Cost To Date', 'Total cost for all maintenance actions'),
    ('Planned Maintenance Budget ($)', 'Budget set aside for scheduled maintenance'),
    ('Failure Incident Count', 'Number of failures/outages to date'),
    ('Support Ticket Volume (12mo)', 'Number of IT/work order tickets logged'),
]

assets = ['Core Network Switch', 'Dell Server R740', 'Staff Laptop A14', 'HVAC Controller',
          'Student Portal Application', 'Library Firewall', 'Cisco IP Phone', 'Facilities UPS']
np.random.seed(33)
asset_example_data = []
for metric, description in asset_metrics:
    for asset in assets:
        if 'Purchase' in metric or 'Last Maintenance' in metric or 'Expected Replacement' in metric or 'Schedule' in metric or 'Expiry' in metric:
            days = int(np.random.uniform(10,1800))
            value = (pd.Timestamp('2020-01-01') + timedelta(days=days)).strftime('%Y-%m-%d')
        elif 'Type' in metric:
            value = np.random.choice(['Server','Switch','Laptop','Application','Firewall','Phone','Controller','UPS'])
        elif 'Condition' in metric:
            value = np.random.choice(['New','Good','Fair','Poor'])
        elif 'Usage Hours' in metric:
            value = np.random.randint(300, 18500)
        elif 'Age' in metric or 'Threshold' in metric:
            value = np.round(np.random.uniform(0.3,7.5),1)
        elif 'Flag' in metric:
            value = np.random.choice(['Yes','No'])
        elif 'Value' in metric or 'Budget' in metric or 'Cost' in metric:
            value = f"${np.random.randint(200,16500):,}"
        elif 'Incident' in metric or 'Ticket' in metric:
            value = np.random.randint(0,36)
        else:
            value = 'N/A'
        asset_example_data.append((asset, metric, description, value))

asset_dashboard_df = pd.DataFrame(asset_example_data, columns=['Asset','Metric','Description','Example'])
asset_dashboard_df.to_csv('asset_lifecycle_management_dashboard_examples.csv', index=False)
print('Asset lifecycle management metrics CSV with examples saved.')

# Optional python module template
script_asset = '''\n# Asset Lifecycle Management Metrics Module\nasset_metric_definitions = [\n    { 'metric': 'Maintenance Schedule', 'description': 'Next scheduled asset maintenance date' },\n    { 'metric': 'Replacement Due Flag', 'description': 'Indicator for replacement readiness' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\nasset_records = [\n    ('Dell Server R740', 'Maintenance Schedule', '2025-03-15'),\n    ('Staff Laptop A14', 'Replacement Due Flag', 'Yes'),\n]\n\ndf_asset = pd.DataFrame(asset_records, columns=['Asset','Metric','Value'])\n\n# Dashboard logic: flag assets with overdue maintenance/replacement\ndef flag_asset_issues(df):\n    overdue = df[(df['Metric'] == 'Replacement Due Flag') & (df['Value'] == 'Yes')]
    maintenance = df[(df['Metric'] == 'Maintenance Schedule') & (pd.to_datetime(df['Value']) < pd.Timestamp('2025-08-19'))]
    return pd.concat([overdue,maintenance])\n# Usage\nissues = flag_asset_issues(df_asset)\nprint(issues)\n'''
with open('asset_lifecycle_management_metrics_module.py', 'w') as f:
    f.write(script_asset)
print('Asset lifecycle management metrics module Python script saved.')