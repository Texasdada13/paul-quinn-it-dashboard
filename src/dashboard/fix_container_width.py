import re

# Read the dashboard file
with open('fully_integrated_dashboard.py', 'r') as f:
    content = f.read()

# Replace use_container_width=True with width='stretch'
content = re.sub(r'use_container_width=True', "width='stretch'", content)

# Write back the fixed content
with open('fully_integrated_dashboard.py', 'w') as f:
    f.write(content)

print("Fixed use_container_width parameters")
