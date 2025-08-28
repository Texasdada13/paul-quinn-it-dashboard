import pandas as pd
import numpy as np
from datetime import datetime

# CFO Metric: Budget vs. Actual Spend Analysis with Variance Alerts
budget_actual_metrics = [
    ('Budget Category', 'Main area tracked (e.g., project, department)'),
    ('Period', 'Fiscal year/quarter/month'),
    ('Initial Budget', 'Original budgeted dollars for period/category'),
    ('Actual Spend', 'Actual expenses for period/category'),
    ('Variance Amount', 'Actual Spend - Initial Budget'),
    ('Variance %', 'Variance Amount / Initial Budget * 100'),
    ('Variance Alert', 'Status based on threshold (OK, Warning, Overrun)'),
    ('Cumulative to Date', 'Total FY actual spend so far'),
    ('Remaining Budget', 'Budgeted minus spent'),
    ('Prior Year Spend', "Last year's spend for comparison"),
]

categories = ['IT Project Portfolio', 'Operations', 'Academic Tech', 'Cloud Spend', 'Cybersecurity', 'Student Services IT', 'Infrastructure']
periods = ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025']
np.random.seed(30)
data = []
for category in categories:
    for period in periods:
        init_budget = np.random.randint(65000,300000)
        # Simulate actuals with some over/under
        actual = init_budget + np.random.randint(-30000,35000)
        variance_amt = actual - init_budget
        variance_pct = round((variance_amt / init_budget) * 100, 1)
        alert = 'OK' if abs(variance_pct) <= 5 else ('Warning' if abs(variance_pct) <= 10 else 'Overrun')
        prior = init_budget + np.random.randint(-20000,22000)
        ctd = actual if period == 'Q4 2025' else np.random.randint(0, actual)
        rem = init_budget - ctd
        data.append((category, period, init_budget, actual, variance_amt, f'{variance_pct} %', alert, ctd, rem, prior))

budget_vs_actual_df = pd.DataFrame(data, columns=[m[0] for m in budget_actual_metrics])
budget_vs_actual_df.to_csv('cfo_budget_vs_actual_examples.csv', index=False)
print('CFO budget vs actual spend metrics CSV with examples saved.')

# Python module to flag overruns/warnings
script_varalert = '''\n# CFO Budget vs Actual Analysis with Alerts\nimport pandas as pd\ndef flag_variance(alert_threshold=5, overrun_threshold=10):\n    # DataFrame must contain columns: ['Budget Category','Period','Initial Budget','Actual Spend','Variance %','Variance Alert']\n    pass # For actual dashboard, compare variance pct to thresholds, output flagged lines\n'''
with open('cfo_budget_vs_actual_module.py', 'w') as f:
    f.write(script_varalert)
print('CFO budget vs actual spend module Python script saved.')