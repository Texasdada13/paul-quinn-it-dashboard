
# Business Unit IT Spend Metrics Module
unit_metric_definitions = [
    { 'metric': 'Total IT Spend', 'description': 'Total annual IT expenditures by business unit' },
    { 'metric': 'High-Cost Outlier Flag', 'description': 'Indicator for units above spend threshold' },
    # ... continued for all metrics ...
]

import pandas as pd

# Example business unit IT spend data
unit_records = [
    ('IT Operations', 'Total IT Spend', '$425,000'),
    ('Academic Affairs', 'High-Cost Outlier Flag', 'Yes'),
]

df_unit = pd.DataFrame(unit_records, columns=['Business_Unit','Metric','Value'])

# Flag high-cost outlier units
def flag_high_cost_units(df):
    return df[(df['Metric'] == 'High-Cost Outlier Flag') & (df['Value'] == 'Yes')]

# Usage
high_costs = flag_high_cost_units(df_unit)
print(high_costs)
