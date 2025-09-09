"""
Enhanced Metric Registry System for Paul Quinn IT Dashboard
Automatically discovers and loads all metric modules with data source integration
"""

import os
import importlib
import importlib.util
import pandas as pd
from pathlib import Path
import sys
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import data source components
try:
    current_dir = Path(__file__).parent.parent
    sys.path.append(str(current_dir))
    
    from integrations.data_connectors import DataSourceManager
    from integrations.file_processors import ContractFileProcessor
    from security.data_encryption import SecureDataHandler
    DATA_INTEGRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Data integration modules not available: {e}")
    DATA_INTEGRATION_AVAILABLE = False

class MetricRegistry:
    """Central registry for all dashboard metrics with data source integration"""
    
    def __init__(self, base_path='src/metrics'):
        self.base_path = Path(base_path)
        self.metrics = {
            'cfo': {},
            'cio': {},
            'cto': {},
            'pm': {},
            'hbcu': {}
        }
        
        # Data source integration
        if DATA_INTEGRATION_AVAILABLE:
            self.data_manager = DataSourceManager()
            self.file_processor = ContractFileProcessor()
            self.security_handler = SecureDataHandler()
        else:
            self.data_manager = None
            self.file_processor = None
            self.security_handler = None
        
        self._discover_metrics()
    
    def _discover_metrics(self):
        """Automatically discover all metric modules"""
        # Get the absolute path to the metrics directory
        current_file = Path(__file__).resolve()
        parent_dir = current_file.parent.parent  # Go up to src/
        metrics_dir = parent_dir / 'metrics'
        
        for persona in ['cfo', 'cio', 'cto', 'pm']:
            persona_path = metrics_dir / persona
            if persona_path.exists():
                # Find all module files
                module_files = list(persona_path.glob('*_module.py'))
                
                for module_file in module_files:
                    # Remove the persona prefix if it exists for the metric name
                    metric_name = module_file.stem.replace('_module', '')
                    if metric_name.startswith(f'{persona}_'):
                        metric_name = metric_name[len(f'{persona}_'):]
                    
                    # Check for corresponding files - handle space in filename
                    script_file = persona_path / f"{metric_name} script.py"
                    csv_file = persona_path / f"{metric_name}_examples.csv"
                    
                    # If script file with space doesn't exist, try without space
                    if not script_file.exists():
                        script_file = persona_path / f"{metric_name}_script.py"
                    
                    # Also try with persona prefix
                    if not csv_file.exists():
                        csv_file = persona_path / f"{persona}_{metric_name}_examples.csv"
                    
                    self.metrics[persona][metric_name] = {
                        'module_path': module_file,
                        'script_path': script_file if script_file.exists() else None,
                        'data_path': csv_file if csv_file.exists() else None,
                        'module': None,  # Will be loaded on demand
                        'data': None,    # Will be loaded on demand
                        'live_data_available': False,  # Will be updated based on data sources
                        'last_updated': None
                    }
        
        # Handle HBCU metrics in separate folder
        hbcu_path = parent_dir / 'metrics' / 'hbcu'
        if hbcu_path.exists():
            module_files = list(hbcu_path.glob('*_module.py'))
            
            for module_file in module_files:
                metric_name = module_file.stem.replace('_module', '')
                
                # Check for corresponding files - handle space in filename
                script_file = hbcu_path / f"{metric_name} script.py"
                csv_file = hbcu_path / f"{metric_name}_examples.csv"
                
                # If script file with space doesn't exist, try without space
                if not script_file.exists():
                    script_file = hbcu_path / f"{metric_name}_script.py"
                
                self.metrics['hbcu'][metric_name] = {
                    'module_path': module_file,
                    'script_path': script_file if script_file.exists() else None,
                    'data_path': csv_file if csv_file.exists() else None,
                    'module': None,
                    'data': None,
                    'live_data_available': False,
                    'last_updated': None
                }
        
        logger.info(f"Discovered metrics: {sum(len(persona_metrics) for persona_metrics in self.metrics.values())}")
    
    def register_data_source(self, name: str, connector):
        """Register a data source connector"""
        if self.data_manager:
            self.data_manager.register_connector(name, connector)
            logger.info(f"Registered data source: {name}")
    
    def get_live_data(self, persona: str, metric_name: str) -> Optional[pd.DataFrame]:
        """Get live data from integrated sources"""
        
        if not self.data_manager:
            return None
        
        try:
            # For contract-related metrics, get consolidated contract data
            if any(keyword in metric_name.lower() for keyword in ['contract', 'vendor', 'spend']):
                live_data = self.data_manager.get_consolidated_contract_data()
                
                if not live_data.empty:
                    # Update metric info
                    if persona in self.metrics and metric_name in self.metrics[persona]:
                        self.metrics[persona][metric_name]['live_data_available'] = True
                        self.metrics[persona][metric_name]['last_updated'] = datetime.now().isoformat()
                    
                    return live_data
        
        except Exception as e:
            logger.error(f"Failed to get live data for {persona}.{metric_name}: {e}")
        
        return None
    
    def load_metric_module(self, persona: str, metric_name: str):
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
                logger.error(f"Error loading module {metric_name}: {e}")
                return None
        
        return metric_info['module']
    
    def load_metric_data(self, persona: str, metric_name: str, prefer_live: bool = True) -> Optional[pd.DataFrame]:
        """
        Load metric data from live sources or CSV files
        
        Args:
            persona: The persona (cfo, cio, cto, etc.)
            metric_name: The metric name
            prefer_live: Whether to prefer live data over static files
            
        Returns:
            DataFrame with metric data or None if not available
        """
        
        if metric_name not in self.metrics[persona]:
            return None
        
        metric_info = self.metrics[persona][metric_name]
        
        # Try live data first if preferred and available
        if prefer_live and self.data_manager:
            live_data = self.get_live_data(persona, metric_name)
            if live_data is not None and not live_data.empty:
                logger.info(f"Using live data for {persona}.{metric_name}")
                return live_data
        
        # Fall back to cached data or CSV file
        if metric_info['data'] is None and metric_info['data_path']:
            try:
                metric_info['data'] = pd.read_csv(metric_info['data_path'])
                logger.info(f"Loaded CSV data for {persona}.{metric_name}")
            except Exception as e:
                logger.error(f"Error loading data for {metric_name}: {e}")
                return None
        
        return metric_info['data']
    
    def get_available_metrics(self, persona: str) -> List[str]:
        """Get list of available metrics for a persona"""
        return list(self.metrics.get(persona, {}).keys())
    
    def get_metric_info(self, persona: str, metric_name: str) -> Dict[str, Any]:
        """Get all information about a specific metric"""
        return self.metrics.get(persona, {}).get(metric_name, {})
    
    def refresh_live_data(self, persona: Optional[str] = None) -> Dict[str, bool]:
        """Refresh live data for all or specific persona metrics"""
        
        if not self.data_manager:
            return {}
        
        results = {}
        personas_to_refresh = [persona] if persona else self.metrics.keys()
        
        for p in personas_to_refresh:
            for metric_name in self.metrics.get(p, {}):
                try:
                    live_data = self.get_live_data(p, metric_name)
                    results[f"{p}.{metric_name}"] = live_data is not None and not live_data.empty
                except Exception as e:
                    logger.error(f"Failed to refresh {p}.{metric_name}: {e}")
                    results[f"{p}.{metric_name}"] = False
        
        return results
    
    def get_data_source_status(self) -> Dict[str, Any]:
        """Get status of all data sources"""
        
        if not self.data_manager:
            return {'status': 'Data integration not available'}
        
        return self.data_manager.get_data_source_status()
    
    def export_metrics_catalog(self, output_path: str = None) -> str:
        """Export complete metrics catalog"""
        
        if output_path is None:
            output_path = f"metrics_catalog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        catalog = {
            'generated_at': datetime.now().isoformat(),
            'data_integration_available': DATA_INTEGRATION_AVAILABLE,
            'total_metrics': sum(len(persona_metrics) for persona_metrics in self.metrics.values()),
            'personas': {}
        }
        
        for persona, metrics in self.metrics.items():
            catalog['personas'][persona] = {
                'metric_count': len(metrics),
                'metrics': {}
            }
            
            for metric_name, metric_info in metrics.items():
                catalog['personas'][persona]['metrics'][metric_name] = {
                    'has_module': metric_info['module_path'] is not None,
                    'has_data_file': metric_info['data_path'] is not None,
                    'has_script': metric_info['script_path'] is not None,
                    'live_data_available': metric_info['live_data_available'],
                    'last_updated': metric_info['last_updated']
                }
        
        import json
        with open(output_path, 'w') as f:
            json.dump(catalog, f, indent=2)
        
        logger.info(f"Metrics catalog exported to {output_path}")
        return output_path

# Enhanced persona-specific metric loaders
class CFOMetrics:
    """CFO-specific metric handlers with live data integration"""
    
    def __init__(self, registry: MetricRegistry):
        self.registry = registry
    
    def get_budget_variance_data(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load and process budget variance data"""
        
        # Try with full name first, then without prefix
        for metric_name in ['cfo_budget_vs_actual', 'budget_vs_actual']:
            data = self.registry.load_metric_data('cfo', metric_name, prefer_live)
            if data is not None:
                break
        else:
            return None, None
        
        module = self.registry.load_metric_module('cfo', metric_name)
        
        if data is not None:
            # Add any additional processing
            if 'Variance Amount' in data.columns:
                data['Variance Amount'] = pd.to_numeric(data['Variance Amount'], errors='coerce')
            if 'Variance %' in data.columns:
                # Handle percentage values that might be strings
                if data['Variance %'].dtype == 'object':
                    # Remove % sign and convert to float
                    data['Variance %'] = data['Variance %'].str.rstrip('%').astype(float)
                else:
                    data['Variance %'] = pd.to_numeric(data['Variance %'], errors='coerce')
        
        return data, module
    
    def get_contract_alerts(self, days_threshold: int = 90, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load and process contract expiration alerts"""
        
        # Try live data first if available
        if prefer_live:
            live_data = self.registry.get_live_data('cfo', 'contract_expiration_alerts')
            if live_data is not None and not live_data.empty:
                data = live_data
            else:
                # Fall back to static data
                data = self.registry.load_metric_data('cfo', 'contract_expiration_alerts', prefer_live=False)
        else:
            data = self.registry.load_metric_data('cfo', 'contract_expiration_alerts', prefer_live=False)
        
        module = self.registry.load_metric_module('cfo', 'contract_expiration_alerts')
        
        if data is not None:
            # Process dates
            if 'Contract End Date' in data.columns:
                data['Contract End Date'] = pd.to_datetime(data['Contract End Date'], errors='coerce')
            if 'Days Until Expiry' in data.columns:
                data['Days Until Expiry'] = pd.to_numeric(data['Days Until Expiry'], errors='coerce')
            else:
                # Calculate days until expiry if not present
                if 'Contract End Date' in data.columns:
                    today = pd.Timestamp.now()
                    data['Days Until Expiry'] = (data['Contract End Date'] - today).dt.days
            
            # Add alert status
            if 'Days Until Expiry' in data.columns:
                data['Alert Status'] = data['Days Until Expiry'].apply(
                    lambda x: 'Critical' if pd.notna(x) and x < 30 
                             else 'Warning' if pd.notna(x) and x < days_threshold 
                             else 'OK' if pd.notna(x) 
                             else 'Unknown'
                )
        
        return data, module
    
    def get_grant_compliance_data(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load and process grant compliance data"""
        data = self.registry.load_metric_data('cfo', 'grant_compliance', prefer_live)
        module = self.registry.load_metric_module('cfo', 'grant_compliance')
        
        if data is not None:
            # Process compliance rate
            if 'Compliance Rate (%)' in data.columns:
                data['Compliance Rate (%)'] = pd.to_numeric(data['Compliance Rate (%)'], errors='coerce')
            if 'Risk of Fund Clawback' in data.columns:
                data['Risk Level'] = data['Risk of Fund Clawback']
            else:
                data['Risk Level'] = 'Unknown'
        
        return data, module
    
    def get_vendor_optimization_data(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load vendor spend optimization data"""
        data = self.registry.load_metric_data('cfo', 'vendor_spend_optimization', prefer_live)
        module = self.registry.load_metric_module('cfo', 'vendor_spend_optimization')
        return data, module
    
    def get_student_success_roi(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load student success ROI data"""
        data = self.registry.load_metric_data('cfo', 'student_success_roi', prefer_live)
        module = self.registry.load_metric_module('cfo', 'student_success_roi')
        return data, module

# Similar enhanced classes for CIO, CTO, and PM metrics
class CIOMetrics:
    """CIO-specific metric handlers with live data integration"""
    
    def __init__(self, registry: MetricRegistry):
        self.registry = registry
    
    def get_digital_transformation_metrics(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load digital transformation metrics"""
        data = self.registry.load_metric_data('cio', 'digital_transformation_metrics', prefer_live)
        module = self.registry.load_metric_module('cio', 'digital_transformation_metrics')
        return data, module
    
    def get_business_unit_spend(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load business unit IT spend data"""
        data = self.registry.load_metric_data('cio', 'business_unit_it_spend', prefer_live)
        module = self.registry.load_metric_module('cio', 'business_unit_it_spend')
        return data, module
    
    def get_risk_metrics(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load risk dashboard metrics"""
        data = self.registry.load_metric_data('cio', 'risk_metrics', prefer_live)
        module = self.registry.load_metric_module('cio', 'risk_metrics')
        return data, module

class CTOMetrics:
    """CTO-specific metric handlers with live data integration"""
    
    def __init__(self, registry: MetricRegistry):
        self.registry = registry
    
    def get_cloud_optimization_metrics(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load cloud cost optimization metrics"""
        data = self.registry.load_metric_data('cto', 'cloud_cost_optimization_metrics', prefer_live)
        module = self.registry.load_metric_module('cto', 'cloud_cost_optimization_metrics')
        return data, module
    
    def get_asset_lifecycle_metrics(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load asset lifecycle management metrics"""
        data = self.registry.load_metric_data('cto', 'asset_lifecycle_management_metrics', prefer_live)
        module = self.registry.load_metric_module('cto', 'asset_lifecycle_management_metrics')
        return data, module
    
    def get_security_metrics(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load security metrics and response data"""
        data = self.registry.load_metric_data('cto', 'security_metrics_and_response', prefer_live)
        module = self.registry.load_metric_module('cto', 'security_metrics_and_response')
        return data, module

class PMMetrics:
    """Project Manager-specific metric handlers"""
    
    def __init__(self, registry: MetricRegistry):
        self.registry = registry
    
    def get_project_charter_metrics(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load project charter metrics"""
        data = self.registry.load_metric_data('pm', 'project_charter_metrics', prefer_live)
        module = self.registry.load_metric_module('pm', 'project_charter_metrics')
        return data, module
    
    def get_raid_log_metrics(self, prefer_live: bool = True) -> Tuple[Optional[pd.DataFrame], Any]:
        """Load RAID log metrics"""
        data = self.registry.load_metric_data('pm', 'raid_log_metrics', prefer_live)
        module = self.registry.load_metric_module('pm', 'raid_log_metrics')
        return data, module

# Utility functions for metric integration
def get_metric_summary(registry: MetricRegistry, persona: str) -> pd.DataFrame:
    """Get a summary of all available metrics for a persona"""
    metrics = registry.get_available_metrics(persona)
    summary = []
    
    for metric in metrics:
        info = registry.get_metric_info(persona, metric)
        summary.append({
            'metric_name': metric,
            'has_module': info['module_path'] is not None,
            'has_data': info['data_path'] is not None,
            'has_script': info['script_path'] is not None,
            'live_data_available': info['live_data_available'],
            'last_updated': info['last_updated']
        })
    
    return pd.DataFrame(summary)

def setup_data_sources(registry: MetricRegistry, config: Dict[str, Any]):
    """Setup data sources based on configuration"""
    
    if not DATA_INTEGRATION_AVAILABLE:
        logger.warning("Data integration not available")
        return
    
    # Setup SAP connector
    if config.get('sap', {}).get('enabled', False):
        from integrations.data_connectors import SAPContractConnector
        sap_config = config['sap']
        
        sap_connector = SAPContractConnector(
            base_url=sap_config['base_url'],
            client_id=sap_config['client_id'],
            client_secret=sap_config['client_secret']
        )
        registry.register_data_source('SAP', sap_connector)
    
    # Setup Paycom connector
    if config.get('paycom', {}).get('enabled', False):
        from integrations.data_connectors import PaycomHRConnector
        paycom_config = config['paycom']
        
        paycom_connector = PaycomHRConnector(
            api_key=paycom_config['api_key'],
            company_id=paycom_config['company_id']
        )
        registry.register_data_source('Paycom', paycom_connector)

# Initialize the enhanced registry when imported
metric_registry = MetricRegistry()
cfo_metrics = CFOMetrics(metric_registry)
cio_metrics = CIOMetrics(metric_registry)
cto_metrics = CTOMetrics(metric_registry)
pm_metrics = PMMetrics(metric_registry)

logger.info("Enhanced metric registry initialized with data source integration")