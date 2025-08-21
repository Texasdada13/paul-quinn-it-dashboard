import pandas as pd
import numpy as np

# CTO Metrics: Cloud cost optimization & resource utilization/right-sizing
cloud_metrics = [
    ('Service/Resource', 'Cloud platform/instance or service'),
    ('Cloud Spend (monthly)', 'Total monthly spend on cloud resources/services'),
    ('Resource Utilization (%)', 'Actual usage as percent of provisioned capacity'),
    ('Idle Resource Cost ($)', 'Spend on underutilized or inactive assets'),
    ('Right-Sizing Status', 'Indicator if the resource is appropriately resized (Yes/No)'),
    ('Scheduled vs On-Demand Cost Ratio', 'Cost spent on scheduled vs dynamic allocations'),
    ('Storage Utilization (%)', 'Used storage as percent of allocated capacity'),
    ('CPU/GPU Utilization (%)', 'Average CPU/GPU use over typical workday/week'),
    ('Reserved vs Spot Instance Usage (%)', 'Mix of long-term reserved and spot usage'),
    ('Automated Cost Alert', 'Was budget or optimization alert triggered this period?'),
    ('Optimized Recommendation Savings ($)', 'Potential savings identified by cloud optimizer tools'),
    ('Unused Service Count', 'Number of active subscriptions/services not used'),
    ('Forecasted Growth Rate (%)', 'Predicted month-over-month spend/infrastructure growth'),
    ('Service Uptime (%)', 'Availability of cloud service over last month'),
    ('Workload Distribution (Regions)', 'List/count of cloud regions utilized'),
    ('Data Egress Cost ($)', 'Spend on outbound data transfer'),
    ('License/Subscription Tier', 'Tier or plan assigned to each resource/service'),
]

cloud_services = ['AWS EC2', 'AWS S3', 'Azure SQL', 'Google BigQuery', 'Zoom Cloud', 'Canvas LMS Cloud', 'Tableau Cloud', 'Dropbox Business']
np.random.seed(19)
cloud_example_data = []
for metric, description in cloud_metrics:
    for service in cloud_services:
        if 'Spend' in metric or 'Cost' in metric or 'Savings' in metric:
            value = f"${np.random.randint(300,35000):,}"
        elif 'Utilization' in metric or 'Ratio' in metric or 'Usage' in metric or 'Growth' in metric or 'Reserved' in metric:
            value = f"{np.round(np.random.uniform(22,99),1)}%"
        elif 'Right-Sizing' in metric or 'Alert' in metric:
            value = np.random.choice(['Yes','No'])
        elif 'Recommendation' in metric:
            value = f"${np.random.randint(2500,19500):,}"
        elif 'Tier' in metric:
            value = np.random.choice(['Business','Standard','Enterprise','Premium'])
        elif 'Unused Service Count' in metric:
            value = np.random.randint(0,12)
        elif 'Service Uptime' in metric:
            value = f"{np.round(np.random.uniform(93,99.99),2)}%"
        elif 'Distribution' in metric:
            value = np.random.randint(1,9)
        else:
            value = 'N/A'
        cloud_example_data.append((service, metric, description, value))

cloud_dashboard_df = pd.DataFrame(cloud_example_data, columns=['Service','Metric','Description','Example'])
cloud_dashboard_df.to_csv('cloud_cost_optimization_dashboard_examples.csv', index=False)
print('Cloud cost optimization metrics CSV with examples saved.')

# Optional module template
script_cloud = '''\n# Cloud Cost & Resource Optimization Metrics Module\ncloud_metric_definitions = [\n    { 'metric': 'Resource Utilization (%)', 'description': 'Percent utilization of provisioned resources' },\n    { 'metric': 'Right-Sizing Status', 'description': 'Is instance right-sized for workload' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\ncloud_records = [\n    ('AWS EC2', 'Resource Utilization (%)', '47.9%'),\n    ('Zoom Cloud', 'Idle Resource Cost ($)', '$6,400'),\n]\n\ndf_cloud = pd.DataFrame(cloud_records, columns=['Service','Metric','Value'])\n\n# Flag underutilized or costly cloud resources\ndef flag_cloud_issues(df):\n    # Utilization <60% or Idle cost >5000
    low_util = df[(df['Metric'] == 'Resource Utilization (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 60)]\n    high_idle = df[(df['Metric'] == 'Idle Resource Cost ($)') & (df['Value'].apply(lambda x: float(x.replace('$','').replace(',','')) if isinstance(x,str) else 0) > 5000)]\n    return pd.concat([low_util,high_idle])\n# Usage\nissues = flag_cloud_issues(df_cloud)\nprint(issues)\n'''
with open('cloud_cost_optimization_metrics_module.py', 'w') as f:
    f.write(script_cloud)
print('Cloud cost optimization metrics module Python script saved.')