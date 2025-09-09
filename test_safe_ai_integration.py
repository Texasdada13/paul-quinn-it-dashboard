#!/usr/bin/env python3
"""Safe AI Integration Test"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ai_modules():
    try:
        from dashboard.ai_optimization_engine import OptimizationDashboard
        from dashboard.metric_intelligence import MetricIntelligenceEngine
        print("AI modules loaded successfully")
        return True
    except Exception as e:
        print(f"AI module test failed: {e}")
        return False

def main():
    print("Safe ISSA AI Integration Test")
    print("=============================")
    
    modules_ok = test_ai_modules()
    
    if modules_ok:
        print("All tests passed! AI integration successful.")
        print("Launch enhanced dashboard:")
        print("python -m streamlit run src/dashboard/withAI_Updates_fully_integrated_dashboard.py")
    else:
        print("Some tests failed. Please check the setup.")
    
    return 0 if modules_ok else 1

if __name__ == "__main__":
    exit(main())
