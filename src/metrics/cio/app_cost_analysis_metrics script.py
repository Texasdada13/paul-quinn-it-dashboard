import pandas as pd
import numpy as np

# Define metrics for application and service total cost analysis, redundancy identification
cost_metrics = [
    ('Total Cost of Ownership (TCO)', 'Sum of initial, recurring, end-of-life costs over expected service period'),
    ('Annual License/Subscription Cost', 'Yearly direct spend on licenses/subscriptions'),
    ('Support/Maintenance Cost', 'Annual cost for vendor or internal support'),
    ('Implementation Cost', 'Total resource and consulting cost for rollout'),
    ('Upgrade/Enhancement Cost', 'Cost invested in customizations, upgrades, add-ons'),
    ('Utilization Rate (%)', 'Percent of seats/features actively used versus provisioned'),
    ('Redundancy Index', 'Count of alternative apps/services with overlapping capability'),
    ('Consolidation Potential', 'Yes/No if system eligible for replacement/merging'),
    ('Cost per Active User', 'Annual license/support cost divided by active user count'),
    ('Feature Utilization Index', 'Percent of key features used versus available'),
    ('Duplicate Functionality Detected', 'Key overlapping processes flagged (True/False)'),
    ('Annual Downtime Loss ($)', 'Dollar cost of lost productivity from outages'),
    ('Compliance/Regulatory Cost', 'Additional cost for audit, security, compliance'),
    ('Switching/Exit Cost', 'Estimated cost to transition away from application/service'),
    ('ROI vs Peer Systems', 'Relative ROI compared to comparable platforms'),
    ('Risk Exposure for Redundancy', 'Score detailing risk if redundant system not addressed'),
]

# Example systems/apps for analysis
applications = ['Office 365', 'Canvas LMS', 'Zoom', 'Blackboard', 'Cisco WebEx', 'Google Workspace', 'Slack']
np.random.seed(88)
cost_example_data = []
for metric, description in cost_metrics:
    for app in applications:
        if 'Cost' in metric or 'Loss' in metric or 'Switching' in metric:
            value = f"${np.random.randint(12000,150000):,}"
        elif 'Rate' in metric or 'Utilization' in metric:
            value = f"{np.round(np.random.uniform(45,99),1)}%"
        elif 'Index' in metric:
            value = np.round(np.random.uniform(0.3,1.0),2)
        elif 'Redundancy' in metric or 'Duplicate' in metric:
            value = np.random.choice([0,1]) if 'Index' in metric else np.random.choice(['True','False'])
        elif 'Potential' in metric:
            value = np.random.choice(['Yes','No'])
        elif 'ROI' in metric:
            value = f"{np.round(np.random.uniform(0.7,1.4),2)}"
        elif 'Risk' in metric:
            value = np.round(np.random.uniform(2.0,7.0),2)
        else:
            value = 'N/A'
        cost_example_data.append((app, metric, description, value))

cost_dashboard_df = pd.DataFrame(cost_example_data, columns=['Application','Metric','Description','Example'])
cost_dashboard_df.to_csv('app_cost_analysis_dashboard_examples.csv', index=False)
print('Application/service total cost metrics CSV with examples saved.')

# Optional module template
script_cost = '''\n# Application Total Cost Analysis Metrics\ncost_metric_definitions = [\n    { 'metric': 'Total Cost of Ownership (TCO)', 'description': 'Sum of all costs over lifecycle' },\n    { 'metric': 'Utilization Rate (%)', 'description': 'Percent of seats/features in use' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\n# Example application cost records\ncost_records = [\n    ('Office 365', 'Total Cost of Ownership (TCO)', '$85,200'),\n    ('Slack', 'Redundancy Index', 0.79),\n]\n\ndf_cost = pd.DataFrame(cost_records, columns=['Application','Metric','Value'])\n\n# Flag systems with low utilization or high redundancy\ndef flag_redundant_systems(df):\n    rst = df[(df['Metric'] == 'Utilization Rate (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 60)]\n    red = df[(df['Metric'] == 'Redundancy Index') & (df['Value'] > 0.5)]\n    return pd.concat([rst,red])\n# Usage\nrepeats = flag_redundant_systems(df_cost)\nprint(repeats)\n'''
with open('app_cost_analysis_metrics_module.py', 'w') as f:
    f.write(script_cost)
print('Total cost analysis metrics module Python script saved.')