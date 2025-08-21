
# Risk Management Metrics Module
risk_metric_definitions = [
    { 'metric': 'Risk Exposure Level', 'description': 'Severity × Probability aggregate across all risks' },
    { 'metric': 'Risk Heat Map Category', 'description': 'Risk classified as Low/Medium/High/Critical' },
    # ... continued for all metrics ...
]

# Example risk data per project
risk_dashboard_records = [
    # project, metric, value
    ('Student Portal Upgrade', 'Risk Exposure Level', 6),
    ('Cybersecurity Enhancement', 'Risk Exposure Level', 9),
]

# DataFrame construction
import pandas as pd
df_risk = pd.DataFrame(risk_dashboard_records, columns=['Project', 'Metric', 'Value'])

# Dashboard logic: filter, alert, calculate
def highlight_high_risk(df):
    return df[df['Value'] >= 8]

# Usage example
high_risks = highlight_high_risk(df_risk)
print(high_risks)
