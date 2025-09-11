# simple_git_commit.ps1
# Quick PowerShell script to commit your working ISSA dashboard

Write-Host "🚀 ISSA Dashboard Git Commit Helper" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check if we're in a git repository
if (!(Test-Path ".git")) {
    Write-Host "❌ Not in a Git repository. Initializing..." -ForegroundColor Red
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Check current status
Write-Host "`n📋 Current Git Status:" -ForegroundColor Yellow
git status

# Add important files (exclude old_versions and temp files)
Write-Host "`n📁 Adding important files..." -ForegroundColor Yellow

# Create .gitignore if it doesn't exist
if (!(Test-Path ".gitignore")) {
    @"
# Python
__pycache__/
*.py[cod]
*.pyc

# VS Code
.vscode/
*.code-workspace

# Backup and old files
old_versions/
backup/
temp/
*.bak
*.tmp

# Data files (optional - keep structure, ignore content)
data/uploads/*
data/processed/*
!data/uploads/.gitkeep
!data/processed/.gitkeep

# Logs
logs/
*.log

# Environment files
.env
.env.local

# OS files
.DS_Store
Thumbs.db
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ Created .gitignore" -ForegroundColor Green
}

# Add the important dashboard files
$importantFiles = @(
    "src/dashboard/fully_integrated_dashboard.py",
    "src/dashboard/dashboard_metric_loader.py", 
    "src/dashboard/metric_registry.py",
    "src/dashboard/hbcu_metrics_integration.py",
    "src/dashboard/issa_theme.py",
    ".gitignore",
    "requirements.txt"
)

foreach ($file in $importantFiles) {
    if (Test-Path $file) {
        git add $file
        Write-Host "✅ Added: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Not found: $file" -ForegroundColor Yellow
    }
}

# Show what will be committed
Write-Host "`n📋 Files staged for commit:" -ForegroundColor Cyan
git diff --name-only --cached

# Prompt for commit message
Write-Host "`n💬 Enter commit message (or press Enter for default):" -ForegroundColor Yellow
$commitMessage = Read-Host
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Working ISSA dashboard - all personas functional"
}

# Commit the changes
Write-Host "`n🔄 Committing changes..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully committed changes!" -ForegroundColor Green
    
    # Check if we have a remote repository
    $remotes = git remote
    if ($remotes) {
        Write-Host "`n🌐 Detected remote repository. Push to remote? (y/n):" -ForegroundColor Cyan
        $pushChoice = Read-Host
        if ($pushChoice -eq "y" -or $pushChoice -eq "Y") {
            git push
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Successfully pushed to remote!" -ForegroundColor Green
            } else {
                Write-Host "❌ Push failed. Check your remote configuration." -ForegroundColor Red
            }
        }
    } else {
        Write-Host "`n💡 No remote repository configured." -ForegroundColor Yellow
        Write-Host "   To add one later: git remote add origin <your-repo-url>" -ForegroundColor Yellow
    }
    
    Write-Host "`n🎉 Git commit complete!" -ForegroundColor Green
    Write-Host "Your working dashboard code is now safely committed." -ForegroundColor White
    
} else {
    Write-Host "❌ Commit failed. Check the error messages above." -ForegroundColor Red
}

Write-Host "`n📊 Final repository status:" -ForegroundColor Cyan
git status --short