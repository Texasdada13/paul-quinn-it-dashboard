import pandas as pd
import numpy as np

# HBCU-Specific: Cost per student served, efficiency for underserved populations
cost_eff_metrics = [
    ('Metric', 'Description', 'Example'),
    ('Total Student Service Cost', 'All instructional, support, administrative spend in year', '$47,700,000'),
    ('Enrolled Undergraduate Students', 'Total undergrad enrolled (annual)', 5_800),
    ('Enrolled Pell Eligible Students', 'Underserved/low-income count (annual)', 1_720),
    ('Cost Per Student Served', 'Total service cost ÷ total enrolled', '$8,224'),
    ('Cost Per Pell Student Served', 'Total service cost ÷ Pell-eligible enrolled', '$27,734'),
    ('Cost Per Degree Conferred', 'Total spend ÷ degrees conferred', '$64,000'),
    ('Instructional Cost Per Student', 'Instructional spend ÷ enrolled', '$5,730'),
    ('Student Support Services Cost Per Student', 'Student affairs/support ÷ enrolled', '$1,960'),
    ('IT Services Cost Per Student', 'IT spend ÷ enrolled', '$510'),
    ('Library Services Cost Per Student', 'Library services ÷ enrolled', '$210'),
    ('Academic Affairs Cost Per URM Student', 'Targeted spend on URM populations', '$3,980'),
    ('Efficiency Ratio (Instructional)', 'Instructional cost ÷ total cost', '0.66'),
    ('Efficiency Ratio (Support)', 'Support cost ÷ total cost', '0.24'),
    ('Efficiency Ratio (IT)', 'IT cost ÷ total cost', '0.011'),
    ('Year-over-Year Per Student Cost Trend', 'Annual delta in cost per student served', '+2.1%'),
    ('Benchmark Comparison Per Student Cost', 'HBCU vs peer per student cost', 'HBCU: $8,224, Peer: $13,650'),
    ('Cost-to-Outcome Ratio', 'Spend per successful degree, placement, or graduation', '$70,100'),
    ('First Generation Student Support Cost Ratio', 'First-gen specific support spend ratios', '0.15'),
    ('Student Satisfaction With Services', 'Survey score: support effectiveness (1-10)', '8.7'),
]

cost_eff_df = pd.DataFrame(cost_eff_metrics[1:], columns=cost_eff_metrics[0])
cost_eff_df.to_csv('hbcu_cost_per_student_served_examples.csv', index=False)
print('HBCU cost per student served metrics CSV with examples saved.')

# Optional python module for integration
script_costeff = '''\n# HBCU Cost per Student Served Metrics Module\ncosteff_metric_definitions = [\n    { 'metric': 'Cost Per Student Served', 'description': 'Total service cost ÷ enrolled' },\n    { 'metric': 'Benchmark Comparison Per Student Cost', 'description': 'HBCU vs peer institution comparison' },\n    # ... continued ...\n]\n\nimport pandas as pd\n\ncosteff_records = [\n    ('Cost Per Student Served', '$8,224'),\n    ('Benchmark Comparison Per Student Cost', 'HBCU: $8,224, Peer: $13,650'),\n]\n\ndf_costeff = pd.DataFrame(costeff_records, columns=['Metric','Value'])\n\n# Flag low/high efficiency or cost outliers\ndef flag_efficiency_gaps(df):\n    costval = df.loc[df['Metric'] == 'Cost Per Student Served', 'Value'].str.replace('$','').str.replace(',','').astype(float)
    bench = df.loc[df['Metric'] == 'Benchmark Comparison Per Student Cost', 'Value'].str.extract(r'HBCU: ([\d,]+)')[0].str.replace(',','').astype(float)
    peer = df.loc[df['Metric'] == 'Benchmark Comparison Per Student Cost', 'Value'].str.extract(r'Peer: ([\d,]+)')[0].str.replace(',','').astype(float)
    gap = peer - bench
    gap_flag = (gap > 3000)
    cost_flag = (costval > 12000)
    outlier = df.loc[cost_flag | gap_flag]
    return outlier\n# Usage\noutlier_units = flag_efficiency_gaps(df_costeff)\nprint(outlier_units)\n'''
with open('hbcu_cost_efficiency_metrics_module.py', 'w') as f:
    f.write(script_costeff)
print('HBCU cost efficiency metrics module Python script saved.')