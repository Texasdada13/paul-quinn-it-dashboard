import pandas as pd
import numpy as np

# CTO Metrics: Technical debt tracking and remediation progress
techdebt_metrics = [
    ('Asset/Component', 'System/component with technical debt'),
    ('Technical Debt Score', 'Composite weighted metric (1-10, higher=worse)'),
    ('Outstanding Debt Items', 'Count of unresolved tech debt tasks/issues'),
    ('Debt Age (days)', 'Average age of unresolved debt'),
    ('Debt Impact Rating', 'Severity of impact on reliability/operations (Low, Medium, High, Critical)'),
    ('Code Quality Index', 'Automated code assessment score (1-10)'),
    ('Documented Remediation Roadmap', 'Is roadmap for debt resolution available? (Yes/No)'),
    ('Remediation Progress (%)', 'Percent completed of debt remediation plan'),
    ('Remediation Completion ETA (days)', 'Estimated days until debt resolved'),
    ('Dependency Risk Score', 'Risk from dependencies on outdated tech (1-10)'),
    ('System Performance Penalty (%)', 'Lost performance due to tech debt issues'),
    ('Incident Occurrences Attributable', 'Count of outages/errors caused by tech debt'),
    ('Resource Allocation to Remediation ($)', 'Budget/hours allocated to debt activities'),
    ('Root Cause Recurrence Rate (%)', 'Percent of errors re-occurring post-fix'),
    ('Stakeholder Priority Ranking', 'Rank (1=highest priority for resolution)'),
    ('Risk Acceptance Exception Flag', 'Is debt/risk formally accepted by leadership?'),
    ('Decommissioning Target Date', 'Planned date for retiring/outdated tech'),
]

components = ['Student Portal', 'Network Core', 'Old ERP System', 'Library Firewall', 'Legacy Email Server', 'Campus WiFi', 'Data Analytics Stack', 'Finance Integration']
np.random.seed(77)
techtebt_example_data = []
for metric, description in techdebt_metrics:
    for comp in components:
        if 'Score' in metric or 'Index' in metric or 'Risk' in metric:
            value = np.round(np.random.uniform(2.3,9.9),1)
        elif 'Debt Items' in metric or 'Occurrences' in metric:
            value = np.random.randint(0,18)
        elif 'Age' in metric or 'ETA' in metric:
            value = np.random.randint(7,520)
        elif 'Impact' in metric:
            value = np.random.choice(['Low','Medium','High','Critical'])
        elif 'Roadmap' in metric or 'Exception Flag' in metric:
            value = np.random.choice(['Yes','No'])
        elif 'Remediation Progress' in metric or 'Penalty' in metric or 'Root Cause' in metric:
            value = f"{np.round(np.random.uniform(0,87),1)}%"
        elif 'Resource Allocation' in metric:
            value = f"${np.random.randint(2500,72500):,}"
        elif 'Decommissioning' in metric:
            days = int(np.random.uniform(10,680))
            value = (pd.Timestamp('2025-08-19') + pd.Timedelta(days=days)).strftime('%Y-%m-%d')
        elif 'Priority' in metric:
            value = np.random.randint(1,8)
        else:
            value = 'N/A'
        techtebt_example_data.append((comp, metric, description, value))

techdebt_dashboard_df = pd.DataFrame(techtebt_example_data, columns=['Component','Metric','Description','Example'])
techdebt_dashboard_df.to_csv('technical_debt_dashboard_examples.csv', index=False)
print('Technical debt tracking metrics CSV with examples saved.')

# Optional python module template for reporting/alerting
script_techdebt = '''\n# Technical Debt Tracking & Remediation Metrics Module\ntechdebt_metric_definitions = [\n    { 'metric': 'Technical Debt Score', 'description': 'Weighted indicator of tech debt severity' },\n    { 'metric': 'Remediation Progress (%)', 'description': 'Percent completed of debt work plan' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\ntechdebt_records = [\n    ('Old ERP System', 'Technical Debt Score', 7.9),\n    ('Legacy Email Server', 'Remediation Progress (%)', '36.3%'),\n]\n\ndf_debt = pd.DataFrame(techdebt_records, columns=['Component','Metric','Value'])\n\n# Dashboard logic: flag high technical debt or slow progress\ndef flag_high_debt(df):\n    severe = df[(df['Metric'] == 'Technical Debt Score') & (df['Value'] > 7)]\n    slow_remed = df[(df['Metric'] == 'Remediation Progress (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 100) < 30)]
    critical_impact = df[(df['Metric'] == 'Debt Impact Rating') & (df['Value'] == 'Critical')]
    return pd.concat([severe,slow_remed,critical_impact])\n# Usage\nissues = flag_high_debt(df_debt)\nprint(issues)\n'''
with open('technical_debt_metrics_module.py', 'w') as f:
    f.write(script_techdebt)
print('Technical debt metrics module Python script saved.')