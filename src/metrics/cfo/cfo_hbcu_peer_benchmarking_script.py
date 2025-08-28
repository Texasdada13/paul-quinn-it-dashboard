import pandas as pd
import numpy as np

# CFO Metric: Benchmarking against peer HBCUs for Board Decisions
benchmark_metrics = [
    ('Metric Category','Area or line item compared'),
    ('Fiscal Year','Year of comparison'),
    ('College','Institution name (Paul Quinn, Peer HBCU, Non-HBCU)'),
    ('IT Spend Per Student','Total IT spend divided by student enrollment'),
    ('Total IT Budget','Annual IT budget'),
    ('Instructional Spend Ratio','Instruction spend ÷ total revenue'),
    ('Academic Technology %','Share of IT budget on academic/teaching tech'),
    ('IT FTE Ratio','IT staff divided by student enrollment'),
    ('Benchmark Peer Median','Median value for comparable peer colleges'),
    ('PQ Delta to Peer (%)','% difference Paul Quinn to peer median'),
    ('Budget Justification Flag','Yes/No indicator if PQ higher/lower than peer'),
]

years = [2023,2024,2025]
colleges = ['Paul Quinn','Peer HBCU 1','Peer HBCU 2','Private College','Public University']
np.random.seed(211)
data = []
for year in years:
    for college in colleges:
        it_budget = np.random.randint(2_000_000,7_000_000)
        enroll = np.random.randint(1100,4500)
        spend_per_s = round(it_budget/enroll,2)
        instr_ratio = round(np.random.uniform(0.78,1.22),2)
        acadtech_pct = round(np.random.uniform(12,32),1)
        it_fte = np.random.randint(5,28)
        fte_ratio = round(it_fte/enroll,4)
        # For benchmarking: Use peer avg for comparison
        peer_vals = [d for d in data if d[1]==year and d[0]!='Paul Quinn']
        peer_spend_med = np.median([v[3] for v in peer_vals]) if peer_vals else spend_per_s
        delta = round((spend_per_s-peer_spend_med)/peer_spend_med*100,1) if peer_spend_med else 0
        flag = 'Yes' if abs(delta)>10 else 'No'
        data.append(( 'IT Spend Per Student', year, college, spend_per_s, it_budget, instr_ratio, acadtech_pct, fte_ratio, peer_spend_med, delta, flag ))

benchmark_df = pd.DataFrame(data, columns=benchmark_metrics)
benchmark_df.to_csv('cfo_hbcu_peer_benchmarking_examples.csv', index=False)
print('CFO HBCU peer benchmarking metrics CSV with examples saved.')

# Python module to report/flag benchmarking anomalies
script_benchmark = '''\n# CFO Peer HBCU Benchmarking Module\nimport pandas as pd\ndef flag_benchmark_for_board(df):\n    # DataFrame must have 'PQ Delta to Peer (%)' and 'Budget Justification Flag'\n    overages = df[(df['Budget Justification Flag']=='Yes') & (df['PQ Delta to Peer (%)']>10)]\n    shortages = df[(df['Budget Justification Flag']=='Yes') & (df['PQ Delta to Peer (%)']<-10)]\n    return pd.concat([overages,shortages])\n'''
with open('cfo_hbcu_peer_benchmarking_module.py', 'w') as f:
    f.write(script_benchmark)
print('CFO peer HBCU benchmarking module Python script saved.')