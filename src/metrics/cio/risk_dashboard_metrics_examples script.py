import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Define comprehensive risk metrics for a risk management dashboard
risk_metrics = [
    ('Risk Exposure Level', 'Severity × Probability aggregate across all risks'),
    ('Risk Heat Map Category', 'Risk classified as Low/Medium/High/Critical'),
    ('Number of Active Risks', 'Total issues currently open'),
    ('Risk Severity Distribution', 'Count of risks by criticality'),
    ('Risk Trend Over Time', 'Change in risk count/severity over the last quarter'),
    ('Risk by Project', 'Total issues open per project'),
    ('Risk Response Status', 'Mitigation stage: Open/In Progress/Resolved'),
    ('Time to Risk Closure (days)', 'Average days to close risk'),
    ('Mitigation Progress', 'Percent risks resolved out of total identified'),
    ('Control Effectiveness', 'Score/percent of mitigations successfully preventing recurrence'),
    ('Residual Risk Level', 'Current risk after mitigations apply'),
    ('Incident Response Time (hours)', 'Average time to respond to new/incidents'),
    ('Escalated Risk Count', 'Number of issues escalated to executive oversight'),
    ('Compliance Adherence (%)', 'Percent of projects meeting regulatory standards'),
    ('Financial Impact Estimate ($)', 'Estimated dollar cost if risk occurs'),
    ('Risk Owner Activity', 'Score or count of mitigations closed by owner'),
    ('Project Milestone Risk Mapping', 'Link of risk to milestone, e.g., Implementation/Go-Live'),
    ('Risks by Project Phase', 'Open issues per phase (planning, execution, closing)'),
    ('Risk Mitigation Effectiveness (%)', 'Change in risk exposure after intervention'),
    ('KRI (Key Risk Indicator)', 'Leading metric such as incident frequency or cost overruns'),
    ('Risk Register Update Frequency', 'Days/weeks since last update'),
    ('Stakeholder Risk Satisfaction', 'Avg survey rating on confidence in controls'),
]

# Example dataset for demonstration purposes
example_projects = ['Student Portal Upgrade', 'Cybersecurity Enhancement', 'Cloud Migration', 'Network Infrastructure']
np.random.seed(42)
example_data = []
for metric, description in risk_metrics:
    for project in example_projects:
        example = None
        # Create tailored example values for each metric
        if 'Heat Map' in metric:
            example = np.random.choice(['Low', 'Medium', 'High', 'Critical'])
        elif 'Level' in metric or 'Severity' in metric or 'Residual' in metric:
            example = np.random.randint(1, 10)
        elif 'Number' in metric or 'Count' in metric:
            example = np.random.randint(0, 8)
        elif 'Risk Trend' in metric:
            example = f"+{np.random.randint(1,5)} in last 90 days"
        elif 'Response Status' in metric or 'Mitigation Progress' in metric:
            example = np.random.choice(['Open', 'In Progress', 'Resolved'])
        elif 'Time' in metric:
            example = np.random.randint(1,50)
        elif 'Effectiveness' in metric or 'Compliance' in metric or 'Satisfaction' in metric:
            example = f"{np.random.randint(70,100)}%"
        elif 'Financial Impact' in metric:
            example = f"${np.random.randint(1000,50000):,}"
        elif 'Owner' in metric:
            example = np.random.randint(1,7)
        elif 'Mapping' in metric:
            example = np.random.choice(['Initiation', 'Design', 'Development', 'Go-Live'])
        elif 'Risks by Project Phase' in metric:
            example = np.random.randint(0,5)
        elif 'KRI' in metric:
            example = np.random.choice(['Incident Rate High', 'Cost Overrun', 'High Usage Alerts'])
        elif 'Register' in metric:
            example = f"{np.random.randint(1,14)} days ago"
        else:
            example = 'N/A'
        example_data.append((project, metric, description, example))

risk_dashboard_df = pd.DataFrame(example_data, columns=['Project','Metric','Description','Example'])
risk_dashboard_df.to_csv('risk_dashboard_metrics_examples.csv', index=False)
print('Risk management metrics CSV with examples saved.')

# (Optional) Generate Python script for integration
script = '''\n# Risk Management Metrics Module\nrisk_metric_definitions = [\n    { \'metric\': \'Risk Exposure Level\', \'description\': \'Severity × Probability aggregate across all risks\' },\n    { \'metric\': \'Risk Heat Map Category\', \'description\': \'Risk classified as Low/Medium/High/Critical\' },\n    # ... continued for all metrics ...\n]\n\n# Example risk data per project\nrisk_dashboard_records = [\n    # project, metric, value\n    (\'Student Portal Upgrade\', \'Risk Exposure Level\', 6),\n    (\'Cybersecurity Enhancement\', \'Risk Exposure Level\', 9),\n]\n\n# DataFrame construction\nimport pandas as pd\ndf_risk = pd.DataFrame(risk_dashboard_records, columns=[\'Project\', \'Metric\', \'Value\'])\n\n# Dashboard logic: filter, alert, calculate\ndef highlight_high_risk(df):\n    return df[df[\'Value\'] >= 8]\n\n# Usage example\nhigh_risks = highlight_high_risk(df_risk)\nprint(high_risks)\n'''
with open('risk_metrics_module.py', 'w') as f:
    f.write(script)
print('Python script for risk management metrics module saved.')