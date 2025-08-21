import pandas as pd
import numpy as np

# CTO Metrics: Technology stack health monitoring with automated alerts
stack_health_metrics = [
    ('Stack Component', 'Name of core technology / platform'),
    ('Version Deployed', 'Current software version in production'),
    ('Patch/Update Status', 'Is component patched or behind (Yes/No)'),
    ('End-of-Life Risk Flag', 'Flag for impending vendor support expiration'),
    ('Performance Health Score', 'Composite score (1-10) based on response/errors/capacity'),
    ('Recent Critical Incident Count', 'Number of P1/P2 issues in last 30-90 days'),
    ('Availability/Uptime (%)', 'Recent measured service uptime (30 days)'),
    ('Integration Dependency Count', 'Number of other systems reliant on this stack component'),
    ('Security Vulnerability Score', 'CVSS or internal weighted score (1-10)'),
    ('Automated Health Alert Status', 'Is alert triggered due to detected issues (Yes/No)'),
    ('Scalability Readiness', 'Indicator for ability to scale with demand (score)'),
    ('Resource Usage Efficiency', 'Percent of system resources efficiently utilized'),
    ('Incident Resolution SLA (%)', 'Percent resolved within SLA targets'),
    ('Known Bugs Open', 'Count of unresolved bugs/defects'),
    ('Change Volume (last 90d)', 'Number of production code/config changes'),
]

stack_components = ['PostgreSQL DB', 'Docker Platform', 'Nginx Web Proxy', 'Ubuntu Servers', 
                    'AWS S3 Storage', 'Okta SSO', 'Streamlit WebApp', 'PowerBI Connector']
np.random.seed(97)
stack_example_data = []
for metric, description in stack_health_metrics:
    for comp in stack_components:
        if 'Version' in metric:
            value = f"v{np.random.randint(1,16)}.{np.random.randint(0,10)}.{np.random.randint(0,10)}"
        elif 'Status' in metric or 'Alert' in metric or 'Flag' in metric:
            value = np.random.choice(['Yes','No'])
        elif 'Score' in metric or 'Readiness' in metric or 'Health' in metric or 'Security' in metric:
            value = np.round(np.random.uniform(4.5,9.9),1)
        elif 'Count' in metric or 'Volume' in metric or 'Bugs' in metric or 'Dependency' in metric:
            value = np.random.randint(0,18)
        elif 'Uptime' in metric or 'Efficiency' in metric or 'SLA' in metric:
            value = f"{np.round(np.random.uniform(91.5,99.95),2)}%"
        else:
            value = 'N/A'
        stack_example_data.append((comp, metric, description, value))

stack_dashboard_df = pd.DataFrame(stack_example_data, columns=['Component','Metric','Description','Example'])
stack_dashboard_df.to_csv('tech_stack_health_dashboard_examples.csv', index=False)
print('Technology stack health monitoring metrics CSV with examples saved.')

# Optional python module template
script_stack = '''\n# Technology Stack Health Monitoring Metrics Module\nstack_metric_definitions = [\n    { 'metric': 'Performance Health Score', 'description': 'Composite tech health rating (1-10)' },\n    { 'metric': 'Patch/Update Status', 'description': 'Is tech up-to-date?' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\nstack_records = [\n    ('Nginx Web Proxy', 'Performance Health Score', 8.2),\n    ('Okta SSO', 'Patch/Update Status', 'No'),\n]\n\ndf_stack = pd.DataFrame(stack_records, columns=['Component','Metric','Value'])\n\n# Dashboard alert logic: flag any with poor health (<7), overdue patch, or support risk\ndef flag_at_risk_stack(df):\n    unhealthy = df[(df['Metric'] == 'Performance Health Score') & (df['Value'] < 7)]\n    unpatched = df[(df['Metric'] == 'Patch/Update Status') & (df['Value'] == 'No')]
    eol_risk = df[(df['Metric'] == 'End-of-Life Risk Flag') & (df['Value'] == 'Yes')]
    return pd.concat([unhealthy,unpatched,eol_risk])\n# Usage\nrisk_components = flag_at_risk_stack(df_stack)\nprint(risk_components)\n'''
with open('tech_stack_health_metrics_module.py', 'w') as f:
    f.write(script_stack)
print('Technology stack health metrics module Python script saved.')