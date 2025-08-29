"""
Diagnostic script to check dashboard dependencies and file structure
Run this in the same directory as your dashboard
"""

import os
import sys
from pathlib import Path
import importlib.util

def check_file_structure():
    """Check if all required files and directories exist"""
    print("=" * 60)
    print("CHECKING FILE STRUCTURE")
    print("=" * 60)
    
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}\n")
    
    # Required files in root
    required_files = [
        'metric_registry.py',
        'dashboard_metric_loader.py',
        'hbcu_metrics_integration.py'
    ]
    
    print("📁 Checking root files:")
    for file in required_files:
        file_path = current_dir / file
        if file_path.exists():
            print(f"  ✅ {file} - Found")
        else:
            print(f"  ❌ {file} - NOT FOUND")
    
    # Check metrics directory structure
    print("\n📁 Checking metrics directory:")
    metrics_dir = current_dir / 'src' / 'metrics'
    if metrics_dir.exists():
        print(f"  ✅ src/metrics/ - Found")
        
        # Check persona subdirectories
        for persona in ['cfo', 'cio', 'cto', 'pm']:
            persona_dir = metrics_dir / persona
            if persona_dir.exists():
                metric_files = list(persona_dir.glob('*.py'))
                print(f"  ✅ {persona}/ - Found ({len(metric_files)} metrics)")
                if len(metric_files) > 0:
                    for metric_file in metric_files[:3]:  # Show first 3
                        print(f"      - {metric_file.name}")
                    if len(metric_files) > 3:
                        print(f"      ... and {len(metric_files) - 3} more")
            else:
                print(f"  ❌ {persona}/ - NOT FOUND")
    else:
        print(f"  ❌ src/metrics/ - NOT FOUND")

def test_imports():
    """Test if modules can be imported"""
    print("\n" + "=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    modules_to_test = [
        ('metric_registry', ['MetricRegistry', 'cfo_metrics', 'cio_metrics', 'cto_metrics']),
        ('dashboard_metric_loader', ['dashboard_loader', 'PM_METRICS_AVAILABLE', 'PM_METRICS']),
        ('hbcu_metrics_integration', ['HBCUMetricsIntegrator', 'integrate_hbcu_metrics_into_persona'])
    ]
    
    for module_name, expected_attrs in modules_to_test:
        print(f"\n📦 Testing {module_name}:")
        try:
            module = importlib.import_module(module_name)
            print(f"  ✅ Module imported successfully")
            
            for attr in expected_attrs:
                if hasattr(module, attr):
                    print(f"  ✅ {attr} - Found")
                else:
                    print(f"  ❌ {attr} - NOT FOUND in module")
                    
        except ImportError as e:
            print(f"  ❌ Failed to import: {e}")
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")

def test_metric_registry():
    """Test the metric registry functionality"""
    print("\n" + "=" * 60)
    print("TESTING METRIC REGISTRY")
    print("=" * 60)
    
    try:
        from metric_registry import metric_registry
        
        print("📊 Available metrics by persona:")
        for persona in ['cfo', 'cio', 'cto', 'pm']:
            metrics = metric_registry.get_available_metrics(persona)
            print(f"\n  {persona.upper()}: {len(metrics)} metrics")
            if metrics:
                for metric in metrics[:3]:  # Show first 3
                    print(f"    - {metric}")
                if len(metrics) > 3:
                    print(f"    ... and {len(metrics) - 3} more")
    except Exception as e:
        print(f"❌ Failed to test metric registry: {e}")

def test_streamlit():
    """Check if Streamlit and required packages are installed"""
    print("\n" + "=" * 60)
    print("TESTING REQUIRED PACKAGES")
    print("=" * 60)
    
    packages = ['streamlit', 'pandas', 'plotly', 'numpy']
    
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED (run: pip install {package})")

def suggest_fixes():
    """Suggest potential fixes based on findings"""
    print("\n" + "=" * 60)
    print("SUGGESTED FIXES")
    print("=" * 60)
    
    print("""
If you're seeing import errors:
1. Make sure all files are in the same directory as your dashboard
2. Check that Python path includes current directory:
   - Add to top of dashboard: sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

If metrics aren't loading:
3. Verify the src/metrics/ folder structure matches expected layout
4. Check that metric files have the correct naming convention
5. Ensure metric files have proper get_data() or render() functions

If you see 'Module not found' errors:
6. Install missing packages: pip install streamlit pandas plotly numpy

To quickly test the dashboard:
7. Run: streamlit run pqc_dashboard.py --server.port 8501

For a clean restart:
8. Clear Streamlit cache: streamlit cache clear
9. Then run the dashboard again
""")

if __name__ == "__main__":
    print("🔍 PAUL QUINN COLLEGE DASHBOARD DIAGNOSTIC")
    print("=" * 60)
    
    check_file_structure()
    test_imports()
    test_metric_registry()
    test_streamlit()
    suggest_fixes()
    
    print("\n" + "=" * 60)
    print("Diagnostic complete! Check the output above for issues.")
    print("=" * 60)