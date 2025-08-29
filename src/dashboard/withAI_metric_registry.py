"""
Metric Registry System for Paul Quinn IT Dashboard
Automatically discovers and loads all metric modules
Enhanced with AI Intelligence and Optimization Engine Integration
"""

import os
import importlib
import importlib.util
import pandas as pd
from pathlib import Path
import sys

# AI Intelligence imports
try:
    from metric_intelligence import MetricIntelligenceEngine, MetricInsight, analyze_single_metric
    from ai_optimization_engine import AIOptimizationEngine
    AI_INTELLIGENCE_AVAILABLE = True
    print("AI intelligence features loaded successfully")
except ImportError as e:
    print(f"AI intelligence not available: {e}")
    AI_INTELLIGENCE_AVAILABLE = False


class AIEnhancedMetricRegistry:
    """Enhanced registry with AI optimization capabilities"""
    
    def __init__(self, base_path='src/metrics'):
        self.base_path = Path(base_path)
        self.metrics = {
            'cfo': {},
            'cio': {},
            'cto': {},
            'hbcu': {}
        }
        
        # Initialize AI components if available
        if AI_INTELLIGENCE_AVAILABLE:
            try:
                self.ai_engine = AIOptimizationEngine()
                self.intelligence_engine = MetricIntelligenceEngine()
                print("AI optimization engine initialized")
            except Exception as e:
                print(f"Warning: AI engine initialization failed: {e}")
                self.ai_engine = None
                self.intelligence_engine = None
        else:
            self.ai_engine = None
            self.intelligence_engine = None
        
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
                    
                    # Check for corresponding files - handle space in filename
                    script_file = persona_path / f"{metric_name} script.py"
                    csv_file = persona_path / f"{metric_name}_examples.csv"
                    
                    # If script file with space doesn't exist, try without space
                    if not script_file.exists():
                        script_file = persona_path / f"{metric_name}_script.py"
                    
                    self.metrics[persona][metric_name] = {
                        'module_path': module_file,
                        'script_path': script_file if script_file.exists() else None,
                        'data_path': csv_file if csv_file.exists() else None,
                        'module': None,  # Will be loaded on demand
                        'data': None,    # Will be loaded on demand
                        'ai_insights': None,  # AI analysis cache
                        'last_ai_analysis': None  # Timestamp of last AI analysis
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
                    'ai_insights': None,
                    'last_ai_analysis': None
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
        """Load metric data from CSV with AI enhancement"""
        if metric_name not in self.metrics[persona]:
            return None
        
        metric_info = self.metrics[persona][metric_name]
        
        if metric_info['data'] is None and metric_info['data_path']:
            try:
                metric_info['data'] = pd.read_csv(metric_info['data_path'])
                
                # Trigger AI analysis if available
                if self.intelligence_engine and metric_info['data'] is not None:
                    try:
                        ai_insights = self.intelligence_engine.analyze_metric(
                            metric_info['data'], persona, metric_name
                        )
                        metric_info['ai_insights'] = ai_insights
                        metric_info['last_ai_analysis'] = pd.Timestamp.now()
                    except Exception as e:
                        print(f"AI analysis failed for {metric_name}: {e}")
                
            except Exception as e:
                print(f"Error loading data for {metric_name}: {e}")
                return None
        
        return metric_info['data']
    
    def get_ai_insights(self, persona, metric_name):
        """Get AI-powered insights for any metric"""
        if not AI_INTELLIGENCE_AVAILABLE or not self.intelligence_engine:
            return None
        
        data = self.load_metric_data(persona, metric_name)
        if data is None:
            return None
        
        metric_info = self.metrics.get(persona, {}).get(metric_name, {})
        
        # Return cached insights if available and recent
        if metric_info.get('ai_insights') and metric_info.get('last_ai_analysis'):
            # Check if analysis is less than 1 hour old
            if (pd.Timestamp.now() - metric_info['last_ai_analysis']).total_seconds() < 3600:
                return metric_info['ai_insights']
        
        # Generate new AI insights
        try:
            insights = self.intelligence_engine.analyze_metric(data, persona, metric_name)
            metric_info['ai_insights'] = insights
            metric_info['last_ai_analysis'] = pd.Timestamp.now()
            return insights
        except Exception as e:
            print(f"Error generating AI insights for {metric_name}: {e}")
            return None
    
    def get_optimization_opportunities(self, persona):
        """Get all optimization opportunities for a persona"""
        if not AI_INTELLIGENCE_AVAILABLE or not self.ai_engine:
            return {}
        
        all_data = {}
        for metric in self.get_available_metrics(persona):
            data = self.load_metric_data(persona, metric)
            if data is not None:
                all_data[metric] = data
        
        if not all_data:
            return {}
        
        try:
            return self.ai_engine.generate_optimization_recommendations(persona, all_data)
        except Exception as e:
            print(f"Error generating optimization opportunities for {persona}: {e}")
            return {}
    
    def get_persona_ai_summary(self, persona):
        """Get AI-powered summary for entire persona"""
        if not AI_INTELLIGENCE_AVAILABLE:
            return None
        
        try:
            all_metrics = self.get_available_metrics(persona)
            summary = {
                'total_metrics': len(all_metrics),
                'metrics_with_data': 0,
                'ai_insights_count': 0,
                'optimization_opportunities': 0,
                'key_recommendations': []
            }
            
            for metric in all_metrics:
                data = self.load_metric_data(persona, metric)
                if data is not None:
                    summary['metrics_with_data'] += 1
                    
                    insights = self.get_ai_insights(persona, metric)
                    if insights:
                        summary['ai_insights_count'] += 1
            
            # Get optimization opportunities
            opportunities = self.get_optimization_opportunities(persona)
            if opportunities:
                summary['optimization_opportunities'] = len(opportunities.get('recommendations', []))
                summary['key_recommendations'] = opportunities.get('recommendations', [])[:3]
            
            return summary
        except Exception as e:
            print(f"Error generating AI summary for {persona}: {e}")
            return None
    
    def get_available_metrics(self, persona):
        """Get list of available metrics for a persona"""
        return list(self.metrics.get(persona, {}).keys())
    
    def get_metric_info(self, persona, metric_name):
        """Get all information about a specific metric"""
        return self.metrics.get(persona, {}).get(metric_name, {})


# Enhanced CFO Metrics with AI capabilities
class AIEnhancedCFOMetrics:
    """CFO-specific metric handlers with AI enhancement"""
    
    def __init__(self, registry):
        self.registry = registry
    
    def get_budget_variance_data(self):
        """Load and process budget variance data with AI insights"""
        data = self.registry.load_metric_data('cfo', 'cfo_budget_vs_actual')
        module = self.registry.load_metric_module('cfo', 'cfo_budget_vs_actual')
        
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
            
            # Add AI-powered variance prediction if available
            if AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
                try:
                    ai_prediction = self.registry.ai_engine.predict_budget_variance(data)
                    if ai_prediction:
                        data['AI_Predicted_Variance'] = ai_prediction.get('predicted_variance', 0)
                        data['AI_Risk_Score'] = ai_prediction.get('risk_score', 0)
                except Exception as e:
                    print(f"AI prediction failed for budget variance: {e}")
        
        return data, module
    
    def get_contract_alerts(self, days_threshold=90):
        """Load and process contract expiration alerts with AI optimization"""
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
            
            # Add AI-powered contract optimization recommendations
            if AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
                try:
                    ai_recommendations = self.registry.ai_engine.analyze_contract_portfolio(data)
                    if ai_recommendations:
                        # Add consolidation opportunities
                        data['AI_Consolidation_Opportunity'] = ai_recommendations.get('consolidation_flags', [False] * len(data))
                        data['AI_Negotiation_Priority'] = ai_recommendations.get('negotiation_priority', [0] * len(data))
                except Exception as e:
                    print(f"AI contract analysis failed: {e}")
        
        return data, module
    
    def get_grant_compliance_data(self):
        """Load and process grant compliance data with AI risk assessment"""
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
            
            # Add AI-powered compliance risk prediction
            if AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
                try:
                    ai_compliance = self.registry.ai_engine.assess_compliance_risk(data)
                    if ai_compliance:
                        data['AI_Risk_Prediction'] = ai_compliance.get('risk_scores', [0] * len(data))
                        data['AI_Recommended_Actions'] = ai_compliance.get('recommended_actions', ['Monitor'] * len(data))
                except Exception as e:
                    print(f"AI compliance analysis failed: {e}")
        
        return data, module
    
    def get_ai_financial_optimization(self):
        """Get comprehensive AI-driven financial optimization recommendations"""
        if not AI_INTELLIGENCE_AVAILABLE or not self.registry.ai_engine:
            return None
        
        try:
            # Gather all CFO data
            budget_data, _ = self.get_budget_variance_data()
            contract_data, _ = self.get_contract_alerts()
            grant_data, _ = self.get_grant_compliance_data()
            
            cfo_dataset = {
                'budget': budget_data,
                'contracts': contract_data,
                'grants': grant_data
            }
            
            # Generate comprehensive optimization recommendations
            optimization = self.registry.ai_engine.generate_financial_optimization(cfo_dataset)
            return optimization
        except Exception as e:
            print(f"Error generating AI financial optimization: {e}")
            return None
    
    def get_vendor_optimization_data(self):
        """Load vendor spend optimization data with AI insights"""
        data = self.registry.load_metric_data('cfo', 'cfo_vendor_spend_optimization')
        module = self.registry.load_metric_module('cfo', 'cfo_vendor_spend_optimization')
        
        return data, module
    
    def get_student_success_roi(self):
        """Load student success ROI data with AI impact analysis"""
        data = self.registry.load_metric_data('cfo', 'cfo_student_success_roi')
        module = self.registry.load_metric_module('cfo', 'cfo_student_success_roi')
        
        return data, module


# Enhanced CIO Metrics with AI capabilities
class AIEnhancedCIOMetrics:
    """CIO-specific metric handlers with AI strategic analysis"""
    
    def __init__(self, registry):
        self.registry = registry
    
    def get_digital_transformation_metrics(self):
        """Load digital transformation metrics with AI roadmap suggestions"""
        data = self.registry.load_metric_data('cio', 'digital_transformation_metrics')
        module = self.registry.load_metric_module('cio', 'digital_transformation_metrics')
        
        if data is not None and AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
            try:
                ai_roadmap = self.registry.ai_engine.optimize_digital_transformation(data)
                if ai_roadmap:
                    data['AI_Priority_Score'] = ai_roadmap.get('priority_scores', [0] * len(data))
                    data['AI_ROI_Prediction'] = ai_roadmap.get('roi_predictions', [0] * len(data))
            except Exception as e:
                print(f"AI digital transformation analysis failed: {e}")
        
        return data, module
    
    def get_business_unit_spend(self):
        """Load business unit IT spend data with AI allocation optimization"""
        data = self.registry.load_metric_data('cio', 'business_unit_it_spend')
        module = self.registry.load_metric_module('cio', 'business_unit_it_spend')
        
        if data is not None and AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
            try:
                ai_allocation = self.registry.ai_engine.optimize_business_unit_allocation(data)
                if ai_allocation:
                    data['AI_Optimization_Flag'] = ai_allocation.get('optimization_flags', [False] * len(data))
                    data['AI_Recommended_Allocation'] = ai_allocation.get('recommended_allocations', [0] * len(data))
            except Exception as e:
                print(f"AI business unit analysis failed: {e}")
        
        return data, module
    
    def get_risk_metrics(self):
        """Load risk dashboard metrics with AI risk scoring"""
        data = self.registry.load_metric_data('cio', 'risk_metrics')
        module = self.registry.load_metric_module('cio', 'risk_metrics')
        
        return data, module
    
    def get_ai_strategic_recommendations(self):
        """Get AI-powered strategic recommendations for CIO"""
        if not AI_INTELLIGENCE_AVAILABLE or not self.registry.ai_engine:
            return None
        
        try:
            # Gather all CIO strategic data
            digital_data, _ = self.get_digital_transformation_metrics()
            business_data, _ = self.get_business_unit_spend()
            risk_data, _ = self.get_risk_metrics()
            
            cio_dataset = {
                'digital_transformation': digital_data,
                'business_units': business_data,
                'risks': risk_data
            }
            
            # Generate strategic recommendations
            recommendations = self.registry.ai_engine.generate_strategic_recommendations(cio_dataset)
            return recommendations
        except Exception as e:
            print(f"Error generating AI strategic recommendations: {e}")
            return None


# Enhanced CTO Metrics with AI capabilities  
class AIEnhancedCTOMetrics:
    """CTO-specific metric handlers with AI operational optimization"""
    
    def __init__(self, registry):
        self.registry = registry
    
    def get_cloud_optimization_metrics(self):
        """Load cloud cost optimization metrics with AI right-sizing recommendations"""
        data = self.registry.load_metric_data('cto', 'cloud_cost_optimization_metrics')
        module = self.registry.load_metric_module('cto', 'cloud_cost_optimization_metrics')
        
        if data is not None and AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
            try:
                ai_optimization = self.registry.ai_engine.optimize_cloud_resources(data)
                if ai_optimization:
                    data['AI_Right_Size_Recommendation'] = ai_optimization.get('right_sizing', ['No Change'] * len(data))
                    data['AI_Potential_Savings'] = ai_optimization.get('potential_savings', [0] * len(data))
            except Exception as e:
                print(f"AI cloud optimization failed: {e}")
        
        return data, module
    
    def get_asset_lifecycle_metrics(self):
        """Load asset lifecycle management metrics with AI replacement predictions"""
        data = self.registry.load_metric_data('cto', 'asset_lifecycle_management_metrics')
        module = self.registry.load_metric_module('cto', 'asset_lifecycle_management_metrics')
        
        if data is not None and AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
            try:
                ai_lifecycle = self.registry.ai_engine.predict_asset_lifecycle(data)
                if ai_lifecycle:
                    data['AI_Replacement_Timeline'] = ai_lifecycle.get('replacement_timeline', ['Unknown'] * len(data))
                    data['AI_Risk_Score'] = ai_lifecycle.get('risk_scores', [0] * len(data))
            except Exception as e:
                print(f"AI asset lifecycle analysis failed: {e}")
        
        return data, module
    
    def get_security_metrics(self):
        """Load security metrics and response data with AI threat analysis"""
        data = self.registry.load_metric_data('cto', 'security_metrics_and_response')
        module = self.registry.load_metric_module('cto', 'security_metrics_and_response')
        
        if data is not None and AI_INTELLIGENCE_AVAILABLE and self.registry.ai_engine:
            try:
                ai_security = self.registry.ai_engine.analyze_security_posture(data)
                if ai_security:
                    data['AI_Threat_Level'] = ai_security.get('threat_levels', ['Low'] * len(data))
                    data['AI_Recommended_Actions'] = ai_security.get('recommended_actions', ['Monitor'] * len(data))
            except Exception as e:
                print(f"AI security analysis failed: {e}")
        
        return data, module
    
    def get_ai_operational_optimization(self):
        """Get comprehensive AI-driven operational optimization recommendations"""
        if not AI_INTELLIGENCE_AVAILABLE or not self.registry.ai_engine:
            return None
        
        try:
            # Gather all CTO operational data
            cloud_data, _ = self.get_cloud_optimization_metrics()
            asset_data, _ = self.get_asset_lifecycle_metrics()
            security_data, _ = self.get_security_metrics()
            
            cto_dataset = {
                'cloud': cloud_data,
                'assets': asset_data,
                'security': security_data
            }
            
            # Generate operational optimization recommendations
            optimization = self.registry.ai_engine.generate_operational_optimization(cto_dataset)
            return optimization
        except Exception as e:
            print(f"Error generating AI operational optimization: {e}")
            return None


# Utility functions for AI-enhanced metric integration
def get_ai_enhanced_metric_summary(registry, persona):
    """Get a summary of all available metrics for a persona with AI insights"""
    metrics = registry.get_available_metrics(persona)
    summary = []
    
    for metric in metrics:
        info = registry.get_metric_info(persona, metric)
        ai_insights = registry.get_ai_insights(persona, metric) if AI_INTELLIGENCE_AVAILABLE else None
        
        summary.append({
            'metric_name': metric,
            'has_module': info['module_path'] is not None,
            'has_data': info['data_path'] is not None,
            'has_script': info['script_path'] is not None,
            'has_ai_insights': ai_insights is not None,
            'ai_score': ai_insights.confidence_score if ai_insights else 0
        })
    
    return pd.DataFrame(summary)


# Initialize the enhanced registry when imported
try:
    metric_registry = AIEnhancedMetricRegistry()
    cfo_metrics = AIEnhancedCFOMetrics(metric_registry)
    cio_metrics = AIEnhancedCIOMetrics(metric_registry)
    cto_metrics = AIEnhancedCTOMetrics(metric_registry)
    
    print("AI-Enhanced Metric Registry initialized successfully")
    if AI_INTELLIGENCE_AVAILABLE:
        print("AI intelligence features are active")
    else:
        print("Running in compatibility mode without AI features")
        
except Exception as e:
    print(f"Error initializing AI-Enhanced Metric Registry: {e}")
    # Fallback to basic registry
    from metric_registry import MetricRegistry, CFOMetrics, CIOMetrics, CTOMetrics
    metric_registry = MetricRegistry()
    cfo_metrics = CFOMetrics(metric_registry)
    cio_metrics = CIOMetrics(metric_registry)
    cto_metrics = CTOMetrics(metric_registry)