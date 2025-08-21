
# System Utilization & License Metrics Module
ut_metric_definitions = [
    { 'metric': 'Utilization Rate (%)', 'description': 'Active Users / Licensed Seats' },
    { 'metric': 'Unused Licenses', 'description': 'Licensed seats remaining unused' },
    # ... continued for all metrics ...
]

import pandas as pd

# Example utilization records
ut_records = [
    ('Office 365', 'Utilization Rate (%)', '94.2%'),
    ('Zoom', 'Unused Licenses', 40),
]

df_util = pd.DataFrame(ut_records, columns=['System','Metric','Value'])

# Flag underutilized systems
def flag_low_utilization(df):
    return df[(df['Metric'] == 'Utilization Rate (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 70)]

# Usage example
low_util = flag_low_utilization(df_util)
print(low_util)
