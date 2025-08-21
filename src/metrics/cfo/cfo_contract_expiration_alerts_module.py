
# CFO Contract Expiration Alerts Module
import pandas as pd
def flag_expiring_contracts(df,date_today=pd.Timestamp('2025-08-19'),alert_days=90):
    expiring = df[(df['Expiration Alert']=='Yes') | (df['Negotiation Recommended']=='Yes')]
    return expiring
