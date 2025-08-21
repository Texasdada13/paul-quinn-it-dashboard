import pandas as pd
import numpy as np

# CTO Metrics: System utilization rates and license optimization
utilization_metrics = [
    ('Total Licensed Seats', 'Number of paid licenses/seats provisioned for system'),
    ('Active Users', 'Count of active users in the current month/period'),
    ('Utilization Rate (%)', 'Active Users ÷ Total Licensed Seats × 100'),
    ('Peak Utilization Rate (%)', 'Peak active users ÷ licensed seats × 100'),
    ('Unused Licenses', 'Licensed seats minus active users'),
    ('Unused License Cost', 'Cost for unused licenses this period'),
    ('Cost per Active User', 'Total license cost ÷ current active users'),
    ('License Renewal Date', 'Next contract renewal date per system'),
    ('License Expiry Alert', 'Flag if renewal within 90 days'),
    ('License Type Breakdown', 'Count by user level: faculty, staff, student'),
    ('Feature Usage Index', 'Percent of features used vs. available in system'),
    ('Overlapping Licenses Flag', 'Boolean if system duplicates other solutions'),
    ('License Compliance Rate', 'Percent of users properly licensed vs. in violation'),
    ('Growth Trend in Usage (%)', 'Month-over-month percent change in active users'),
    ('User Satisfaction Score', 'Survey score for system effectiveness (1-5 scale)'),
]

systems = ['Office 365', 'Canvas LMS', 'Zoom', 'Blackboard', 'Cisco WebEx', 'Tableau', 'AWS Cloud']
np.random.seed(64)
utilization_example_data = []
for metric, description in utilization_metrics:
    for system in systems:
        if 'Seats' in metric:
            value = np.random.randint(200,1050)
        elif 'Users' in metric:
            value = np.random.randint(150,950)
        elif 'Rate' in metric or 'Index' in metric or 'Trend' in metric:
            value = f"{np.round(np.random.uniform(45,99),1)}%"
        elif 'Unused' in metric or 'Overlap' in metric:
            value = np.random.randint(0, 250) if 'Licenses' in metric else np.random.choice(['True','False'])
        elif 'Cost' in metric:
            value = f"${np.random.randint(5000,68000):,}"
        elif 'Date' in metric:
            value = pd.Timestamp('2025-08-19') + pd.Timedelta(days=int(np.random.uniform(1,365)))
            value = value.strftime('%Y-%m-%d')
        elif 'Alert' in metric:
            value = np.random.choice(['Yes','No'])
        elif 'Breakdown' in metric:
            value = f"Faculty: {np.random.randint(10,80)}, Staff: {np.random.randint(10,60)}, Student: {np.random.randint(120,900)}"
        elif 'Compliance' in metric:
            value = f"{np.round(np.random.uniform(90,100),1)}%"
        elif 'Satisfaction' in metric:
            value = np.round(np.random.uniform(3.5,4.8), 1)
        else:
            value = 'N/A'
        utilization_example_data.append((system, metric, description, value))

utilization_dashboard_df = pd.DataFrame(utilization_example_data, columns=['System','Metric','Description','Example'])
utilization_dashboard_df.to_csv('system_utilization_dashboard_examples.csv', index=False)
print('System utilization and license optimization metrics CSV with examples saved.')

# Optional module template
script_utilization = '''\n# System Utilization & License Metrics Module\nut_metric_definitions = [\n    { 'metric': 'Utilization Rate (%)', 'description': 'Active Users / Licensed Seats' },\n    { 'metric': 'Unused Licenses', 'description': 'Licensed seats remaining unused' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\n# Example utilization records\nut_records = [\n    ('Office 365', 'Utilization Rate (%)', '94.2%'),\n    ('Zoom', 'Unused Licenses', 40),\n]\n\ndf_util = pd.DataFrame(ut_records, columns=['System','Metric','Value'])\n\n# Flag underutilized systems\ndef flag_low_utilization(df):\n    return df[(df['Metric'] == 'Utilization Rate (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 70)]\n\n# Usage example\nlow_util = flag_low_utilization(df_util)\nprint(low_util)\n'''
with open('system_utilization_metrics_module.py', 'w') as f:
    f.write(script_utilization)
print('System utilization metrics module Python script saved.')