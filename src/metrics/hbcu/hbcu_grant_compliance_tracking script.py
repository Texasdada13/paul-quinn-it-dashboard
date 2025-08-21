import pandas as pd
import numpy as np

# HBCU-Specific: Grant compliance tracking for federal/foundation funding
compliance_metrics = [
    ('Metric', 'Description', 'Example'),
    ('Active Grant Count', 'Current number of active federal/foundation grants managed', 12),
    ('Percent Grant Allocation Used', 'Percent of budgeted grant dollars spent in cycle', '84%'),
    ('Timeliness of Grant Reporting', 'Percent of required reports submitted on time', '95%'),
    ('Compliance Rate by Grant Type', 'Percent federal/foundation grants fully compliant with terms', 'Federal: 96%, Foundation: 92%'),
    ('Unspent Grant Funds', 'Dollar value of unspent/encumbered funds by fiscal year end', '$245,000'),
    ('Grant Risk Score', 'Composite metric for risk of compliance breach by grant', 'Low/Moderate/High'),
    ('Flagged Compliance Issues', 'Number of grants with flagged issues in audits', 3),
    ('Audit Exception Rate', 'Percent of audits with material exceptions/events', '8%'),
    ('Outstanding Documentation Requests', 'Count of unresolved document/information requests', 7),
    ('Disallowed Cost Rate', 'Percent of grant costs deemed ineligible in audits', '2.6%'),
    ('Percent Staff Trained in Compliance', 'Percent project/finance staff with up-to-date compliance training', '88%'),
    ('Days to Resolution of Audit Exception', 'Average days to resolve audit exception/findings', 23),
    ('Federal Drawdown Frequency', 'Number of federal account drawdowns per fiscal year', 9),
    ('Foundation Fund Spending Adherence', 'Percent of foundation funding spent to spec/requirements', '97%'),
    ('Grant Renewal Rate', 'Percent of grants successfully renewed/extended', '71%'),
    ('Cost Allocation Accuracy Score', 'Quantitative compliance with cost allocation plans', '9.2/10'),
    ('Percent Compliance for Subgrantees', 'Percent subgrantees monitoring/compliance rate', '100%'),
    ('Percent of Grants Used for Direct Instruction', 'Percent of grant dollars supporting instructional/student-facing efforts', '62%'),
    ('Annual Compliance Training Completion', 'Percent compliance team completed training', '91%'),
    ('Grant Report Accuracy Rate', 'Percent of grant reports submitted without correction', '98%'),
    ('Grant Reporting Technology Utilization', 'Percent of grant teams using centralized system/workflow', '86%'),
]

compliance_df = pd.DataFrame(compliance_metrics[1:], columns=compliance_metrics[0])
compliance_df.to_csv('hbcu_grant_compliance_tracking_examples.csv', index=False)
print('HBCU grant compliance tracking metrics CSV with examples saved.')

# Optional python module for integration
script_compliance = '''\n# HBCU Grant Compliance Tracking Metrics Module\ncompliance_metric_definitions = [\n    { 'metric': 'Compliance Rate by Grant Type', 'description': 'Federal/foundation grants fully compliant' },\n    { 'metric': 'Audit Exception Rate', 'description': 'Percent audits with material exceptions' },\n    # ... continued ...\n]\n\nimport pandas as pd\n\ncompliance_records = [\n    ('Compliance Rate by Grant Type', 'Federal: 96%, Foundation: 92%'),\n    ('Audit Exception Rate', '8%'),\n]\n\ndf_compliance = pd.DataFrame(compliance_records, columns=['Metric','Value'])\n\n# Flag late, inaccurate, or at-risk grants\ndef flag_noncompliance(df):\n    inaccurate = df[(df['Metric'] == 'Grant Report Accuracy Rate') & (df['Value'].apply(lambda x: float(x.replace('%','')) if isinstance(x,str) else 100) < 95)]\n    exception = df[(df['Metric'] == 'Audit Exception Rate') & (df['Value'].apply(lambda x: float(x.replace('%','')) if isinstance(x,str) else 0) > 10)]\n    at_risk = df[(df['Metric'] == 'Grant Risk Score') & (df['Value'].isin(['High','Moderate']))]
    return pd.concat([inaccurate,exception,at_risk])\n# Usage\nissues = flag_noncompliance(df_compliance)\nprint(issues)\n'''
with open('hbcu_grant_compliance_metrics_module.py', 'w') as f:
    f.write(script_compliance)
print('HBCU grant compliance metrics module Python script saved.')