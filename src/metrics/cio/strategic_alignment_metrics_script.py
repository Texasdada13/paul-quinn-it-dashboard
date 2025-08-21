import pandas as pd
import numpy as np

# Define strategic alignment metrics for IT initiatives
alignment_metrics = [
    ('Strategic Alignment Score', 'Degree to which initiative aligns with institutional strategic priorities (1-10 scale)'),
    ('Mission Relevance Rating', 'How well the initiative supports core college mission (1-5 scale)'),
    ('Student Experience Impact', 'Estimated impact on student success or engagement (1-10 scale)'),
    ('Underserved Population Benefit Index', 'Relative benefit delivered specifically to underserved groups (0-1 scale)'),
    ('Equity Advancement Score', 'Degree to which initiative closes access gaps (1-10 scale)'),
    ('Learning Outcomes Improvement', 'Expected improvement in key student learning metrics (%)'),
    ('Digital Inclusion Rating', 'Extent of technology access expansion (1-5 scale)'),
    ('Retention/Uplift Projection', 'Projected increase in retention or graduation rate (%)'),
    ('Community Engagement Level', 'Score for outreach or partnership value (1-10 scale)'),
    ('Grant/Funder Mission Fit', 'Alignment with grant or funding source priorities (1-5 scale)'),
    ('Faculty/Staff Support Level', 'Stakeholder survey rating of initiative support (1-5 scale)'),
    ('Sustainability Factor', 'Initiative’s ability to deliver lasting value (1-10 scale)'),
    ('Accessibility Rating', 'Extent of ADA/accessibility compliance (1-5 scale)'),
    ('Holistic Support Integration', 'Quality of wraparound/holistic support services enabled (1-10 scale)'),
    ('Cost per Student Benefited', 'Operational cost divided by impacted student count ($)'),
]

# Example data for several IT initiatives
initiatives = ['Student Portal Upgrade', 'AI Tutoring', 'LMS Modernization', 'Mobile App Development', 'Library Digital Access']
np.random.seed(27)
alignment_example_data = []
for metric, description in alignment_metrics:
    for initiative in initiatives:
        if 'Score' in metric:
            value = np.round(np.random.uniform(6.0, 10.0), 1)
        elif 'Rating' in metric or 'Fit' in metric or 'Support' in metric or 'Accessibility' in metric:
            value = np.round(np.random.uniform(3.0, 5.0), 1)
        elif 'Impact' in metric or 'Advancement' in metric or 'Community' in metric or 'Sustainability' in metric or 'Integration' in metric:
            value = np.round(np.random.uniform(5.0, 10.0), 1)
        elif 'Benefit Index' in metric:
            value = np.round(np.random.uniform(0.3, 1.0), 2)
        elif 'Improvement' in metric or 'Projection' in metric:
            value = np.round(np.random.uniform(0, 10), 1)
        elif 'Cost' in metric:
            value = f"${np.random.randint(30,200)}"
        else:
            value = 'N/A'
        alignment_example_data.append((initiative, metric, description, value))

alignment_dashboard_df = pd.DataFrame(alignment_example_data, columns=['Initiative','Metric','Description','Example'])
alignment_dashboard_df.to_csv('strategic_alignment_dashboard_examples.csv', index=False)
print('Strategic alignment indicators CSV with examples saved.')

# Optional Python module example
script_alignment = '''\n# Strategic Alignment Metrics Module\nalignment_metric_definitions = [\n    { 'metric': 'Strategic Alignment Score', 'description': 'Degree of strategic priority alignment' },\n    { 'metric': 'Student Experience Impact', 'description': 'Effect on student success metrics' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\n# Example strategic alignment records\nalignment_records = [\n    ('Student Portal Upgrade', 'Strategic Alignment Score', 9.2),\n    ('AI Tutoring', 'Underserved Population Benefit Index', 0.92),\n]\n\ndf_alignment = pd.DataFrame(alignment_records, columns=['Initiative','Metric','Value'])\n\n# Flag initiatives with low alignment or low equity advancement\ndef flag_low_alignment(df):\n    return df[(df['Metric'] == 'Strategic Alignment Score') & (df['Value'] < 7.0)]\n\n# Usage example\nlow_align = flag_low_alignment(df_alignment)\nprint(low_align)\n'''
with open('strategic_alignment_metrics_module.py', 'w') as f:
    f.write(script_alignment)
print('Strategic alignment metrics module Python script saved.')