
# Digital Transformation Metrics Module
digital_metric_definitions = [
    { 'metric': 'Digital Transformation Maturity', 'description': 'Stage of transformation' },
    { 'metric': 'Online Learning Adoption Rate', 'description': 'Percent of courses offered online/hybrid' },
    # ... continued for all metrics ...
]

import pandas as pd

# Example digital progress data
digital_records = [
    ('Online BA in Psychology', 'Online Learning Adoption Rate', '88%'),
    ('AI Tutoring Platform', 'Satisfaction With Digital Learning', 4.7),
]

df_digital = pd.DataFrame(digital_records, columns=['Initiative','Metric','Value'])

# Dashboard alert: flag initiatives with <60% adoption or <3.5 satisfaction
def flag_low_progress(df):
    # For adoption rate, strip '%' safely
    low_adopt = df[(df['Metric'] == 'Online Learning Adoption Rate') & (df['Value'].apply(lambda x: float(x.strip('%')) if isinstance(x,str) else 0) < 60)]
    low_satis = df[(df['Metric'] == 'Satisfaction With Digital Learning') & (df['Value'] < 3.5)]
    return pd.concat([low_adopt,low_satis])

# Usage example
issues = flag_low_progress(df_digital)
print(issues)
