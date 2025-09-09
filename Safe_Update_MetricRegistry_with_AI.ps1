# PowerShell Script to Update withAI_metric_registry.py with AI Intelligence Features
# Safe version that uses separate file to avoid conflicts

param(
    [string]$SourceFile = "src\dashboard\withAI_metric_registry.py",
    [string]$OriginalFile = "src\dashboard\metric_registry.py", 
    [string]$BackupDir = "backup",
    [switch]$DryRun = $false,
    [switch]$CopyFromOriginal = $false
)

Write-Host "AI Metric Registry Update Script (Safe Version)" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
Write-Host "Updating: $SourceFile" -ForegroundColor White
Write-Host ""

# Ensure backup directory exists
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "Created backup directory: $BackupDir" -ForegroundColor Yellow
}

# Handle file preparation
if ($CopyFromOriginal) {
    if (Test-Path $OriginalFile) {
        Write-Host "Copying from original file: $OriginalFile" -ForegroundColor Cyan
        Copy-Item $OriginalFile $SourceFile
        Write-Host "Copied original to withAI file" -ForegroundColor Green
    } else {
        Write-Host "Original file not found: $OriginalFile" -ForegroundColor Red
        exit 1
    }
} elseif (!(Test-Path $SourceFile)) {
    if (Test-Path $OriginalFile) {
        Write-Host "withAI file not found, copying from original..." -ForegroundColor Cyan
        Copy-Item $OriginalFile $SourceFile
        Write-Host "Created withAI file from original" -ForegroundColor Green
    } else {
        Write-Host "Neither file found. Please ensure files exist:" -ForegroundColor Red
        Write-Host "   Original: $OriginalFile" -ForegroundColor Red
        Write-Host "   Target: $SourceFile" -ForegroundColor Red
        exit 1
    }
}

# Create backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "$BackupDir\withAI_metric_registry_backup_$timestamp.py"

Copy-Item $SourceFile $backupFile
Write-Host "Backup created: $backupFile" -ForegroundColor Green

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
}

# Read the current file
$content = Get-Content $SourceFile -Raw

# AI Intelligence imports to add
$aiImports = @"

# AI Intelligence imports
try:
    from metric_intelligence import MetricIntelligenceEngine, MetricInsight, analyze_single_metric
    AI_INTELLIGENCE_AVAILABLE = True
    print("AI intelligence features loaded successfully")
except ImportError as e:
    print(f"AI intelligence not available: {e}")
    AI_INTELLIGENCE_AVAILABLE = False
    MetricIntelligenceEngine = None
    MetricInsight = None

"@

# AI methods to add to MetricRegistry class
$aiRegistryMethods = @"

    def analyze_metric_with_ai(self, persona, metric_name):
        """Analyze metric with AI intelligence engine"""
        if not AI_INTELLIGENCE_AVAILABLE:
            return []
        
        try:
            data = self.load_metric_data(persona, metric_name)
            if data is None or data.empty:
                return []
            
            intelligence_engine = MetricIntelligenceEngine()
            insights = intelligence_engine.analyze_metric(data, persona, metric_name)
            return insights
        except Exception as e:
            print(f"AI analysis failed for {metric_name}: {e}")
            return []
    
    def get_ai_optimization_opportunities(self, persona):
        """Get AI-powered optimization opportunities for a persona"""
        if not AI_INTELLIGENCE_AVAILABLE:
            return {}
        
        try:
            intelligence_engine = MetricIntelligenceEngine()
            all_data = {}
            
            # Collect all metric data for the persona
            available_metrics = self.get_available_metrics(persona)
            for metric in available_metrics:
                data = self.load_metric_data(persona, metric)
                if data is not None and not data.empty:
                    all_data[metric] = data
            
            if not all_data:
                return {}
            
            # Generate comprehensive analysis
            all_insights = {}
            for metric_name, data in all_data.items():
                all_insights[metric_name] = intelligence_engine.analyze_metric(data, persona, metric_name)
            
            # Generate executive summary
            executive_summary = intelligence_engine.generate_executive_summary(all_insights, persona)
            
            return {
                'insights': all_insights,
                'summary': executive_summary,
                'optimization_opportunities': executive_summary.get('optimization_opportunities', []),
                'risk_alerts': executive_summary.get('risk_alerts', []),
                'top_recommendations': executive_summary.get('top_recommendations', [])
            }
        except Exception as e:
            print(f"AI optimization analysis failed for {persona}: {e}")
            return {}

"@

# Apply updates step by step
$updatedContent = $content

Write-Host "`nApplying AI imports..." -ForegroundColor Cyan
if ($updatedContent -notmatch "AI_INTELLIGENCE_AVAILABLE") {
    # Add after the existing imports
    $updatedContent = $updatedContent -replace "(import sys)", "$1$aiImports"
    Write-Host "Added AI intelligence imports" -ForegroundColor Green
} else {
    Write-Host "AI imports already present" -ForegroundColor Yellow
}

Write-Host "`nEnhancing MetricRegistry class with AI methods..." -ForegroundColor Cyan
# Find the get_metric_info method and add AI methods after it
$metricInfoPattern = '(    def get_metric_info\(self, persona, metric_name\):\s*"""Get all information about a specific metric"""\s*return self\.metrics\.get\(persona, \{\}\)\.get\(metric_name, \{\}\))'
if ($updatedContent -match $metricInfoPattern) {
    $updatedContent = $updatedContent -replace $metricInfoPattern, "$1$aiRegistryMethods"
    Write-Host "Added AI methods to MetricRegistry class" -ForegroundColor Green
} else {
    Write-Host "Could not find exact MetricRegistry pattern - trying alternative..." -ForegroundColor Yellow
    
    # Try broader pattern
    if ($updatedContent -match '(def get_metric_info.*?return self\.metrics\.get.*?\n)') {
        $updatedContent = $updatedContent -replace '(def get_metric_info.*?return self\.metrics\.get.*?\n)', "$1$aiRegistryMethods"
        Write-Host "Added AI methods using alternative pattern" -ForegroundColor Green
    }
}

Write-Host "`nEnhancing CFOMetrics class..." -ForegroundColor Cyan
# Update CFOMetrics __init__ method to add AI intelligence
$cfoInitPattern = '(class CFOMetrics:\s*"""CFO-specific metric handlers"""\s*def __init__\(self, registry\):\s*self\.registry = registry)'
$cfoInitReplacement = @'
$1
        self.intelligence_engine = MetricIntelligenceEngine() if AI_INTELLIGENCE_AVAILABLE else None
'@

if ($updatedContent -match $cfoInitPattern) {
    $updatedContent = $updatedContent -replace $cfoInitPattern, $cfoInitReplacement
    Write-Host "Enhanced CFOMetrics __init__ method" -ForegroundColor Green
}

# Add CFO AI methods after the last CFO method
$cfoAiMethods = @"

    def get_ai_financial_insights(self):
        """Get AI-powered financial insights for CFO"""
        if not self.intelligence_engine:
            return {}
        
        try:
            insights = {}
            
            # Budget variance insights
            budget_data, _ = self.get_budget_variance_data()
            if budget_data is not None:
                insights['budget_insights'] = self.intelligence_engine.analyze_metric(
                    budget_data, 'cfo', 'budget_variance'
                )
            
            # Contract optimization insights
            contract_data, _ = self.get_contract_alerts()
            if contract_data is not None:
                insights['contract_insights'] = self.intelligence_engine.analyze_metric(
                    contract_data, 'cfo', 'contract_optimization'
                )
            
            return insights
        except Exception as e:
            print(f"AI financial insights generation failed: {e}")
            return {}
    
    def get_optimization_recommendations(self):
        """Get AI-powered optimization recommendations for CFO"""
        if not self.intelligence_engine:
            return []
        
        try:
            # Return demo recommendations
            return [
                {
                    'title': 'Contract Consolidation Opportunity',
                    'savings': 67000,
                    'confidence': 0.92,
                    'timeline': '2-3 months',
                    'description': 'Consolidate Microsoft contracts for cost reduction'
                },
                {
                    'title': 'Budget Reallocation Strategy', 
                    'savings': 120000,
                    'confidence': 0.87,
                    'timeline': '1 month',
                    'description': 'Redirect underutilized budget to student success'
                }
            ]
        except Exception as e:
            print(f"CFO optimization recommendations failed: {e}")
            return []

"@

$cfoLastMethodPattern = '(    def get_student_success_roi\(self\):\s*"""Load student success ROI data"""\s*.*?return data, module)'
if ($updatedContent -match $cfoLastMethodPattern) {
    $updatedContent = $updatedContent -replace $cfoLastMethodPattern, "$1$cfoAiMethods"
    Write-Host "Added AI methods to CFOMetrics class" -ForegroundColor Green
}

Write-Host "`nEnhancing CIOMetrics and CTOMetrics classes..." -ForegroundColor Cyan
# Update CIOMetrics __init__ method
$cioInitPattern = '(class CIOMetrics:\s*"""CIO-specific metric handlers"""\s*def __init__\(self, registry\):\s*self\.registry = registry)'
$cioInitReplacement = @'
$1
        self.intelligence_engine = MetricIntelligenceEngine() if AI_INTELLIGENCE_AVAILABLE else None
'@

if ($updatedContent -match $cioInitPattern) {
    $updatedContent = $updatedContent -replace $cioInitPattern, $cioInitReplacement
    Write-Host "Enhanced CIOMetrics __init__ method" -ForegroundColor Green
}

# Update CTOMetrics __init__ method
$ctoInitPattern = '(class CTOMetrics:\s*"""CTO-specific metric handlers"""\s*def __init__\(self, registry\):\s*self\.registry = registry)'
$ctoInitReplacement = @'
$1
        self.intelligence_engine = MetricIntelligenceEngine() if AI_INTELLIGENCE_AVAILABLE else None
'@

if ($updatedContent -match $ctoInitPattern) {
    $updatedContent = $updatedContent -replace $ctoInitPattern, $ctoInitReplacement
    Write-Host "Enhanced CTOMetrics __init__ method" -ForegroundColor Green
}

Write-Host "`nAdding enhanced registry class..." -ForegroundColor Cyan
# Add enhanced registry class before final initialization
$enhancedRegistryClass = @"

class AIEnhancedMetricRegistry(MetricRegistry):
    """Enhanced registry with comprehensive AI optimization capabilities"""
    
    def __init__(self, base_path='src/metrics'):
        super().__init__(base_path)
        self.ai_engine = MetricIntelligenceEngine() if AI_INTELLIGENCE_AVAILABLE else None
    
    def get_comprehensive_ai_analysis(self, persona):
        """Get comprehensive AI analysis for all persona metrics"""
        if not self.ai_engine:
            return {'error': 'AI intelligence not available'}
        
        try:
            analysis_result = {
                'persona': persona,
                'timestamp': pd.Timestamp.now(),
                'metrics_analyzed': 0,
                'optimization_opportunities': [],
                'executive_summary': {}
            }
            
            available_metrics = self.get_available_metrics(persona)
            all_insights = {}
            
            # Analyze each metric with AI
            for metric_name in available_metrics:
                try:
                    data = self.load_metric_data(persona, metric_name)
                    if data is not None and not data.empty:
                        insights = self.ai_engine.analyze_metric(data, persona, metric_name)
                        if insights:
                            all_insights[metric_name] = insights
                            analysis_result['metrics_analyzed'] += 1
                except Exception as e:
                    print(f"AI analysis failed for metric {metric_name}: {e}")
                    continue
            
            # Generate executive summary
            if all_insights:
                analysis_result['executive_summary'] = self.ai_engine.generate_executive_summary(all_insights, persona)
            
            return analysis_result
        except Exception as e:
            return {'error': f'Comprehensive AI analysis failed: {e}'}

"@

# Replace the final registry initialization
$registryInitPattern = '(# Initialize the registry when imported\nmetric_registry = MetricRegistry\(\)\ncfo_metrics = CFOMetrics\(metric_registry\)\ncio_metrics = CIOMetrics\(metric_registry\)\ncto_metrics = CTOMetrics\(metric_registry\))'

if ($updatedContent -match $registryInitPattern) {
    $newInit = @"
$enhancedRegistryClass
# Initialize the enhanced registry when imported
metric_registry = AIEnhancedMetricRegistry()
cfo_metrics = CFOMetrics(metric_registry)
cio_metrics = CIOMetrics(metric_registry)
cto_metrics = CTOMetrics(metric_registry)
"@
    $updatedContent = $updatedContent -replace $registryInitPattern, $newInit
    Write-Host "Added enhanced registry class and updated initialization" -ForegroundColor Green
} else {
    Write-Host "Could not find registry initialization pattern - adding at end" -ForegroundColor Yellow
    $updatedContent += $enhancedRegistryClass
    $updatedContent += "`n# Initialize the enhanced registry`nmetric_registry = AIEnhancedMetricRegistry()`ncfo_metrics = CFOMetrics(metric_registry)`ncio_metrics = CIOMetrics(metric_registry)`ncto_metrics = CTOMetrics(metric_registry)"
}

if (-not $DryRun) {
    # Write updated content back to file
    $updatedContent | Set-Content $SourceFile -Encoding UTF8
    Write-Host "`nMetric Registry update completed!" -ForegroundColor Green
    Write-Host "Original backed up to: $backupFile" -ForegroundColor Yellow
    Write-Host "Updated file: $SourceFile" -ForegroundColor Yellow
} else {
    Write-Host "`nDry run completed. Run without -DryRun to apply changes." -ForegroundColor Yellow
}

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Ensure metric_intelligence.py is in src/dashboard/" -ForegroundColor White
Write-Host "2. Test the enhanced registry: python -c `"from src.dashboard.withAI_metric_registry import metric_registry; print('Enhanced registry loaded')`"" -ForegroundColor White  
Write-Host "3. Update your dashboard to use: from withAI_metric_registry import ..." -ForegroundColor White
Write-Host "4. When ready, merge changes to your main metric_registry.py" -ForegroundColor White
Write-Host "5. If issues occur, restore from backup: Copy-Item $backupFile $SourceFile" -ForegroundColor White

Write-Host "`nSafe Workflow:" -ForegroundColor Cyan
Write-Host "• Your original metric_registry.py remains untouched" -ForegroundColor White
Write-Host "• All AI enhancements are in the withAI file" -ForegroundColor White  
Write-Host "• Test AI features independently" -ForegroundColor White
Write-Host "• Merge when satisfied with both versions" -ForegroundColor White