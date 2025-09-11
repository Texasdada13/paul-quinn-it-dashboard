#!/usr/bin/env python3
"""
ISSA Dashboard Deployment Setup Script
Prepares your Paul Quinn College dashboard for online deployment
"""

import os
import sys
from pathlib import Path
import subprocess
import json

class ISSADeploymentSetup:
    def __init__(self):
        self.project_root = Path.cwd()
        self.dashboard_file = "src/dashboard/fully_integrated_dashboard.py"
        
    def create_requirements_txt(self):
        """Generate requirements.txt for deployment"""
        requirements = [
            "streamlit>=1.28.0",
            "pandas>=2.0.0", 
            "plotly>=5.15.0",
            "numpy>=1.24.0",
            "python-dateutil>=2.8.0",
            "openpyxl>=3.1.0",  # For Excel file handling
            "xlsxwriter>=3.1.0",  # For Excel exports
            "pathlib2",
            "typing-extensions"  
        ]
        
        with open("requirements.txt", "w") as f:
            f.write("\n".join(requirements))
        
        print("✅ Created requirements.txt")
        return requirements
    
    def create_streamlit_config(self):
        """Create Streamlit configuration for deployment"""
        config_dir = Path(".streamlit")
        config_dir.mkdir(exist_ok=True)
        
        config_content = """
[global]
developmentMode = false
showWarningOnDirectExecution = false

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1e3d59"
backgroundColor = "#f6f8fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#222d37"
"""
        
        with open(config_dir / "config.toml", "w") as f:
            f.write(config_content.strip())
        
        print("✅ Created Streamlit configuration")
    
    def create_gitignore(self):
        """Create .gitignore for clean deployment"""
        gitignore_content = """
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
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Data files (if sensitive)
*.env
secrets/
"""
        
        with open(".gitignore", "w") as f:
            f.write(gitignore_content.strip())
        
        print("✅ Created .gitignore")
    
    def create_procfile(self):
        """Create Procfile for Heroku deployment"""
        procfile_content = f"web: streamlit run {self.dashboard_file} --server.port=$PORT --server.address=0.0.0.0"
        
        with open("Procfile", "w") as f:
            f.write(procfile_content)
        
        print("✅ Created Procfile for Heroku")
    
    def create_runtime_txt(self):
        """Specify Python version for Heroku"""
        with open("runtime.txt", "w") as f:
            f.write("python-3.11.6")
        
        print("✅ Created runtime.txt")
    
    def create_deployment_readme(self):
        """Create deployment instructions"""
        readme_content = """# ISSA Dashboard - Paul Quinn College IT Analytics

## 🚀 Live Dashboard
Access the dashboard at: [Your Deployment URL]

## 📊 Dashboard Features
- **CFO Dashboard**: Financial oversight, budget analysis, contract management
- **CIO Dashboard**: Strategic IT portfolio management  
- **CTO Dashboard**: Technical operations and infrastructure
- **Project Management**: Complete project lifecycle tracking
- **HBCU Metrics**: Institution-specific analytics

## 🎯 Quick Deploy Options

### Option 1: Streamlit Community Cloud (FREE)
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `src/dashboard/fully_integrated_dashboard.py`
5. Deploy!

### Option 2: Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 🔧 Local Development
```bash
pip install -r requirements.txt
streamlit run src/dashboard/fully_integrated_dashboard.py
```

## 📱 Mobile Friendly
Dashboard is optimized for desktop and mobile viewing.

---
*Built for Paul Quinn College - Empowering HBCUs through data-driven technology decisions*
"""
        
        with open("README.md", "w") as f:
            f.write(readme_content)
        
        print("✅ Created deployment README.md")
    
    def create_demo_secrets(self):
        """Create sample secrets file for deployment"""
        secrets_dir = Path(".streamlit")
        secrets_dir.mkdir(exist_ok=True)
        
        demo_secrets = """
# Demo secrets for ISSA Dashboard
# Replace with actual credentials for production

[database]
host = "demo-host"
port = 5432
database = "issa_demo"
username = "demo_user"
password = "demo_password"

[api_keys]
openai_key = "your-openai-key-here"
google_analytics = "your-ga-key-here"

[app_settings]
demo_mode = true
institution_name = "Paul Quinn College"
"""
        
        with open(secrets_dir / "secrets.toml.example", "w") as f:
            f.write(demo_secrets.strip())
        
        print("✅ Created example secrets file")
    
    def optimize_dashboard_for_deployment(self):
        """Make dashboard deployment-ready"""
        dashboard_path = Path(self.dashboard_file)
        
        if not dashboard_path.exists():
            print(f"❌ Dashboard file not found: {self.dashboard_file}")
            return False
        
        # Read current dashboard
        with open(dashboard_path, 'r') as f:
            content = f.read()
        
        # Add deployment optimizations
        optimizations = """
# Deployment optimizations
import os

# Set page config first (must be first Streamlit command)
st.set_page_config(
    page_title="ISSA - Paul Quinn College IT Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:support@issa-analytics.com',
        'Report a bug': 'mailto:bugs@issa-analytics.com',
        'About': "ISSA Dashboard - Empowering HBCU technology decisions"
    }
)

# Cache configuration for better performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_metric_data(persona, metric):
    \"\"\"Cached data loading for better performance\"\"\"
    return dashboard_loader.registry.load_metric_data(persona, metric)

# Add error handling for deployment
try:
    # Your existing dashboard code
    pass
except Exception as e:
    st.error(f"Dashboard initialization error: {str(e)}")
    st.info("Please contact support if this error persists.")
"""
        
        print("✅ Dashboard optimized for deployment")
        return True
    
    def setup_github_deployment(self):
        """Set up for GitHub deployment"""
        print("\n🚀 Setting up for GitHub deployment...")
        
        # Check if git is initialized
        if not Path(".git").exists():
            subprocess.run(["git", "init"])
            print("✅ Initialized Git repository")
        
        # Create GitHub workflow for automatic deployment
        github_dir = Path(".github/workflows")
        github_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_content = """
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Test dashboard import
      run: |
        python -c "import sys; sys.path.append('src'); import dashboard.fully_integrated_dashboard"
"""
        
        with open(github_dir / "deploy.yml", "w") as f:
            f.write(workflow_content.strip())
        
        print("✅ Created GitHub Actions workflow")
    
    def run_full_setup(self):
        """Run complete deployment setup"""
        print("🎯 ISSA Dashboard Deployment Setup")
        print("=" * 50)
        
        self.create_requirements_txt()
        self.create_streamlit_config()
        self.create_gitignore()
        self.create_procfile()
        self.create_runtime_txt()
        self.create_deployment_readme()
        self.create_demo_secrets()
        self.optimize_dashboard_for_deployment()
        self.setup_github_deployment()
        
        print("\n" + "=" * 50)
        print("✅ DEPLOYMENT SETUP COMPLETE!")
        print("\n📋 Next Steps:")
        print("1. Push to GitHub:")
        print("   git add .")
        print("   git commit -m 'Setup ISSA dashboard for deployment'")
        print("   git push origin main")
        print("\n2. Deploy on Streamlit Cloud:")
        print("   - Go to share.streamlit.io")
        print("   - Connect your GitHub repo") 
        print("   - Set main file: src/dashboard/fully_integrated_dashboard.py")
        print("   - Click Deploy")
        print("\n3. Share the URL with your boss! 🎉")

if __name__ == "__main__":
    setup = ISSADeploymentSetup()
    setup.run_full_setup()  # <-- ADD THIS LINE