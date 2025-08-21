import pandas as pd
import numpy as np

# CFO Key Metrics: ROI calculations for IT investments tied to student success
roi_metrics = [
    ('Investment Name','IT project or initiative'),
    ('Investment Category','Infrastructure, Academic Tech, Support, Security, etc.'),
    ('Year','Fiscal year of investment'),
    ('Total IT Investment','Total spend on investment/project'),
    ('Student Population Served','Number of directly impacted students'),
    ('Cost Per Student Served','Investment ÷ student population'),
    ('Student Success Outcome Metric','What outcome does investment support'),
    ('Baseline Outcome Rate','Success metric pre-investment (e.g. grad, retention)'),
    ('Outcome Rate After Investment','Outcome metric after investment'),
    ('Absolute Outcome Improvement','Delta in outcome value'),
    ('Percent Outcome Improvement','Percent increase (post-pre)/pre*100'),
    ('Cost Per Outcome Improvement','Cost ÷ absolute improvement'),
    ('Estimated Lifetime Benefit ($)','Lifelong earnings, employment, retention $ gain'),
    ('ROI (Outcome-Driven)','(Benefit - Total IT Investment)/Investment*100'),
    ('Peer/Industry Benchmark','Peer/similar school comparable metric'),
    ('Stakeholder Satisfaction Score','Survey of perceived value/impact (1-5 or 1-10)'),
    ('Grant/Funder ROI Requirement Met','Yes/No'),
    ('Board-Level ROI Narrative','Narrative/summary for governance report'),
]

investments = ['Student Portal Upgrade','AI Tutoring','Learning Analytics','Cloud Modernization','LMS Mobile App','Cybersecurity','Virtual Lab']
years = [2023,2024,2025]
printf = lambda x: int(x) if abs(x-int(x))<0.01 else round(x,2)
np.random.seed(123)
data = []
for inv in investments:
    for year in years:
        cat = np.random.choice(['Academics','Support','Infrastructure','Security'])
        spend = np.random.randint(62_000,770_000)
        pop = np.random.randint(1100,4100)
        cost_per_student = round(spend/pop,2)
        metric = np.random.choice(['Graduation Rate','Retention Rate','1st-Year GPA','Completion Rate','Digital Literacy'])
        base_outcome = np.random.uniform(60,83) if 'Rate' in metric else np.random.uniform(2.1,2.9)
        # Simulate a modest gain
        if 'Rate' in metric:
            outcome_post = base_outcome + np.random.uniform(0.3,2.2)
        else:
            outcome_post = base_outcome + np.random.uniform(0.02,0.19)
        absolute = outcome_post - base_outcome
        percent_impr = round((absolute/base_outcome)*100,2)
        cost_per_outcome = round(spend/absolute,2) if absolute>0 else 0
        est_benefit = np.random.randint(spend,int(spend*4.5))
        roi_val = round((est_benefit-spend)/spend*100,2)
        benchmark = np.random.uniform(base_outcome-0.5,base_outcome+0.5)
        satis = round(np.random.uniform(3.4,4.7),1)
        grant_ok = np.random.choice(['Yes','No'],p=[0.8,0.2])
        board = f"Enabled {metric} improvement from {base_outcome:.1f} to {outcome_post:.1f} at ${cost_per_student:,.0f} per student."
        data.append(
            (inv,cat,year,spend,pop,cost_per_student,metric,float(f'{base_outcome:.2f}'),float(f'{outcome_post:.2f}'),
             round(absolute,2),percent_impr,cost_per_outcome,est_benefit,roi_val,float(f'{benchmark:.2f}'),satis,grant_ok,board) )

roi_df = pd.DataFrame(data, columns=[m[0] for m in roi_metrics])
roi_df.to_csv('cfo_student_success_roi_examples.csv', index=False)
print('CFO ROI for IT investments tied to student success metrics CSV with examples saved.')

# Python module for flagging high/low ROI and missed benchmarks
script_roi = '''\n# CFO IT Student Success ROI Module\nimport pandas as pd\ndef flag_roi_issues(df,min_roi=25):\n    low_roi = df[df['ROI (Outcome-Driven)']<min_roi]
    missed_bench = df[(df['Outcome Rate After Investment']<df['Peer/Industry Benchmark'])]
    no_grant_ok = df[df['Grant/Funder ROI Requirement Met']=='No']
    return pd.concat([low_roi,missed_bench,no_grant_ok]).drop_duplicates()\n'''
with open('cfo_student_success_roi_module.py', 'w') as f:
    f.write(script_roi)
print('CFO student success ROI module Python script saved.')