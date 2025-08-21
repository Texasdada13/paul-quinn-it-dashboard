
# HBCU Cost per Student Served Metrics Module
costeff_metric_definitions = [
    { 'metric': 'Cost Per Student Served', 'description': 'Total service cost ÷ enrolled' },
    { 'metric': 'Benchmark Comparison Per Student Cost', 'description': 'HBCU vs peer institution comparison' },
    # ... continued ...
]

import pandas as pd

costeff_records = [
    ('Cost Per Student Served', '$8,224'),
    ('Benchmark Comparison Per Student Cost', 'HBCU: $8,224, Peer: $13,650'),
]

df_costeff = pd.DataFrame(costeff_records, columns=['Metric','Value'])

# Flag low/high efficiency or cost outliers
def flag_efficiency_gaps(df):
    costval = df.loc[df['Metric'] == 'Cost Per Student Served', 'Value'].str.replace('$','').str.replace(',','').astype(float)
    bench = df.loc[df['Metric'] == 'Benchmark Comparison Per Student Cost', 'Value'].str.extract(r'HBCU: ([\d,]+)')[0].str.replace(',','').astype(float)
    peer = df.loc[df['Metric'] == 'Benchmark Comparison Per Student Cost', 'Value'].str.extract(r'Peer: ([\d,]+)')[0].str.replace(',','').astype(float)
    gap = peer - bench
    gap_flag = (gap > 3000)
    cost_flag = (costval > 12000)
    outlier = df.loc[cost_flag | gap_flag]
    return outlier
# Usage
outlier_units = flag_efficiency_gaps(df_costeff)
print(outlier_units)
