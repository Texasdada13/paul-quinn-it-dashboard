
# CFO IT Student Success ROI Module
import pandas as pd
def flag_roi_issues(df,min_roi=25):
    low_roi = df[df['ROI (Outcome-Driven)']<min_roi]
    missed_bench = df[(df['Outcome Rate After Investment']<df['Peer/Industry Benchmark'])]
    no_grant_ok = df[df['Grant/Funder ROI Requirement Met']=='No']
    return pd.concat([low_roi,missed_bench,no_grant_ok]).drop_duplicates()
