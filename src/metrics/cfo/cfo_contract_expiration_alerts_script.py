import pandas as pd
import numpy as np
from datetime import datetime

# CFO Metric: Contract Expiration Alerts for vendor renewal/renegotiation
date_today = datetime(2025, 8, 19)
alert_threshold = 90 # days for alert

contract_metrics = [
    ('Vendor', 'Supplier/name'),
    ('System/Product', 'System or service under contract'),
    ('Contract Start Date', 'Start of contract'),
    ('Contract End Date', 'End/renewal date'),
    ('Annual Spend', 'Annual contract value'),
    ('Contract Status', 'Active, Expiring Soon, Expired'),
    ('Days Until Expiry', 'Days from today to end date'),
    ('Expiration Alert', 'Flag if within alert threshold (Yes/No)'),
    ('Renewal Option', 'Contractual renewal clause'),
    ('Negotiation Recommended', 'Trigger based on alert/policy'),
    ('Last Negotiation Date', 'Previous negotiation, if applicable'),
]

vendors = ['Microsoft','AWS','Adobe','Blackboard','Cisco','Zoom','Oracle']
systems = ['Email','Cloud Storage','LMS','Network','Security','Video','ERP']
np.random.seed(115)
contracts = []
for vendor in vendors:
    for system in np.random.choice(systems, 2, replace=False):
        start = (date_today.replace(year=np.random.choice([2022,2023,2024])) - pd.Timedelta(days=np.random.randint(100,800)))
        end = start + pd.Timedelta(days=np.random.randint(250,730))
        spend = np.random.randint(48_000,480_000)
        days_to_expiry = (end - date_today).days
        status = 'Active' if days_to_expiry > 0 else 'Expired'
        alert = 'Yes' if status=='Active' and days_to_expiry < alert_threshold else 'No'
        renewal = np.random.choice(['Auto-Renew','Manual','Negotiation Required'])
        negotiate = 'Yes' if alert=='Yes' or renewal!='Auto-Renew' else 'No'
        last_neg = (start + pd.Timedelta(days=np.random.randint(1,200))).strftime('%Y-%m-%d')
        contracts.append((vendor, system, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), spend, status, days_to_expiry, alert, renewal, negotiate, last_neg))

contract_alerts_df = pd.DataFrame(contracts, columns=[m[0] for m in contract_metrics])
contract_alerts_df.to_csv('cfo_contract_expiration_alerts_examples.csv', index=False)
print('CFO contract expiration alerts metrics CSV with examples saved.')

# Python module to flag expiring/negotiation contracts
script_contracts = '''\n# CFO Contract Expiration Alerts Module\nimport pandas as pd\ndef flag_expiring_contracts(df,date_today=pd.Timestamp('2025-08-19'),alert_days=90):\n    expiring = df[(df['Expiration Alert']=='Yes') | (df['Negotiation Recommended']=='Yes')]\n    return expiring\n'''
with open('cfo_contract_expiration_alerts_module.py', 'w') as f:
    f.write(script_contracts)
print('CFO contract expiration alerts module Python script saved.')