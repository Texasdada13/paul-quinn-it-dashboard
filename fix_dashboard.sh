#!/bin/bash

# Create a backup first
cp src/dashboard/dashboard_metric_loader.py src/dashboard/dashboard_metric_loader.py.backup

# Fix the applymap deprecation warnings
sed -i 's/\.style\.applymap(/.style.map(/g' src/dashboard/dashboard_metric_loader.py

# Fix the duplicate key issue in display_generic_metric
# This is more complex, so we'll use a Python script embedded in bash
python3 << 'EOF'
import re

# Read the file
with open('src/dashboard/dashboard_metric_loader.py', 'r') as f:
    content = f.read()

# Find the display_generic_metric method and fix the key issues
def fix_display_generic_metric(content):
    # Pattern to find the chart_type selectbox
    pattern = r'(with viz_col2:\s*\n\s*)(chart_type = st\.selectbox\(\s*\n\s*"Chart Type",\s*\n\s*\["Bar", "Line", "Scatter", "Box"\],\s*\n\s*key=f"{persona}_{metric_name}_chart_type"\s*\n\s*\))'
    
    replacement = r'\1# Remove any persona prefix from metric_name if it exists\n            clean_metric_name = metric_name\n            if metric_name.startswith(f"{persona}_"):\n                clean_metric_name = metric_name[len(persona)+1:]\n            \n            chart_type = st.selectbox(\n                "Chart Type", \n                ["Bar", "Line", "Scatter", "Box"],\n                key=f"{persona}_{clean_metric_name}_chart_type"\n            )'
    
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Fix all other keys in the method to use clean_metric_name
    content = re.sub(
        r'key=f"{persona}_{metric_name}_x"',
        'key=f"{persona}_{clean_metric_name}_x"',
        content
    )
    content = re.sub(
        r'key=f"{persona}_{metric_name}_y"',
        'key=f"{persona}_{clean_metric_name}_y"',
        content
    )
    content = re.sub(
        r'key=f"{persona}_{metric_name}_col"',
        'key=f"{persona}_{clean_metric_name}_col"',
        content
    )
    content = re.sub(
        r'key=f"{persona}_{metric_name}_chart_{chart_type}"',
        'key=f"{persona}_{clean_metric_name}_chart_{chart_type}"',
        content
    )
    
    return content

# Apply the fix
fixed_content = fix_display_generic_metric(content)

# Write back to file
with open('src/dashboard/dashboard_metric_loader.py', 'w') as f:
    f.write(fixed_content)

print("All fixes applied successfully!")
EOF

echo "Dashboard metric loader has been updated!"
echo "A backup was created at: src/dashboard/dashboard_metric_loader.py.backup"
echo ""
echo "To verify the changes:"
echo "  diff src/dashboard/dashboard_metric_loader.py.backup src/dashboard/dashboard_metric_loader.py"
echo ""
echo "To revert if needed:"
echo "  mv src/dashboard/dashboard_metric_loader.py.backup src/dashboard/dashboard_metric_loader.py"