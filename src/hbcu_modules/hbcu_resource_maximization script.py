import pandas as pd
import numpy as np

# HBCU-Specific: Resource Maximization & Instructional Spending
hbcu_metrics = [
    ('Metric', 'Description', 'Example'),
    ('Instructional Spending Ratio', 'Instruction spend ÷ total revenue (by sector/HBCU vs private)', 'HBCU: 1.20, Private NP: 0.78'),
    ('Cost Per Student Served', 'Total operational cost ÷ number of enrolled students', '$8,100'),
    ('Student Success ROI (Instruction)', 'Improvement in graduation/employment ÷ instructional cost per FTE', '6.1% graduation increase/$10,000 spend'),
    ('Grant Compliance Score', 'Percent of grant dollars in compliance/active/eligible projects', '99%'),
    ('Federal/State Funding Ratio', 'Proportion of revenue from government sources versus tuition/other', '72% government'),
    ('Academic vs. Admin Spend Ratio', 'Academic/Instruction spend ÷ administrative/support spend', 'Academic: $20M, Admin: $10M (2.0)'),
    ('Cost Per Degree Awarded', 'Total annual cost ÷ number of degrees conferred', '$62,500'),
    ('Mission Alignment Index', 'Degree to which budget/investments align with HBCU equity/mission goals', '8.9/10'),
    ('Peer Benchmark (Instructional %)', 'Percent of budget spent on instruction vs sector median/peer HBCUs', 'HBCU: 57%, Peer: 41%'),
    ('1st Gen/Low-income Student Cost Efficiency', 'Instructional/total spend per Pell, 1st Gen, and/or low-income student', '$6,500 per Pell recipient'),
    ('Grant/Donor Reporting Timeliness', 'Percent reports/filings submitted on/before due date', '95% on time'),
    ('Faculty FTE/Student Ratio', 'Full-time instructional staff per enrolled FTE student', '1:16'),
    ('Instructional Spend Trend (5y)', 'Change in instructional dollars per student/full time equivalent over five years', '+4.2% annually'),
]

hbcu_df = pd.DataFrame(hbcu_metrics[1:], columns=hbcu_metrics[0])
hbcu_df.to_csv('hbcu_resource_maximization_examples.csv', index=False)
print('HBCU resource maximization metrics CSV with examples saved.')

# Optional python module template
script_hbcu = '''\n# HBCU Resource Maximization Metrics Module\nhbcu_metric_definitions = [\n    { 'metric': 'Instructional Spending Ratio', 'description': 'Instruction spend ÷ total revenue' },\n    { 'metric': 'Mission Alignment Index', 'description': 'Degree of equity/mission fit of spend' },\n    # ... continued ...\n]\n\nimport pandas as pd\n\nhbcu_records = [\n    ('Instructional Spending Ratio', 'HBCU: 1.20, Private NP: 0.78'),\n    ('Mission Alignment Index', 8.9),\n]\n\ndf_hbcu = pd.DataFrame(hbcu_records, columns=['Metric','Value'])\n\n# Dashboard logic: flag below-benchmark spending ratios\ndef flag_spending_issues(df):\n    below_ratio = df[(df['Metric'] == 'Instructional Spending Ratio') & (df['Value'].str.contains('HBCU')) & (df['Value'].str.extract(r'HBCU: ([0-9.]+)')[0].astype(float) < 1.0)]\n    return below_ratio\n# Usage\nissues = flag_spending_issues(df_hbcu)\nprint(issues)\n'''
with open('hbcu_resource_maximization_metrics_module.py', 'w') as f:
    f.write(script_hbcu)
print('HBCU resource maximization metrics module Python script saved.')