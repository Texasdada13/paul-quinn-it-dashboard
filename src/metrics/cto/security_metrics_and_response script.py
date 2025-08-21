import pandas as pd
import numpy as np

# CTO Metrics: Security metrics, vulnerability assessments, incident response times
security_metrics = [
    ('Asset/System', 'System, application, or device being tracked'),
    ('Open Vulnerabilities Count', 'Active, unresolved security vulnerabilities'),
    ('Critical Vulnerabilities %', 'Share of open vulnerabilities rated as critical or high'),
    ('Average Vulnerability Age (days)', 'Mean age of current open vulnerabilities'),
    ('Patch Compliance Rate (%)', 'Percent of risky vulnerabilities remediated within SLA'),
    ('Number of Security Incidents', 'Detected breaches, malware, or suspicious events per period'),
    ('Mean Time to Detect (MTTD)', 'Average hours or days to discover new incident'),
    ('Mean Time to Respond (MTTR)', 'Average hours to contain or remediate incident'),
    ('Incident Escalation Rate', 'Percent incidents requiring executive/third-party involvement'),
    ('User Account Compromises', 'Count per period'),
    ('Phishing/Social Eng. Reports', 'User-reported phishing or social engineering events'),
    ('Failed Login Attempts', 'Number per system per week or month'),
    ('Policy Violation Rate', 'Percent systems/users violating security policy'),
    ('Endpoint Protection Coverage', 'Percent of endpoints with active/updated protection'),
    ('Security Training Completion Rate', 'Percent users completed training this cycle'),
    ('False Positive Alert Rate', 'Percent of alerts determined as non-issues'),
    ('Penetration Test Success Rate', 'Percent of pen-test findings addressed in-time'),
    ('Regulatory Compliance Score', 'Audited or self-reported alignment with key controls'),
]

security_assets = ['Core Network', 'Email Suite', 'ERP System', 'Website', 'Student Portal', 'Cloud Servers', 'Campus WiFi']
np.random.seed(15)
security_example_data = []
for metric, description in security_metrics:
    for asset in security_assets:
        if 'Count' in metric or 'Attempts' in metric or 'Compromises' in metric or 'Reports' in metric or 'Events' in metric:
            value = np.random.randint(0,28)
        elif 'Rate' in metric or 'Coverage' in metric or 'Score' in metric or 'Compliance' in metric or 'Percent' in metric:
            value = f"{np.round(np.random.uniform(65,100),1)}%"
        elif 'Age' in metric or 'MTTD' in metric or 'MTTR' in metric:
            value = np.round(np.random.uniform(2,72),1)
        else:
            value = 'N/A'
        security_example_data.append((asset, metric, description, value))

security_dashboard_df = pd.DataFrame(security_example_data, columns=['Asset','Metric','Description','Example'])
security_dashboard_df.to_csv('security_metrics_dashboard_examples.csv', index=False)
print('Security metrics, vulnerability, and incident response metrics CSV with examples saved.')

# Optional python module template
script_security = '''\n# Security Metrics & Incident Response Module\nsecurity_metric_definitions = [\n    { 'metric': 'Open Vulnerabilities Count', 'description': 'Unresolved security threats' },\n    { 'metric': 'Mean Time to Respond (MTTR)', 'description': 'Hours to containment/remediation' },\n    # ... continued ...\n]\n\nimport pandas as pd\n\nsecurity_records = [\n    ('ERP System', 'Open Vulnerabilities Count', 7),\n    ('Email Suite', 'Mean Time to Respond (MTTR)', 18.2),\n]\n\ndf_security = pd.DataFrame(security_records, columns=['Asset','Metric','Value'])\n\n# Dashboard logic: flag high-severity, slow response, or low coverage \ndef flag_security_issues(df):\n    critical_vuln = df[(df['Metric'] == 'Critical Vulnerabilities %') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) > 25)]\n    slow_mttr = df[(df['Metric'] == 'Mean Time to Respond (MTTR)') & (df['Value'] > 24)]\n    incomplete_cov = df[(df['Metric'] == 'Endpoint Protection Coverage') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 85)]\n    return pd.concat([critical_vuln,slow_mttr,incomplete_cov])\n# Usage\nissues = flag_security_issues(df_security)\nprint(issues)\n'''
with open('security_metrics_and_response_module.py', 'w') as f:
    f.write(script_security)
print('Security metrics and response module Python script saved.')