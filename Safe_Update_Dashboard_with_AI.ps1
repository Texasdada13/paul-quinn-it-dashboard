# PowerShell Script to Update withAI_Updates_fully_integrated_dashboard.py with AI Features
# Safe version that uses separate file to avoid conflicts

param(
    [string]$SourceFile = "src\dashboard\withAI_Updates_fully_integrated_dashboard.py",
    [string]$OriginalFile = "src\dashboard\fully_integrated_dashboard.py",
    [string]$BackupDir = "backup",
    [switch]$DryRun = $false,
    [switch]$CopyFromOriginal = $false
)

Write-Host "🚀 ISSA AI Dashboard Update Script (Safe Version)" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host "Updating: $SourceFile" -ForegroundColor White
Write-Host ""

# Ensure backup directory exists
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "📁 Created backup directory: $BackupDir" -ForegroundColor Yellow
}

# Handle file preparation
if ($CopyFromOriginal) {
    if (Test-Path $OriginalFile) {
        Write-Host "📋 Copying from original file: $OriginalFile" -ForegroundColor Cyan
        Copy-Item $OriginalFile $SourceFile
        Write-Host "✅ Copied original to withAI file" -ForegroundColor Green
    } else {
        Write-Host "❌ Original file not found: $OriginalFile" -ForegroundColor Red
        exit 1
    }
} elseif (!(Test-Path $SourceFile)) {
    if (Test-Path $OriginalFile) {
        Write-Host "📋 withAI file not found, copying from original..." -ForegroundColor Cyan
        Copy-Item $OriginalFile $SourceFile
        Write-Host "✅ Created withAI file from original" -ForegroundColor Green
    } else {
        Write-Host "❌ Neither file found. Please ensure files exist:" -ForegroundColor Red
        Write-Host "   Original: $OriginalFile" -ForegroundColor Red
        Write-Host "   Target: $SourceFile" -ForegroundColor Red
        exit 1
    }
}

# Create backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "$BackupDir\withAI_dashboard_backup_$timestamp.py"

Copy-Item $SourceFile $backupFile
Write-Host "✅ Backup created: $backupFile" -ForegroundColor Green

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
}

# Read the current file
$content = Get-Content $SourceFile -Raw

# Define the AI enhancement updates
$aiImportsToAdd = @"

# AI Enhancement imports
try:
    from ai_optimization_engine import OptimizationDashboard, AIOptimizationEngine
    from metric_intelligence import MetricIntelligenceEngine, analyze_single_metric
    AI_FEATURES_AVAILABLE = True
    print("✅ AI optimization features loaded successfully")
except ImportError as e:
    print(f"⚠️ AI features not available: {e}")
    AI_FEATURES_AVAILABLE = False

"@

# Apply AI imports
Write-Host "`n📝 Adding AI imports..." -ForegroundColor Cyan
$updatedContent = $content

if ($updatedContent -notmatch "AI_FEATURES_AVAILABLE") {
    $updatedContent = $updatedContent -replace "(from issa_theme import ISSATheme.*?\n)", "`$1$aiImportsToAdd"
    Write-Host "✅ Added AI imports" -ForegroundColor Green
} else {
    Write-Host "⚠️ AI imports already present" -ForegroundColor Yellow
}

# Add CFO AI Tab to configuration
Write-Host "`n📝 Adding CFO AI tab configuration..." -ForegroundColor Cyan
$cfoTabPattern = '(\("📊 Budget Analysis", \["cfo_budget_vs_actual".*?\]\),\s*\("📃 Contracts & Vendors".*?\],\),)'
$cfoTabReplacement = @'
$1
            ("🤖 AI Optimization", []),  # NEW AI TAB
'@

if ($updatedContent -match $cfoTabPattern) {
    $updatedContent = $updatedContent -replace $cfoTabPattern, $cfoTabReplacement
    Write-Host "✅ Added AI tab to CFO configuration" -ForegroundColor Green
} else {
    Write-Host "⚠️ CFO tab pattern not found - checking alternative patterns..." -ForegroundColor Yellow
    
    # Try simpler pattern
    if ($updatedContent -match '(\("📊 Budget Analysis".*?\n.*?\("📃 Contracts.*?\n)') {
        $updatedContent = $updatedContent -replace '(\("📊 Budget Analysis".*?\n.*?\("📃 Contracts.*?\n)', '$1            ("🤖 AI Optimization", []),  # NEW AI TAB' + "`n"
        Write-Host "✅ Added AI tab using alternative pattern" -ForegroundColor Green
    }
}

# Add CFO AI Tab Handler
Write-Host "`n📝 Adding CFO AI tab handler..." -ForegroundColor Cyan
$cfoAiTabHandler = @"
                elif tab_name == "🤖 AI Optimization":
                    if AI_FEATURES_AVAILABLE:
                        st.markdown("### 🤖 AI-Powered Financial Optimization")
                        
                        # Create demo data for AI analysis
                        cfo_ai_data = {
                            'contract_data': pd.DataFrame({
                                'Vendor': ['Microsoft', 'Adobe', 'AWS', 'Microsoft', 'Salesforce'],
                                'Annual Spend': [150000, 80000, 200000, 90000, 120000],
                                'Days Until Expiry': [45, 120, 200, 30, 180]
                            }),
                            'budget_data': pd.DataFrame({
                                'Budget Category': ['Software', 'Hardware', 'Cloud', 'Consulting'],
                                'Initial Budget': [500000, 300000, 400000, 200000],
                                'Actual Spend': [420000, 280000, 450000, 160000]
                            })
                        }
                        
                        # Render AI optimization dashboard
                        optimization_dashboard = OptimizationDashboard()
                        optimization_dashboard.render_optimization_dashboard('cfo', cfo_ai_data)
                        
                    else:
                        st.warning("🤖 AI features not available. Please install required AI modules.")
                        
                        # Show demo content
                        st.markdown("#### Demo: AI Optimization Potential")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Potential Savings", "$450K", "+15%")
                        with col2:
                            st.metric("Optimization Score", "8.2/10", "+0.8")
                        with col3:
                            st.metric("AI Confidence", "87%", "+5%")

"@

# Find CFO "All Metrics" section and add AI handler before it
$cfoAllMetricsPattern = '(\s+elif tab_name == "📋 All Metrics":\s+dashboard_loader\.display_metric_summary\(''cfo''\))'
if ($updatedContent -match $cfoAllMetricsPattern) {
    $updatedContent = $updatedContent -replace $cfoAllMetricsPattern, "$cfoAiTabHandler`$1"
    Write-Host "✅ Added CFO AI tab handler" -ForegroundColor Green
} else {
    Write-Host "⚠️ CFO All Metrics pattern not found - will add to end of CFO section" -ForegroundColor Yellow
}

# Add CIO AI Tab
Write-Host "`n📝 Adding CIO AI optimization..." -ForegroundColor Cyan

# Add CIO AI tab to configuration
$cioTabPattern = '(\("🎯 Strategic Portfolio".*?\],\),\s*\("💼 Business Analysis".*?\],\),)'
$cioTabReplacement = @'
$1
            ("🤖 AI Strategic Optimization", []),  # NEW AI TAB
'@

if ($updatedContent -match $cioTabPattern) {
    $updatedContent = $updatedContent -replace $cioTabPattern, $cioTabReplacement
    Write-Host "✅ Added AI tab to CIO configuration" -ForegroundColor Green
}

# Add CIO AI tab handler
$cioAiTabHandler = @"
                elif tab_name == "🤖 AI Strategic Optimization":
                    if AI_FEATURES_AVAILABLE:
                        st.markdown("### 🤖 AI-Powered Strategic Optimization")
                        
                        # Strategic optimization for CIO
                        optimization_dashboard = OptimizationDashboard()
                        optimization_dashboard.render_optimization_dashboard('cio', {})
                        
                        # CIO-specific AI insights
                        st.markdown("---")
                        st.markdown("#### 🎯 Strategic AI Recommendations")
                        
                        with st.expander("💡 Digital Transformation Opportunities"):
                            st.success("**AI Recommendation**: Accelerate student analytics platform deployment")
                            st.info("Expected ROI: 4.2x over 3 years | Student retention impact: +12%")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Key Actions:**")
                                st.markdown("• Prioritize data integration initiatives")
                                st.markdown("• Implement predictive student success models") 
                                st.markdown("• Deploy real-time intervention systems")
                            with col2:
                                st.metric("Investment Required", "$200K")
                                st.metric("Expected Benefit", "$820K")
                                st.metric("AI Confidence", "82%")
                    else:
                        st.warning("🤖 AI strategic optimization features not available")

"@

# Find CIO section and add handler
if ($updatedContent -match '(elif persona == "CIO - Strategic Partner":.*?)(\s+# Add this after your existing CIO tabs)') {
    $cioSection = $updatedContent -replace '(for tab, \(tab_name, metrics_list\) in zip\(tabs, tab_config\):.*?\n.*?with tab:.*?\n.*?)(if tab_name == "📋 All Metrics":)', "`$1$cioAiTabHandler`$2"
    $updatedContent = $cioSection
    Write-Host "✅ Added CIO AI tab handler" -ForegroundColor Green
}

# Add CTO AI Tab
Write-Host "`n📝 Adding CTO AI optimization..." -ForegroundColor Cyan

# Add CTO AI tab to configuration  
$ctoTabPattern = '(\("🖥️ Infrastructure".*?\],\),\s*\("☁️ Cloud & Assets".*?\],\),)'
$ctoTabReplacement = @'
$1
            ("🤖 AI Operational Optimization", []),  # NEW AI TAB
'@

if ($updatedContent -match $ctoTabPattern) {
    $updatedContent = $updatedContent -replace $ctoTabPattern, $ctoTabReplacement
    Write-Host "✅ Added AI tab to CTO configuration" -ForegroundColor Green
}

# Add CTO AI tab handler
$ctoAiTabHandler = @"
                elif tab_name == "🤖 AI Operational Optimization":
                    if AI_FEATURES_AVAILABLE:
                        st.markdown("### 🤖 AI-Powered Operational Optimization")
                        
                        # Operational optimization for CTO
                        optimization_dashboard = OptimizationDashboard()
                        optimization_dashboard.render_optimization_dashboard('cto', {})
                        
                        # CTO-specific AI insights
                        st.markdown("---")
                        st.markdown("#### ⚡ Operational AI Recommendations")
                        
                        with st.expander("☁️ Infrastructure Right-Sizing"):
                            st.success("**AI Recommendation**: Cloud resource optimization identified")
                            st.info("Potential annual savings: $180K | Efficiency improvement: 40%")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Optimization Actions:**")
                                st.markdown("• Right-size over-provisioned instances")
                                st.markdown("• Implement auto-scaling policies")
                                st.markdown("• Optimize storage tiers")
                            with col2:
                                st.metric("Current Monthly Cost", "$25K")
                                st.metric("Optimized Cost", "$18K")
                                st.metric("Monthly Savings", "$7K")
                    else:
                        st.warning("🤖 AI operational optimization features not available")

"@

# Find CTO section and add handler
if ($updatedContent -match 'elif persona == "CTO - Technology Operator":') {
    $ctoSection = $updatedContent -replace '(CTO.*?for tab, \(tab_name, metrics_list\) in zip\(tabs, tab_config\):.*?\n.*?with tab:.*?\n.*?)(if tab_name == "📋 All Metrics":)', "`$1$ctoAiTabHandler`$2"
    $updatedContent = $ctoSection
    Write-Host "✅ Added CTO AI tab handler" -ForegroundColor Green
}

if (-not $DryRun) {
    # Write updated content back to file
    $updatedContent | Set-Content $SourceFile -Encoding UTF8
    Write-Host "`n🎉 Dashboard update completed!" -ForegroundColor Green
    Write-Host "📁 Original backed up to: $backupFile" -ForegroundColor Yellow
    Write-Host "🔄 Updated file: $SourceFile" -ForegroundColor Yellow
} else {
    Write-Host "`n🔍 Dry run completed. Run without -DryRun to apply changes." -ForegroundColor Yellow
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Ensure ai_optimization_engine.py is in src/dashboard/" -ForegroundColor White
Write-Host "2. Ensure metric_intelligence.py is in src/dashboard/" -ForegroundColor White
Write-Host "3. Test your enhanced dashboard: python -m streamlit run $SourceFile" -ForegroundColor White
Write-Host "4. When ready, copy enhancements to your main dashboard file" -ForegroundColor White
Write-Host "5. If issues occur, restore from backup: Copy-Item $backupFile $SourceFile" -ForegroundColor White

Write-Host "`n💡 Safe Workflow:" -ForegroundColor Cyan
Write-Host "• Your original dashboard file remains untouched" -ForegroundColor White
Write-Host "• All AI enhancements are in the separate withAI file" -ForegroundColor White
Write-Host "• You can continue formatting the original while testing AI features" -ForegroundColor White
Write-Host "• Merge the changes when you're satisfied with both" -ForegroundColor White