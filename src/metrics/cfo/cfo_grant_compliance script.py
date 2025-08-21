import pandas as pd
import numpy as np

# CFO Metrics: Compliance Reporting for Grant Funding Requirements (very exhaustive)
gr_compliance_metrics = [
    ('Grant Program/Source','Federal/foundation/grant-giver'),
    ('Grant Code','Internal or federal grant code/identifier'),
    ('FY','Fiscal or grant year'),
    ('Award Amount ($)','Original grant award'),
    ('Grant Period Start','Start date'),
    ('Grant Period End','End date'),
    ('Permitted Spend Categories','Summary/percent per category: Instruction, Tech, Scholarships, Admin, Other'),
    ('Spend To Date ($)','Year/cycle-to-date total spend applied'),
    ('Unspent Balance ($)','Award minus total spend'),
    ('Compliance Rate (%)','Percent of spend meeting all eligibility requirements'),
    ('Compliance Issues Flag','Flag for any open or closed compliance issues, e.g., improper costs'),
    ('Last Compliance Audit Date','Most recent audited/review date'),
    ('Audit Exceptions','Count or issues flagged in last audit'),
    ('Issue Description/Status','Narrative for any non-closeout, as applicable'),
    ('Corrective Actions (%)','% of required corrections resolved'),
    ('Timely Report Filing (%)','% reports on/before due date'),
    ('Key Grant Deliverables On-Track','Yes/No/milestone score'),
    ('Grant Drawdown Schedule Status','On/Behind/Ahead'),
    ('Disallowed/Questioned Costs ($)','Total costs disallowed or pending review'),
    ('Federal Financial Reporting Score','Automated or auditor score (1-10)'),
    ('Project Compliance Training Rate','% project team with current compliance training'),
    ('Indirect Cost Rate (%)','Current approved federal indirect rate'),
    ('Document Request Response Time (days)','Average days to submit requested docs for compliance checks'),
    ('Risk of Fund Clawback','Low/Moderate/High'),
    ('Pending/Upcoming Reports','Next due, with date/description'),
    ('History of Extension Requests','Count or record of past grant extensions'),
    ('Grant Renewal Eligibility Status','Eligible for renewal or at risk'),
    ('Percent Used for Direct Instruction/Student','Share of total spend serving student/final beneficiary'),
    ('Funder Satisfaction/Survey Score','Latest available survey/evaluation of grant management (1-10)'),
]

np.random.seed(246)
grants = [
    ('Title III HBCU','PQC-T3-2023','2024'),
    ('NSF S-STEM','PQC-NSF-2024','2025'),
    ('Gates Digital Equity','PQC-GATES-2025','2025'),
    ('Dept of Ed ARP','PQC-ARP-2023','2023')
]
grandata = []
for name, code, fy in grants:
    award = np.random.randint(400000,2200000)
    start = pd.Timestamp('2022-10-01') + pd.Timedelta(days=int(np.random.uniform(0,400)))
    end = start + pd.Timedelta(days=np.random.randint(350,720))
    instruct = np.random.randint(30,65)
    tech = np.random.randint(12,37)
    scholarship = np.random.randint(6,22)
    admin = np.random.randint(2,12)
    other = 100-instruct-tech-scholarship-admin if (instruct+tech+scholarship+admin)<100 else 0
    spends = np.random.randint(0,award)
    unspent = award-spends
    compl_rate = round(np.random.uniform(92,100),2)
    flag = np.random.choice(['Open','Closed','None'])
    last_audit = (start + pd.Timedelta(days=np.random.randint(30,400))).strftime('%Y-%m-%d')
    exceptions = np.random.choice([0,1,2])
    desc = '' if exceptions==0 else np.random.choice(['Minor doc error','Late cost draw','Ineligible spend'])
    corrections = np.random.randint(85,101)
    timely = np.random.randint(87,100)
    deliver = np.random.choice(['On Track','Behind','Milestone 2/3'])
    draw_status = np.random.choice(['On','Behind','Ahead'])
    disallow = np.random.randint(0,7000)
    fedscore = np.random.uniform(7.2,9.9)
    teamtrain = np.random.randint(72,100)
    indirate = round(np.random.uniform(7.5,16.5),2)
    docdays = np.random.uniform(1.7,12.3)
    risk = np.random.choice(['Low','Moderate','High'],p=[0.7,0.22,0.08])
    nextrep = f'{pd.Timestamp(end)+pd.Timedelta(days=np.random.randint(33,109)):%Y-%m-%d}: Final/Quarterly'
    extens = np.random.randint(0,3)
    renew = np.random.choice(['Eligible','At Risk','Not Eligible'])
    pct_direct = np.random.randint(56,100)
    survey = np.random.uniform(7.7,9.7)
    spendcat = f'Instruction:{instruct}%, Tech:{tech}%, Scholar:{scholarship}%, Admin:{admin}%, Other:{other}%'
    grandata.append((name,code,fy,award,start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'),spendcat,spends,unspent,compl_rate,flag,last_audit,exceptions,desc,corrections, timely, deliver,draw_status, disallow, round(fedscore,2), teamtrain, indirate, round(docdays,1),risk,nextrep,extens,renew,pct_direct,round(survey,1)))

gr_comp_df = pd.DataFrame(grandata, columns=[m[0] for m in gr_compliance_metrics])
gr_comp_df.to_csv('cfo_grant_compliance_report_examples.csv', index=False)
print('CFO grant compliance report metrics CSV with examples SAVED.')

# Python module for dashboard reporting/flagging
script_grcomp = '''\n# CFO Grant Compliance Dashboard Module\nimport pandas as pd\ndef flag_grant_compliance_issues(df, min_compliance=95):\n    noncompliant = df[df['Compliance Rate (%)']<min_compliance]
    unresolved = df[(df['Compliance Issues Flag']=='Open') | (df['Corrective Actions (%)']<97)]
    past_due = df[(df['Timely Report Filing (%)']<93)]
    highrisk = df[df['Risk of Fund Clawback']!='Low']
    under_direct = df[df['Percent Used for Direct Instruction/Student']<70]
    return pd.concat([noncompliant,unresolved,past_due,highrisk,under_direct]).drop_duplicates()\n'''
with open('cfo_grant_compliance_dashboard_module.py', 'w') as f:
    f.write(script_grcomp)
print('CFO grant compliance dashboard module Python script saved.')