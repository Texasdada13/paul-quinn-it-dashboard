
# CFO Vendor Spend Optimization Analysis
import pandas as pd
def flag_underutilized_overlapping(df):
    # DataFrame columns: ['Vendor','Utilization Rate (%)','Overlapping Subscription Flag','Unused License Count','Potential Savings ($)']
    low_util = df[(df['Utilization Rate (%)'] < 80)]
    overlap = df[(df['Overlapping Subscription Flag']==True)]
    high_savings = df[df['Potential Savings ($)']>10000]
    return pd.concat([low_util,overlap,high_savings]).drop_duplicates()
