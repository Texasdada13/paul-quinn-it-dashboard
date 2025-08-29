"""
Metric Registry System for Paul Quinn IT Dashboard
Automatically discovers and loads all metric modules
"""

import os
import importlib
import importlib.util
import pandas as pd
from pathlib import Path
import sys

class MetricRegistry:
    """Central registry for all dashboard metrics"""
    
    def __init__(self, base_path='src/metrics'):
        self.base_path = Path(base_path)
        self.metrics = {
            'cfo': {},
            'cio': {},
            'cto': {},
            'hbcu': {}
        }
        self._discover_metrics()
    
    def _discover_metrics(self):
        """Automatically discover all metric modules"""
        # Get the absolute path to the metrics directory
        current_file = Path(__file__).resolve()
        parent_dir = current_file.parent.parent  # Go up to src/
        metrics_dir = parent_dir / 'metrics'
        
        for persona in ['cfo', 'cio', 'cto']:
            persona_path = metrics_dir / persona
            if persona_path.exists():
                # Find all module files
                module_files = list(persona_path.glob('*_module.py'))
                
                for module_file in module_files:
                    # Remove the 'cfo_' prefix if it exists for the metric name
                    metric_name = module_file.stem.replace('_module', '')
                    
                    # Check for corresponding files
                    script_file = persona_path / f"{metric_name}_script.py"
                    csv_file = persona_path / f"{metric_name}_examples.csv"
                    
                    self.metrics[persona][metric_name] = {
                        'module_path': module_file,
                        'script_path': script_file if script_file.exists() else None,
                        'data_path': csv_file if csv_file.exists() else None,
                        'module': None,  # Will be loaded on demand
                        'data': None     # Will be loaded on demand
                    }
        
        # Handle HBCU metrics in separate folder
        hbcu_path = parent_dir / 'metrics' / 'hbcu'
        if hbcu_path.exists():
            module_files = list(hbcu_path.glob('*_module.py'))
            
            for module_file in module_files:
                metric_name = module_file.stem.replace('_module', '')
                
                script_file = hbcu_path / f"{metric_name}_script.py"
                csv_file = hbcu_path / f"{metric_name}_examples.csv"
                
                self.metrics['hbcu'][metric_name] = {
                    'module_path': module_file,
                    'script_path': script_file if script_file.exists() else None,
                    'data_path': csv_file if csv_file.exists() else None,
                    'module': None,
                    'data': None
                }
    
    def load_metric_module(self, persona, metric_name):
        """Load a specific metric module"""
        if metric_name not in self.metrics[persona]:
            return None
        
        metric_info = self.metrics[persona][metric_name]
        
        if metric_info['module'] is None and metric_info['module_path']:
            try:
                # Dynamic import of the module
                spec = importlib.util.spec_from_file_location(
                    f"{persona}.{metric_name}_module",
                    metric_info['module_path']
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                metric_info['module'] = module
            except Exception as e:
                print(f"Error loading module {metric_name}: {e}")
                return None
        
        return metric_info['module']
    
    def load_metric_data(self, persona, metric_name):
        """Load metric data from CSV"""
        if metric_name not in self.metrics[persona]:
            return None
        
        metric_info = self.metrics[persona][metric_name]
        
        if metric_info['data'] is None and metric_info['data_path']:
            try:
                metric_info['data'] = pd.read_csv(metric_info['data_path'])
            except Exception as e:
                print(f"Error loading data for {metric_name}: {e}")
                return None
        
        return metric_info['data']
    
    def get_available_metrics(self, persona):
        """Get list of available metrics for a persona"""
        return list(self.metrics.get(persona, {}).keys())
    
    def get_metric_info(self, persona, metric_name):
        """Get all information about a specific metric"""
        return self.metrics.get(persona, {}).get(metric_name, {})

# Specific metric loaders for CFO metrics
class CFOMetrics:
    """CFO-specific metric handlers"""
    
    def __init__(self, registry):
        self.registry = registry
    
    def get_budget_variance_data(self):
        """Load and process budget variance data"""
        # Try with the full name first
        data = self.registry.load_metric_data('cfo', 'cfo_budget_vs_actual')
        module = self.registry.load_metric_module('cfo', 'cfo_budget_vs_actual')
        
        if data is not None:
            # Add any additional processing
            if 'Variance Amount' in data.columns:
                data['Variance Amount'] = pd.to_numeric(data['Variance Amount'], errors='coerce')
            if 'Variance %' in data.columns:
                data['Variance %'] = data['Variance %'].str.rstrip(' %').astype(float) if data['Variance %'].dtype == 'object' else data['Variance %']
        
        return data, module
    
    def get_contract_alerts(self, days_threshold=90):
        """Load and process contract expiration alerts"""
        data = self.registry.load_metric_data('cfo', 'cfo_contract_expiration_alerts')
        module = self.registry.load_metric_module('cfo', 'cfo_contract_expiration_alerts')
        
        if data is not None:
            # Process dates
            if 'Contract End Date' in data.columns:
                data['Contract End Date'] = pd.to_datetime(data['Contract End Date'])
            if 'Days Until Expiry' in data.columns:
                data['Days Until Expiry'] = pd.to_numeric(data['Days Until Expiry'], errors='coerce')
            
            # Filter for alerts
            if 'Days Until Expiry' in data.columns:
                data['Alert Status'] = data['Days Until Expiry'].apply(
                    lambda x: 'Critical' if x < 30 else 'Warning' if x < days_threshold else 'OK'
                )
        
        return data, module
    
    def get_grant_compliance_data(self):
        """Load and process grant compliance data"""
        data = self.registry.load_metric_data('cfo', 'cfo_grant_compliance')
        module = self.registry.load_metric_module('cfo', 'cfo_grant_compliance')
        
        if data is not None:
            # Process compliance rate
            if 'Compliance Rate (%)' in data.columns:
                data['Compliance Rate (%)'] = pd.to_numeric(data['Compliance Rate (%)'], errors='coerce')
            if 'Risk of Fund Clawback' in data.columns:
                data['Risk Level'] = data['Risk of Fund Clawback']
            else:
                data['Risk Level'] = 'Unknown'
        
        return data, module
    
    def get_vendor_optimization_data(self):
        """Load vendor spend optimization data"""
        data = self.registry.load_metric_data('cfo', 'cfo_vendor_spend_optimization')
        module = self.registry.load_metric_module('cfo', 'cfo_vendor_spend_optimization')
        
        return data, module
    
    def get_student_success_roi(self):
        """Load student success ROI data"""
        data = self.registry.load_metric_data('cfo', 'cfo_student_success_roi')
        module = self.registry.load_metric_module('cfo', 'cfo_student_success_roi')
        
        return data, module

# Similar classes for CIO and CTO metrics
class CIOMetrics:
    """CIO-specific metric handlers"""
    
    def __init__(self, registry):
        self.registry = registry
    
    def get_digital_transformation_metrics(self):
        """Load digital transformation metrics"""
        data = self.registry.load_metric_data('cio', 'digital_transformation_metrics')
        module = self.registry.load_metric_module('cio', 'digital_transformation_metrics')
        return data, module
    
    def get_business_unit_spend(self):
        """Load business unit IT spend data"""
        data = self.registry.load_metric_data('cio', 'business_unit_it_spend')
        module = self.registry.load_metric_module('cio', 'business_unit_it_spend')
        return data, module
    
    def get_risk_metrics(self):
        """Load risk dashboard metrics"""
        data = self.registry.load_metric_data('cio', 'risk_metrics')
        module = self.registry.load_metric_module('cio', 'risk_metrics')
        return data, module

class CTOMetrics:
    """CTO-specific metric handlers"""
    
    def __init__(self, registry):
        self.registry = registry
    
    def get_cloud_optimization_metrics(self):
        """Load cloud cost optimization metrics"""
        data = self.registry.load_metric_data('cto', 'cloud_cost_optimization_metrics')
        module = self.registry.load_metric_module('cto', 'cloud_cost_optimization_metrics')
        return data, module
    
    def get_asset_lifecycle_metrics(self):
        """Load asset lifecycle management metrics"""
        data = self.registry.load_metric_data('cto', 'asset_lifecycle_management_metrics')
        module = self.registry.load_metric_module('cto', 'asset_lifecycle_management_metrics')
        return data, module
    
    def get_security_metrics(self):
        """Load security metrics and response data"""
        data = self.registry.load_metric_data('cto', 'security_metrics_and_response')
        module = self.registry.load_metric_module('cto', 'security_metrics_and_response')
        return data, module

# Utility functions for metric integration
def get_metric_summary(registry, persona):
    """Get a summary of all available metrics for a persona"""
    metrics = registry.get_available_metrics(persona)
    summary = []
    
    for metric in metrics:
        info = registry.get_metric_info(persona, metric)
        summary.append({
            'metric_name': metric,
            'has_module': info['module_path'] is not None,
            'has_data': info['data_path'] is not None,
            'has_script': info['script_path'] is not None
        })
    
    return pd.DataFrame(summary)

# Initialize the registry when imported
metric_registry = MetricRegistry()
cfo_metrics = CFOMetrics(metric_registry)
cio_metrics = CIOMetrics(metric_registry)
cto_metrics = CTOMetrics(metric_registry)