import pandas as pd
import numpy as np

# HBCU-Specific: Student Success ROI metrics for technology impact
roi_metrics = [
    ('Metric', 'Description', 'Example'),
    ('Technology-Linked Graduation Rate', 'Percent of students graduating who used targeted technology interventions', '78%'),
    ('Technology-Linked Retention Rate', 'Percent of students retained one year after technology adoption', '87%'),
    ('Economic Mobility Index', 'Percent increase in job, wage, or graduate study attainment after technology/program', '23% increase over 3 years'),
    ('Student Engagement Index', 'Survey or activity score (1-10) reflecting engagement with campus technologies', '8.6'),
    ('Digital Literacy Test Improvement', 'Percent improvement in digital skills after program/rollout', '36%'),
    ('GPA Change (Tech-enabled courses)', 'Mean GPA change in courses with tech integration', '+0.17 GPA points'),
    ('Faculty Adoption Rate', 'Percent of faculty incorporating digital/tech tools in the classroom', '93%'),
    ('Tech Intervention Cost per Graduate', 'All program spend ÷ number of technology-enabled graduates', '$2,450'),
    ('Program Completion Rate', 'Percent of students completing tech-enabled certificate or degree', '81%'),
    ('Job/Internship Placement Rate', 'Percent graduates placed in jobs or internships facilitated by campus technology', '74%'),
    ('Graduate Study Matriculation Rate', 'Percent entering grad school after tech-driven undergrad experience', '22%'),
    ('Post-grad Earnings Increase', 'Dollar wage increase contributed to tech/facilities', '$9,200 increase'),
    ('Minority/URM Student Tech Support Utilization', 'Percent URM/minority students using campus tech support', '68%'),
    ('Pell/Low-income Student Completion Rate', 'Tech-enabled graduation/retention for Pell/low-income', '66%'),
]

roi_df = pd.DataFrame(roi_metrics[1:], columns=roi_metrics[0])
roi_df.to_csv('hbcu_student_success_roi_examples.csv', index=False)
print('HBCU student success ROI metrics CSV with examples saved.')

# Optional python module/template
script_roi = '''\n# HBCU Student Success ROI Metrics Module\nroi_metric_definitions = [\n    { 'metric': 'Graduation Rate', 'description': 'Percent students graduating after tech adoption' },\n    { 'metric': 'Economic Mobility Index', 'description': 'Earnings/wage growth post graduation' },\n    # ... continued ...\n]\n\nimport pandas as pd\n\nroi_records = [\n    ('Technology-Linked Graduation Rate', '78%'),\n    ('Economic Mobility Index', '23% increase over 3 years'),\n]\n\ndf_roi = pd.DataFrame(roi_records, columns=['Metric','Value'])\n\n# Flag low ROI or tech engagement\ndef flag_low_success(df):\n    grad = df.loc[df['Metric'] == 'Technology-Linked Graduation Rate', 'Value'].str.replace('%','').astype(float)
    mobility = df.loc[df['Metric'] == 'Economic Mobility Index', 'Value'].str.extract(r'(\d+)')[0].astype(float)
    grad_issues = df.loc[grad < 70]
    mobility_issues = df.loc[mobility < 10]
    return pd.concat([grad_issues,mobility_issues])\n# Usage\nissues = flag_low_success(df_roi)\nprint(issues)\n'''
with open('hbcu_student_success_roi_module.py', 'w') as f:
    f.write(script_roi)
print('HBCU student success ROI metrics module Python script saved.')