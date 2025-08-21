
# CFO Peer HBCU Benchmarking Module
import pandas as pd
def flag_benchmark_for_board(df):
    # DataFrame must have 'PQ Delta to Peer (%)' and 'Budget Justification Flag'
    overages = df[(df['Budget Justification Flag']=='Yes') & (df['PQ Delta to Peer (%)']>10)]
    shortages = df[(df['Budget Justification Flag']=='Yes') & (df['PQ Delta to Peer (%)']<-10)]
    return pd.concat([overages,shortages])
