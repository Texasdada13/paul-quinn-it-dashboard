import pandas as pd
import numpy as np

# CFO Metric: Total IT Spend breakdown by project, vendor, functional area, 3-year trends
spend_breakdown_metrics = [
    ('Year', 'Reporting period'),
    ('Project', 'Named IT initiative or system'),
    ('Vendor', 'Supplier/service provider for project'),
    ('Functional Area', 'Major campus IT function'),
    ('Spend Amount', 'Total spend attributed for category/year'),
    ('% of Annual IT Budget', 'Category spend ÷ annual IT budget'),
    ('Spend YOY Change', 'Year-over-year $ or % change from prior year'),
    ('Peer/HBCU Benchmark Ratio', 'Comparison ratio to similar institutions/HBCUs'),
]

projects = ['Student Portal', 'Cybersecurity', 'Network Refresh', 'Cloud Migration', 'LMS Modernization', 'Mobile App', 'AI Tutoring']
vendors = ['Microsoft', 'AWS', 'Cisco', 'Zoom', 'Blackboard', 'Tableau', 'Others']
areas = [
    'Academic Apps', 'Infrastructure', 'Security', 'Communications', 'Data Analytics', 'Student Services', 'Core IT'
]
years = [2023,2024,2025]
np.random.seed(45)
data = []
annual_budget = {2023:2_800_000,2024:3_000_000,2025:3_200_000}
benchmarks = {'Academic Apps':0.9,'Infrastructure':1.2,'Security':1.1,'Communications':1.0,'Data Analytics':1.3,'Student Services':0.95,'Core IT':1.15}
for year in years:
    for project in projects:
        vendor = np.random.choice(vendors)
        area = np.random.choice(areas)
        spend = np.random.randint(38_000,370_000)
        pct_budget = round(spend/annual_budget[year]*100,2)
        # YOY: Compare to prior year if not first
        prev = [d for d in data if d[1]==project and d[0]==year-1]
        if prev:
            prev_spend = prev[0][4]
            yoy = f"{spend-prev_spend:+,}" if prev_spend else 'N/A'
        else:
            yoy = 'N/A'
        bench = benchmarks.get(area,1.0)
        data.append((year, project, vendor, area, spend, f'{pct_budget} %', yoy, bench))

it_spend_breakdown_df = pd.DataFrame(data, columns=[m[0] for m in spend_breakdown_metrics])
it_spend_breakdown_df.to_csv('cfo_total_it_spend_breakdown_examples.csv', index=False)
print('CFO total IT spend breakdown metrics CSV with examples saved.')

# Python module for dashboard integration
script_spendbreak = '''\n# CFO IT Spend Breakdown & Trend Module\nimport pandas as pd\ndef breakdown_by_category(df, years=[2023,2024,2025]):\n    pivot = df.pivot_table(index=['Project','Vendor','Functional Area'],columns='Year',values='Spend Amount')\n    return pivot\n# Usage\n# it_spend_breakdown_df = pd.read_csv('cfo_total_it_spend_breakdown_examples.csv')\n# spend_pivot = breakdown_by_category(it_spend_breakdown_df)\n'''
with open('cfo_total_it_spend_breakdown_module.py', 'w') as f:
    f.write(script_spendbreak)
print('CFO total IT spend breakdown module Python script saved.')