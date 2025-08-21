
# Vendor Metrics Module
vendor_metric_definitions = [
    { 'metric': 'Vendor Satisfaction Score', 'description': 'Average stakeholder satisfaction rating (1-5)' },
    { 'metric': 'SLA Compliance', 'description': 'Percent SLAs met' },
    # ... continued for all metrics ...
]

import pandas as pd

# Example vendor data
vendor_metrics_records = [
    ('Microsoft', 'Vendor Satisfaction Score', 4.4),
    ('Adobe', 'SLA Compliance', '98%'),
]

df_vendor = pd.DataFrame(vendor_metrics_records, columns=['Vendor','Metric','Value'])

# Dashboard alert: flag vendors with <4.0 satisfaction or <95% SLA
def flag_vendors(df):
    return df[(df['Metric'] == 'Vendor Satisfaction Score') & (df['Value'] < 4.0)]

# Usage example
bad_vendors = flag_vendors(df_vendor)
print(bad_vendors)
