import pandas as pd
import numpy as np

# CTO Metrics: Infrastructure performance indicators (uptime, response times, error rates)
infra_metrics = [
    ('System Uptime (%)', 'Percent of time system/network is available and operational'),
    ('Scheduled Downtime (hrs)', 'Planned outages for upgrades/maintenance (per month/year)'),
    ('Unplanned Downtime (hrs)', 'Unscheduled outages in service window'),
    ('Mean Time to Recovery (MTTR)', 'Average time to restore full service after outage'),
    ('Mean Time Between Failures (MTBF)', 'Average operating time between system failures'),
    ('Peak/Mean Response Time (ms)', 'Average time to process user/system requests'),
    ('Critical Incident Count', 'Number of P1/P2 incidents reported per period'),
    ('Error Rate (%)', 'Percent failed transactions/processes'),
    ('Capacity Utilization (%)', 'Percent utilization versus installed/system capacity'),
    ('Resource Scalability Index', 'Score/indicator of infrastructure elasticity'),
    ('Security Incident Rate', 'Number of security event detections per month/quarter'),
    ('Patch/Update Success Rate (%)', 'Percent systems successfully updated'),
    ('Support Ticket Volume', 'Number of IT/service requests per period'),
    ('Service Desk Response Time (min)', 'Average time to acknowledge a user issue'),
    ('Backlog Volume', 'Number of unresolved incidents/issues'),
    ('Availability Zone Redundancy', 'Count of independent availability zones/backup systems'),
    ('Energy Efficiency Rating', 'Score reflecting sustainable power usage'),
]

infrastructure = ['Network', 'WiFi', 'Campus Servers', 'Cloud Storage', 'VPN Gateway', 'Firewall', 'VoIP Phones']
np.random.seed(47)
infra_example_data = []
for metric, description in infra_metrics:
    for system in infrastructure:
        if '(%)' in metric:
            value = f"{np.round(np.random.uniform(91,99.99),2)}%"
        elif 'Downtime' in metric or 'Recovery' in metric or 'Between Failures' in metric or 'Response Time' in metric:
            value = np.round(np.random.uniform(0.2,72),2)
        elif 'Incident' in metric or 'Error' in metric or 'Volume' in metric or 'Count' in metric or 'Backlog' in metric or 'Redundancy' in metric:
            value = np.random.randint(0,55)
        elif 'Efficiency' in metric or 'Scalability' in metric:
            value = np.round(np.random.uniform(0.4,1.0),2)
        else:
            value = 'N/A'
        infra_example_data.append((system, metric, description, value))

infra_dashboard_df = pd.DataFrame(infra_example_data, columns=['Infrastructure','Metric','Description','Example'])
infra_dashboard_df.to_csv('infrastructure_performance_dashboard_examples.csv', index=False)
print('Infrastructure performance indicator metrics CSV with examples saved.')

# Optional module template
script_infra = '''\n# Infrastructure Performance Metrics Module\ninfra_metric_definitions = [\n    { 'metric': 'System Uptime (%)', 'description': 'Percent of time service is operational' },\n    { 'metric': 'Error Rate (%)', 'description': 'Percent failed requests' },\n    # ... continued for all metrics ...\n]\n\nimport pandas as pd\n\ninfra_records = [\n    ('Network', 'System Uptime (%)', '99.95%'),\n    ('VPN Gateway', 'Error Rate (%)', '1.2%'),\n]\n\ndf_infra = pd.DataFrame(infra_records, columns=['Infrastructure','Metric','Value'])\n\n# Flag infra systems with low uptime or high error rates\ndef flag_low_perf(df):\n    low_uptime = df[(df['Metric'] == 'System Uptime (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 97)]\n    high_error = df[(df['Metric'] == 'Error Rate (%)') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) > 5)]\n    return pd.concat([low_uptime,high_error])\n# Usage\nissues = flag_low_perf(df_infra)\nprint(issues)\n'''
with open('infrastructure_performance_metrics_module.py', 'w') as f:
    f.write(script_infra)
print('Infrastructure performance metrics module Python script saved.')