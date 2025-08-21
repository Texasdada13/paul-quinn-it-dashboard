
# CFO IT Spend Breakdown & Trend Module
import pandas as pd
def breakdown_by_category(df, years=[2023,2024,2025]):
    pivot = df.pivot_table(index=['Project','Vendor','Functional Area'],columns='Year',values='Spend Amount')
    return pivot
# Usage
# it_spend_breakdown_df = pd.read_csv('cfo_total_it_spend_breakdown_examples.csv')
# spend_pivot = breakdown_by_category(it_spend_breakdown_df)
