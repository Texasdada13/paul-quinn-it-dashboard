import pandas as pd
import numpy as np

# Define metrics for digital transformation and online/hybrid learning capabilities
transformation_metrics = [
    ('Digital Transformation Maturity', 'Stage of transformation: Ad hoc, Basic, Established, Leading'),
    ('Online Learning Adoption Rate', 'Percent of courses/programs delivered online or hybrid'),
    ('Student Participation In Digital Learning (%)', 'Percent of enrolled students actively participating'),
    ('Faculty Participation In Digital Learning (%)', 'Percent of faculty involved in online/hybrid delivery'),
    ('Technology Platform Utilization', 'Frequency/percentage usage of key EdTech platforms'),
    ('Digital Literacy Index - Students', 'Average score assessing student technology readiness'),
    ('Digital Literacy Index - Faculty', 'Average score assessing faculty readiness'),
    ('Content Accessibility Compliance', 'Percent of digital content meeting accessibility (ADA, WCAG) standards'),
    ('Online Program Completion Rate (%)', 'Percent of students completing digital/hybrid programs'),
    ('Student Success Metrics in Digital Courses', 'Comparison of performance in online vs in-person courses'),
    ('Satisfaction With Digital Learning', 'Student/faculty satisfaction survey score (1-5 scale)'),
    ('EdTech Support Ticket Resolution', 'Average time to resolve support requests for digital platforms'),
    ('Virtual Engagement Rate', 'Student participation in virtual office hours/events'),
    ('Remote Faculty/Staff Enablement', 'Percent of faculty/staff with full remote access to systems'),
    ('Innovation Milestone Achievements', 'Count or completion rate of major digital transformation milestones'),
    ('Budget Allocation For Digital Initiatives (%)', 'Proportion of IT/academic budget for transformation'),
    ('Digital Credential/Certificate Volume', 'Total digital credentials/certificates issued annually'),
]

# Example initiatives/projects for tracking
initiatives = ['Online BA in Psychology', 'Hybrid MBA', 'Virtual STEM Labs', 'AI Tutoring Platform', 'Learning Analytics Implementation']
np.random.seed(31)
digital_example_data = []
for metric, description in transformation_metrics:
    for initiative in initiatives:
        if 'Maturity' in metric:
            value = np.random.choice(['Ad hoc', 'Basic', 'Established', 'Leading'])
        elif 'Rate' in metric or 'Participation' in metric or 'Completion' in metric or 'Engagement' in metric or 'Enablement' in metric or 'Allocation' in metric:
            value = f"{np.round(np.random.uniform(40,95),1)}%"
        elif 'Utilization' in metric:
            value = f"{np.round(np.random.uniform(50,99),1)}% utilization"
        elif 'Index' in metric or 'Satisfaction' in metric:
            value = np.round(np.random.uniform(3.0, 4.8), 1)
        elif 'Compliance' in metric:
            value = f"{np.random.randint(85,100)}% ADA/Section508"
        elif 'Success Metrics' in metric:
            value = f"Online GPA: {np.round(np.random.uniform(2.5,3.7),2)} vs In-person: {np.round(np.random.uniform(2.5,3.7),2)}"
        elif 'Resolution' in metric:
            value = f"{np.random.randint(1,24)} hours"
        elif 'Milestone' in metric:
            value = f"{np.random.randint(1,6)} milestones completed"
        elif 'Volume' in metric:
            value = np.random.randint(100,900)
        else:
            value = 'N/A'
        digital_example_data.append((initiative, metric, description, value))

digital_dashboard_df = pd.DataFrame(digital_example_data, columns=['Initiative','Metric','Description','Example'])
digital_dashboard_df.to_csv('digital_transformation_dashboard_examples.csv', index=False)
print('Digital transformation progress metrics CSV with examples saved.')

# Optional python module template for integration
script_digital = '''\n# Digital Transformation Metrics Module\ndigital_metric_definitions = [\n    { 'metric': 'Digital Transformation Maturity', 'description': 'Stage of transformation' },\n    { 'metric': 'Online Learning Adoption Rate', 'description': 'Percent of courses offered online/hybrid' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\n# Example digital progress data\ndigital_records = [\n    ('Online BA in Psychology', 'Online Learning Adoption Rate', '88%'),\n    ('AI Tutoring Platform', 'Satisfaction With Digital Learning', 4.7),\n]\n\ndf_digital = pd.DataFrame(digital_records, columns=['Initiative','Metric','Value'])\n\n# Dashboard alert: flag initiatives with <60% adoption or <3.5 satisfaction\ndef flag_low_progress(df):\n    # For adoption rate, strip '%' safely
    low_adopt = df[(df['Metric'] == 'Online Learning Adoption Rate') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 60)]\n    low_satis = df[(df['Metric'] == 'Satisfaction With Digital Learning') & (df['Value'] < 3.5)]\n    return pd.concat([low_adopt,low_satis])
\n# Usage example\nissues = flag_low_progress(df_digital)\nprint(issues)\n'''
with open('digital_transformation_metrics_module.py', 'w') as f:
    f.write(script_digital)
print('Digital transformation metrics module Python script saved.')