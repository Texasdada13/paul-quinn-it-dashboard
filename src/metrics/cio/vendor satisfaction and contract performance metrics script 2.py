import pandas as pd
import numpy as np

# Corrected - use np.round for floats
vendor_metrics = [
    ('Vendor Satisfaction Score', 'Average rating from end user, CIO, or stakeholder surveys (1-5 scale)'),
    ('Service Level Agreement (SLA) Compliance', 'Percent of time vendor met all SLAs'),
    ('Contract Renewal Rate', 'Percentage of contracts renewed versus terminated per year'),
    ('Contract Value vs Delivered Value', 'Ratio of perceived benefit or savings to cost'),
    ('Response Time to Incidents', 'Average time (in hours) for vendor to respond to support issues'),
    ('Resolution Time for Issues', 'Average days to fully resolve critical issues'),
    ('Penalty/Fee Occurrences', 'Count of penalty clauses invoked (e.g. for downtime)'),
    ('Dispute Frequency', 'Number of formal contract disputes in last year'),
    ('Innovation Contribution', 'Stakeholder rating of vendor-led innovation (1-5 scale)'),
    ('Cost Variance', 'Percent difference (actual vs. contract spend)'),
    ('Uptime/Availability (%)', 'Measured service availability vs. contract guarantee'),
    ('Contract Breach Incidents', 'Count of contract compliance failures'),
    ('Vendor Longevity', 'Years as a college vendor (relationship health)'),
    ('Discounts/Savings Realized', 'Total cost savings delivered versus expectations'),
    ('Annual Spend Growth Rate', 'Year-over-year change in vendor spend'),
    ('Compliance With College Standards', 'Audited vendor compliance to HBCU/IT standards'),
]

vendors = ['Microsoft', 'Adobe', 'AWS', 'Blackboard', 'Cisco', 'Zoom', 'Oracle', 'Salesforce']
np.random.seed(21)
vendor_example_data = []
for metric, description in vendor_metrics:
    for vendor in vendors:
        example = None
        if 'Score' in metric or 'Innovation' in metric:
            example = np.round(np.random.uniform(3.2, 4.9), 1)
        elif 'Compliance' in metric:
            example = f"{np.random.randint(85,100)}%"
        elif 'Rate' in metric:
            example = f"{np.random.randint(75,100)}%"
        elif 'Value' in metric:
            example = np.round(np.random.uniform(0.8, 1.2), 2)
        elif 'Time' in metric:
            example = np.random.randint(1,36)
        elif 'Penalty' in metric or 'Dispute' in metric or 'Breach' in metric:
            example = np.random.randint(0, 4)
        elif 'Uptime' in metric:
            example = f"{np.random.uniform(97.0, 99.99):.2f}%"
        elif 'Longevity' in metric:
            example = np.random.randint(1, 8)
        elif 'Discount' in metric:
            example = f"${np.random.randint(5000, 60000):,}"
        elif 'Growth' in metric:
            example = f"{np.round(np.random.uniform(-0.05, 0.15)*100, 1)}%"
        else:
            example = 'N/A'
        vendor_example_data.append((vendor, metric, description, example))

vendor_dashboard_df = pd.DataFrame(vendor_example_data, columns=['Vendor','Metric','Description','Example'])
vendor_dashboard_df.to_csv('vendor_dashboard_metrics_examples.csv', index=False)
print('Vendor satisfaction and contract performance metrics CSV with examples saved.')

# (Optional) Generate Python module template
script_vendor = '''\n# Vendor Metrics Module\nvendor_metric_definitions = [\n    { 'metric': 'Vendor Satisfaction Score', 'description': 'Average stakeholder satisfaction rating (1-5)' },\n    { 'metric': 'SLA Compliance', 'description': 'Percent SLAs met' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\n# Example vendor data\nvendor_metrics_records = [\n    ('Microsoft', 'Vendor Satisfaction Score', 4.4),\n    ('Adobe', 'SLA Compliance', '98%'),\n]\n\ndf_vendor = pd.DataFrame(vendor_metrics_records, columns=['Vendor','Metric','Value'])\n\n# Dashboard alert: flag vendors with <4.0 satisfaction or <95% SLA\ndef flag_vendors(df):\n    return df[(df['Metric'] == 'Vendor Satisfaction Score') & (df['Value'] < 4.0)]\n\n# Usage example\nbad_vendors = flag_vendors(df_vendor)\nprint(bad_vendors)\n'''
with open('vendor_metrics_module.py', 'w') as f:
    f.write(script_vendor)
print('Vendor metrics module Python script saved.')
