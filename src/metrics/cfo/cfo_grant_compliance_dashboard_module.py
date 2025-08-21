
# CFO Grant Compliance Dashboard Module
import pandas as pd
def flag_grant_compliance_issues(df, min_compliance=95):
    noncompliant = df[df['Compliance Rate (%)']<min_compliance]
    unresolved = df[(df['Compliance Issues Flag']=='Open') | (df['Corrective Actions (%)']<97)]
    past_due = df[(df['Timely Report Filing (%)']<93)]
    highrisk = df[df['Risk of Fund Clawback']!='Low']
    under_direct = df[df['Percent Used for Direct Instruction/Student']<70]
    return pd.concat([noncompliant,unresolved,past_due,highrisk,under_direct]).drop_duplicates()
