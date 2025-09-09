<#
.SYNOPSIS
    Complete ISSA Data Integration Setup Script
.DESCRIPTION
    Creates all directories, files, and content for ISSA Data Integration System
.NOTES
    Run this from your project root directory
#>

param(
    [switch]$Force,  # Force overwrite existing files
    [switch]$Verbose # Verbose output
)

# Set error action preference
$ErrorActionPreference = "Continue"

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [string]$Prefix = ""
    )
    if ($Prefix) {
        Write-Host "$Prefix " -NoNewline -ForegroundColor $Color
        Write-Host $Message
    } else {
        Write-Host $Message -ForegroundColor $Color
    }
}

function New-DirectoryIfNotExists {
    param([string]$Path)
    
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-ColorOutput "Created directory: $Path" $Green "✅"
    } else {
        Write-ColorOutput "Directory exists: $Path" $Yellow "⚠️"
    }
}

function New-FileWithContent {
    param(
        [string]$Path,
        [string]$Content,
        [switch]$Force
    )
    
    if ((Test-Path $Path) -and !$Force) {
        Write-ColorOutput "File exists (use -Force to overwrite): $Path" $Yellow "⚠️"
        return
    }
    
    try {
        Set-Content -Path $Path -Value $Content -Encoding UTF8
        Write-ColorOutput "Created file: $Path" $Green "✅"
    } catch {
        Write-ColorOutput "Failed to create file: $Path - $($_.Exception.Message)" $Red "❌"
    }
}

Write-ColorOutput "🚀 ISSA Complete Setup Script Starting..." $Blue
Write-ColorOutput "=" * 60 $Blue

# Verify we're in the right directory
$currentDir = Get-Location
Write-ColorOutput "Current directory: $currentDir" $Blue

if (!(Test-Path "src")) {
    Write-ColorOutput "Error: 'src' directory not found. Please run this from your project root." $Red "❌"
    exit 1
}

Write-ColorOutput "`n📁 Creating Directory Structure..." $Blue

# Create all directories
$directories = @(
    "data",
    "data/uploads",
    "data/processed", 
    "data/backups",
    "data/reports",
    "src/integrations",
    "src/security",
    "src/pipelines",
    "src/utils",
    "src/tests",
    "logs"
)

foreach ($dir in $directories) {
    New-DirectoryIfNotExists $dir
}

Write-ColorOutput "`n📄 Creating Configuration Files..." $Blue

# pipeline_config.json
$pipelineConfig = @'
{
  "data_sources": {
    "sap": {
      "enabled": false,
      "base_url": "",
      "client_id": "",
      "client_secret": "",
      "username": "",
      "password": ""
    },
    "paycom": {
      "enabled": false,
      "api_key": "",
      "company_id": ""
    },
    "file_upload": {
      "enabled": true,
      "watch_directory": "data/uploads",
      "processed_directory": "data/processed",
      "supported_formats": ["csv", "xlsx", "xls"],
      "auto_process": true
    }
  },
  "pipeline_settings": {
    "schedule_frequency": "daily",
    "schedule_time": "06:00",
    "data_retention_days": 30,
    "enable_encryption": false,
    "backup_enabled": true,
    "quality_checks": true,
    "max_file_size_mb": 50,
    "timeout_minutes": 30
  },
  "output_settings": {
    "cfo_metrics_path": "src/metrics/cfo/cfo_contract_expiration_alerts_examples.csv",
    "cio_metrics_path": "src/metrics/cio/",
    "cto_metrics_path": "src/metrics/cto/",
    "backup_directory": "data/backups",
    "reports_directory": "data/reports",
    "processed_directory": "data/processed"
  },
  "notification_settings": {
    "email_enabled": false,
    "email_recipients": [],
    "slack_webhook": "",
    "alert_on_failure": true,
    "alert_on_success": false
  },
  "security_settings": {
    "encryption_key": "",
    "mask_sensitive_data": true,
    "audit_logging": true,
    "data_classification": {
      "vendor_info": "sensitive",
      "financial_data": "highly_sensitive",
      "contract_details": "sensitive"
    }
  }
}
'@

New-FileWithContent -Path "pipeline_config.json" -Content $pipelineConfig -Force:$Force

# .env.template
$envTemplate = @'
# ISSA Data Integration Environment Variables
# Copy this file to .env and fill in your values

# Encryption Key (generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
ISSA_ENCRYPTION_KEY=

# SAP Configuration
SAP_BASE_URL=
SAP_CLIENT_ID=
SAP_CLIENT_SECRET=
SAP_USERNAME=
SAP_PASSWORD=

# Paycom Configuration
PAYCOM_API_KEY=
PAYCOM_COMPANY_ID=

# Database Configuration (if using)
DATABASE_URL=

# Logging Level
LOG_LEVEL=INFO

# Email Notifications (optional)
SMTP_SERVER=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
NOTIFICATION_EMAILS=

# Dashboard Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
'@

New-FileWithContent -Path ".env.template" -Content $envTemplate -Force:$Force

# requirements.txt
$requirements = @'
# Core dependencies
streamlit>=1.25.0
pandas>=1.3.0
plotly>=5.0.0
numpy>=1.21.0

# Data integration
cryptography>=3.4.8
requests>=2.25.1
schedule>=1.1.0

# File processing
openpyxl>=3.0.7
xlrd>=2.0.1

# Security
python-dotenv>=0.19.0

# Development and testing
pytest>=6.2.4
pytest-cov>=2.12.1

# Optional: Database support
# sqlalchemy>=1.4.0
# psycopg2-binary>=2.9.0

# Optional: Email notifications
# smtplib (built-in)
# email (built-in)
'@

New-FileWithContent -Path "requirements.txt" -Content $requirements -Force:$Force

# .gitignore
$gitignore = @'
# ISSA Data Integration .gitignore

# Environment files
.env
.env.local
.env.production
.env.*.local

# Data files (keep structure, ignore content)
data/uploads/*
data/processed/*
data/backups/*
data/reports/*
!data/uploads/.gitkeep
!data/processed/.gitkeep
!data/backups/.gitkeep
!data/reports/.gitkeep

# Configuration with secrets
pipeline_config_production.json
*_secrets.json

# Logs
logs/
*.log
audit_log_*.json
pipeline_stats.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Streamlit
.streamlit/
.streamlit/secrets.toml

# VS Code
.vscode/
*.code-workspace

# System files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Windows
*.tmp
Desktop.ini
$RECYCLE.BIN/

# Backup files
*.bak
*.backup
*_backup.*
*_original.*

# Temporary files
temp/
tmp/
*.temp
'@

New-FileWithContent -Path ".gitignore" -Content $gitignore -Force:$Force

Write-ColorOutput "`n📚 Creating Documentation Files..." $Blue

# README.md (Main Project)
$readmeMain = @'
# ISSA - Integrated Systems for Strategic Analytics
## Paul Quinn College IT Dashboard

### 🎯 Overview
ISSA is a comprehensive IT analytics dashboard designed specifically for Higher Education institutions, with enhanced capabilities for HBCUs like Paul Quinn College. The platform provides persona-based dashboards for CFO, CIO, CTO, and Project Managers with live data integration capabilities.

### ✨ Key Features
- **Multi-Persona Dashboards**: Tailored views for CFO, CIO, CTO, and PM roles
- **Live Data Integration**: Connect to SAP, Paycom, and file uploads
- **Automated Processing**: Scheduled data pipelines with quality validation
- **Security & Compliance**: Data encryption, masking, and audit logging
- **HBCU-Specific Metrics**: Specialized analytics for HBCU institutions
- **Real-time Updates**: Dynamic metrics with live data sources

### 🚀 Quick Start
For immediate setup, see our [15-minute Quick Start Guide](QUICK_START.md).

### 📊 Dashboard Views

#### CFO - Financial Steward
- Budget variance analysis with alerts
- Contract expiration tracking
- Vendor spend optimization
- Grant compliance monitoring
- ROI and peer benchmarking

#### CIO - Strategic Partner  
- Digital transformation metrics
- Business unit IT spend analysis
- Strategic alignment tracking
- Risk and vendor management

#### CTO - Technology Operator
- Infrastructure performance monitoring
- Cloud cost optimization
- Asset lifecycle management
- Security metrics and incident response
- Technical debt tracking

#### Project Manager
- Project charter and portfolio metrics
- Timeline and budget performance
- Requirements traceability matrix
- RAID log management
- Resource allocation tracking

### 🔧 Installation

#### Prerequisites
- Python 3.8+
- Streamlit 1.25+
- Required packages: `pip install -r requirements.txt`

#### Automated Setup
```bash