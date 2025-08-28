import pandas as pd
import numpy as np

# CFO Metric: Vendor Spend Optimization (underutilized licenses, overlapping subscriptions)
vendor_opt_metrics = [
    ('Vendor', 'Supplier/vendor name'),
    ('System/Product', 'Product/service under contract'),
    ('Annual Spend', 'Annual expenditure on vendor/system'),
    ('Total Licenses/Seats', 'Licensed seat count for system'),
    ('Active Users', 'Current active users this cycle'),
    ('Utilization Rate (%)', 'Active Users ÷ Total Licenses × 100'),
    ('Unused License Count', 'Total Licenses minus Active Users'),
    ('Unused License Cost', 'Pro-rated cost for unused seats'),
    ('Subscription Type', 'Service tier or license group'),
    ('Overlapping Subscription Flag', 'Boolean if duplicate/competing system in use'),
    ('Potential Savings ($)', 'Annual savings from license right-sizing/consolidation'),
    ('Renewal Date', 'Next contract expiration or renewal date'),
    ('Satisfaction Score', 'Stakeholder/user rating for service value (1-5)'),
]

vendors = ['Microsoft', 'AWS', 'Zoom', 'Adobe', 'Blackboard', 'Tableau', 'Cisco']
systems = ['Office 365','Canvas LMS','Video Conferencing','Cloud Storage','Student Portal','BI Analytics','Network Mgmt']
np.random.seed(85)
vendor_data = []
for vendor in vendors:
    for system in np.random.choice(systems, 3, replace=False):
        spend = np.random.randint(50_000,650_000)
        seats = np.random.randint(100,1000)
        users = np.random.randint(50,seats)
        util_rate = round(users/seats*100,1)
        unused_count = seats - users
        unused_cost = round(spend * unused_count / seats,2)
        sub_type = np.random.choice(['Std','Premium','Edu','Adv','Faculty','Staff','Student'])
        overlap = np.random.choice([True,False])
        pot_save = round(unused_cost + (np.random.randint(0,40000) if overlap else 0),2)
        renewal = pd.Timestamp('2025-08-19') + pd.Timedelta(days=int(np.random.uniform(30,340)))
        satis = round(np.random.uniform(3.1,4.8),1)
        vendor_data.append((vendor, system, spend, seats, users, util_rate, unused_count, unused_cost, sub_type, overlap, pot_save, renewal.strftime('%Y-%m-%d'), satis))

vendor_opt_df = pd.DataFrame(vendor_data, columns=[m[0] for m in vendor_opt_metrics])
vendor_opt_df.to_csv('cfo_vendor_spend_optimization_examples.csv', index=False)
print('CFO vendor spend optimization metrics CSV with examples saved.')

# Python module to flag underutilized and overlapping spend
script_vendoropt = '''\n# CFO Vendor Spend Optimization Analysis\nimport pandas as pd\ndef flag_underutilized_overlapping(df):\n    # DataFrame columns: ['Vendor','Utilization Rate (%)','Overlapping Subscription Flag','Unused License Count','Potential Savings ($)']\n    low_util = df[(df['Utilization Rate (%)'] < 80)]\n    overlap = df[(df['Overlapping Subscription Flag']==True)]\n    high_savings = df[df['Potential Savings ($)']>10000]
    return pd.concat([low_util,overlap,high_savings]).drop_duplicates()\n'''
with open('cfo_vendor_spend_optimization_module.py', 'w') as f:
    f.write(script_vendoropt)
print('CFO vendor spend optimization module Python script saved.')