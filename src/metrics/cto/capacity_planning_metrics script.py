import pandas as pd
import numpy as np

# CTO Metrics: Capacity planning indicators for proactive scaling
capacity_metrics = [
    ('Asset/Component', 'Infrastructure element tracked for capacity'),
    ('Peak Utilization (%)', 'Highest observed utilization for component/system'),
    ('Average Utilization (%)', 'Mean utilization over selected time window'),
    ('Seasonal/Weekly Utilization Pattern', 'Pattern or index for regular spikes/dips (e.g., semester start)'),
    ('Capacity Threshold (%)', 'Pre-set upper utilization limit before scaling action'),
    ('Current Buffer Capacity (%)', 'Percent available resource headroom (100%-Current Peak)'),
    ('Forecasted Utilization Growth (%)', 'Projected increase based on historical/data trend'),
    ('Time-to-Threshold (days)', 'Predicted days/resources until threshold likely exceeded'),
    ('Scaling Recommendation', 'Advisory: scale-up, scale-out, maintain'),
    ('Physical/Virtual Capacity', 'Actual installed/virtual resource limits (CPU, RAM, storage, bandwidth)'),
    ('Scalability Score', 'Composite score for ease of scaling (1-10 scale)'),
    ('Auto-Scaling Event Count', 'Times infrastructure was automatically scaled in period'),
    ('Resource Bottleneck Detector', 'Flag for elements causing performance bottleneck'),
    ('Utilization/Performance Variance', 'Standard deviation/variance from peak usage'),
    ('Pending Capacity Requests', 'Count of pending new requests for capacity from users/projects'),
    ('Capacity Used Per FTE ($)', 'Annual cost/component used per full-time equivalent'),
    ('Capacity Utilization by Business Unit', 'Usage per unit/group (e.g., labs, admin, students)'),
    ('Service Impact Score', 'Rating of how scaling decisions impact service availability/performance'),
    ('Redundancy/Failover Capacity (%)', 'Percent of infrastructure maintained for backup/failover'),
]

components = ['Campus WiFi', 'Data Analytics Cluster', 'Email Platform', 'Student Portal',
              'Core Network', 'Virtual Desktop', 'File Storage', 'Meeting Platform']
np.random.seed(28)
capacity_example_data = []
for metric, description in capacity_metrics:
    for comp in components:
        if 'Utilization' in metric or 'Threshold' in metric or 'Buffer' in metric or 'Growth' in metric or 'Redundancy' in metric:
            value = f"{np.round(np.random.uniform(23,98),1)}%"
        elif 'Time-to-Threshold' in metric:
            value = np.random.randint(7,350)
        elif 'Pattern' in metric:
            value = np.random.choice(['Stable','Cyclical','High at Semester Start','Weekend Dip','Holiday Spike'])
        elif 'Recommendation' in metric:
            value = np.random.choice(['Scale Up','Scale Out','Maintain','Investigate Bottleneck'])
        elif 'Capacity' in metric and 'Physical/Virtual' in metric:
            resource_type = np.random.choice(['CPU','RAM','Storage','Bandwidth'])
            value = f"{resource_type}: {np.random.randint(32,8096)} units"
        elif 'Score' in metric or 'Service Impact' in metric:
            value = np.round(np.random.uniform(4.3,9.7),1)
        elif 'Event Count' in metric or 'Bottleneck' in metric or 'Pending Capacity' in metric or 'Used' in metric or 'Requests' in metric:
            value = np.random.randint(0,26)
        elif 'Variance' in metric:
            value = np.round(np.random.uniform(0.2,31),2)
        elif 'Capacity Utilization by Business Unit' in metric:
            value = f"IT: {np.random.randint(15,250)}%, Admin: {np.random.randint(10,150)}%, Student Labs: {np.random.randint(13,220)}%"
        else:
            value = 'N/A'
        capacity_example_data.append((comp, metric, description, value))

capacity_dashboard_df = pd.DataFrame(capacity_example_data, columns=['Component','Metric','Description','Example'])
capacity_dashboard_df.to_csv('capacity_planning_dashboard_examples.csv', index=False)
print('Capacity planning metrics CSV with examples saved.')

# Optional python module template
script_capacity = '''\n# Capacity Planning & Scaling Metrics Module\ncapacity_metric_definitions = [\n    { 'metric': 'Peak Utilization (%)', 'description': 'Highest recorded usage over interval' },\n    { 'metric': 'Scaling Recommendation', 'description': 'Advisory action: scale up/out/maintain' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\ncapacity_records = [\n    ('Core Network', 'Peak Utilization (%)', '94.1%'),\n    ('Campus WiFi', 'Scaling Recommendation', 'Scale Up'),\n]\n\ndf_capacity = pd.DataFrame(capacity_records, columns=['Component','Metric','Value'])\n\n# Dashboard logic: flag components nearing threshold or recommended for scaling
# Utilization >85% or buffer <15%
def flag_scaling_needed(df):\n    near_peak = df[(df['Metric'] == 'Peak Utilization (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) > 85)]\n    low_buffer = df[(df['Metric'] == 'Current Buffer Capacity (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 15)]\n    scaling_recommend = df[(df['Metric'] == 'Scaling Recommendation') & (df['Value'].isin(['Scale Up','Scale Out','Investigate Bottleneck']))]
    return pd.concat([near_peak,low_buffer,scaling_recommend])\n# Usage\nissues = flag_scaling_needed(df_capacity)\nprint(issues)\n'''
with open('capacity_planning_metrics_module.py', 'w') as f:
    f.write(script_capacity)
print('Capacity planning metrics module Python script saved.')