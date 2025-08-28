# PowerShell script to fix dashboard_metric_loader.py

# Create a backup
Copy-Item "src\dashboard\dashboard_metric_loader.py" "src\dashboard\dashboard_metric_loader.py.backup"

# Read the file
$content = Get-Content "src\dashboard\dashboard_metric_loader.py" -Raw

# Fix applymap to map
$content = $content -replace '\.style\.applymap\(', '.style.map('

# Fix the display_generic_metric method
# Find the section with viz_col2 and add the clean_metric_name logic
$pattern = @'
(\s+with viz_col2:\s*\n\s+)(chart_type = st\.selectbox\(\s*\n\s+"Chart Type",\s*\n\s+\["Bar", "Line", "Scatter", "Box"\],\s*\n\s+key=f"{persona}_{metric_name}_chart_type"\s*\n\s+\))
'@

$replacement = @'
$1# Remove any persona prefix from metric_name if it exists
            clean_metric_name = metric_name
            if metric_name.startswith(f"{persona}_"):
                clean_metric_name = metric_name[len(persona)+1:]
            
            chart_type = st.selectbox(
                "Chart Type", 
                ["Bar", "Line", "Scatter", "Box"],
                key=f"{persona}_{clean_metric_name}_chart_type"
            )
'@

$content = $content -replace $pattern, $replacement

# Fix all other keys to use clean_metric_name
$content = $content -replace 'key=f"{persona}_{metric_name}_x"', 'key=f"{persona}_{clean_metric_name}_x"'
$content = $content -replace 'key=f"{persona}_{metric_name}_y"', 'key=f"{persona}_{clean_metric_name}_y"'
$content = $content -replace 'key=f"{persona}_{metric_name}_col"', 'key=f"{persona}_{clean_metric_name}_col"'
$content = $content -replace 'key=f"{persona}_{metric_name}_chart_{chart_type}"', 'key=f"{persona}_{clean_metric_name}_chart_{chart_type}"'

# Write the content back
Set-Content "src\dashboard\dashboard_metric_loader.py" $content -NoNewline

Write-Host "Dashboard metric loader has been updated!" -ForegroundColor Green
Write-Host "A backup was created at: src\dashboard\dashboard_metric_loader.py.backup" -ForegroundColor Yellow
Write-Host ""
Write-Host "To verify changes:" -ForegroundColor Cyan
Write-Host "  git diff src/dashboard/dashboard_metric_loader.py"
Write-Host ""
Write-Host "To revert if needed:" -ForegroundColor Cyan
Write-Host "  Copy-Item src\dashboard\dashboard_metric_loader.py.backup src\dashboard\dashboard_metric_loader.py -Force"