"""
Metric Intelligence Module - AI Enhancement Layer for ISSA
Provides intelligent analysis and predictions for all metric types
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
from dataclasses import dataclass
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MetricInsight:
    """Data class for metric insights"""
    metric_name: str
    persona: str
    insight_type: str  # 'trend', 'anomaly', 'prediction', 'optimization'
    message: str
    confidence: float
    impact_score: float
    recommended_actions: List[str]
    data_points: Dict[str, Any]

@dataclass
class OptimizationOpportunity:
    """Data class for optimization opportunities"""
    title: str
    description: str
    category: str
    potential_value: float
    implementation_effort: str  # 'Low', 'Medium', 'High'
    timeline: str
    confidence: float
    prerequisites: List[str]
    success_metrics: List[str]

class MetricIntelligenceEngine:
    """AI-powered intelligence engine for metric analysis"""
    
    def __init__(self):
        self.analysis_models = {
            'trend_analysis': self._analyze_trends,
            'anomaly_detection': self._detect_anomalies,
            'predictive_modeling': self._generate_predictions,
            'optimization_scoring': self._score_optimization_opportunities
        }
        
        # Intelligence thresholds
        self.thresholds = {
            'significant_variance': 0.15,  # 15% variance threshold
            'anomaly_z_score': 2.0,        # Z-score for anomaly detection
            'confidence_minimum': 0.6,     # Minimum confidence for recommendations
            'high_impact_threshold': 50000  # Dollar threshold for high impact
        }
        
        # Persona-specific intelligence weights
        self.persona_weights = {
            'cfo': {
                'cost_focus': 0.4,
                'risk_focus': 0.3,
                'compliance_focus': 0.2,
                'efficiency_focus': 0.1
            },
            'cio': {
                'strategic_focus': 0.35,
                'innovation_focus': 0.25,
                'alignment_focus': 0.25,
                'risk_focus': 0.15
            },
            'cto': {
                'operational_focus': 0.35,
                'efficiency_focus': 0.3,
                'security_focus': 0.2,
                'innovation_focus': 0.15
            },
            'pm': {
                'delivery_focus': 0.4,
                'resource_focus': 0.25,
                'quality_focus': 0.2,
                'stakeholder_focus': 0.15
            }
        }
    
    def analyze_metric(self, data: pd.DataFrame, persona: str, metric_name: str) -> List[MetricInsight]:
        """Generate comprehensive insights for a single metric"""
        
        insights = []
        
        if data is None or data.empty:
            return [MetricInsight(
                metric_name=metric_name,
                persona=persona,
                insight_type='data_quality',
                message="No data available for analysis",
                confidence=1.0,
                impact_score=0.0,
                recommended_actions=["Check data sources", "Verify data pipeline"],
                data_points={}
            )]
        
        try:
            # Run all analysis models
            for model_name, model_func in self.analysis_models.items():
                model_insights = model_func(data, persona, metric_name)
                insights.extend(model_insights)
            
            # Score and filter insights
            insights = self._score_insights(insights, persona)
            
            # Add persona-specific context
            insights = self._add_persona_context(insights, persona)
            
            return sorted(insights, key=lambda x: x.impact_score, reverse=True)
        
        except Exception as e:
            logger.error(f"Error analyzing metric {metric_name}: {e}")
            return [MetricInsight(
                metric_name=metric_name,
                persona=persona,
                insight_type='error',
                message=f"Analysis error: {str(e)}",
                confidence=0.0,
                impact_score=0.0,
                recommended_actions=["Review data format", "Check for data anomalies"],
                data_points={'error': str(e)}
            )]
    
    def _analyze_trends(self, data: pd.DataFrame, persona: str, metric_name: str) -> List[MetricInsight]:
        """Analyze trends in metric data"""
        insights = []
        
        # Find numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if len(data[col].dropna()) < 3:
                continue
                
            # Calculate trend
            values = data[col].dropna().values
            if len(values) >= 3:
                # Simple linear trend
                x = np.arange(len(values))
                trend = np.polyfit(x, values, 1)[0]
                
                # Determine trend significance
                trend_pct = (trend * len(values)) / np.mean(values) * 100
                
                if abs(trend_pct) > 5:  # 5% change threshold
                    trend_direction = "increasing" if trend > 0 else "decreasing"
                    impact = abs(trend_pct) / 10  # Scale to 0-10
                    
                    # Generate recommendations based on trend and persona
                    actions = self._generate_trend_actions(trend_direction, col, persona, trend_pct)
                    
                    insights.append(MetricInsight(
                        metric_name=metric_name,
                        persona=persona,
                        insight_type='trend',
                        message=f"{col} is {trend_direction} by {abs(trend_pct):.1f}% over time",
                        confidence=min(abs(trend_pct) / 20, 1.0),  # Higher change = higher confidence
                        impact_score=impact,
                        recommended_actions=actions,
                        data_points={
                            'column': col,
                            'trend_percentage': trend_pct,
                            'trend_direction': trend_direction,
                            'current_value': values[-1],
                            'trend_coefficient': trend
                        }
                    ))
        
        return insights
    
    def _detect_anomalies(self, data: pd.DataFrame, persona: str, metric_name: str) -> List[MetricInsight]:
        """Detect anomalies in metric data"""
        insights = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            values = data[col].dropna()
            
            if len(values) < 5:
                continue
            
            # Z-score based anomaly detection
            z_scores = np.abs((values - values.mean()) / values.std())
            anomalies = values[z_scores > self.thresholds['anomaly_z_score']]
            
            if len(anomalies) > 0:
                severity = "high" if z_scores.max() > 3 else "medium"
                
                actions = self._generate_anomaly_actions(col, persona, severity, anomalies.values)
                
                insights.append(MetricInsight(
                    metric_name=metric_name,
                    persona=persona,
                    insight_type='anomaly',
                    message=f"Detected {len(anomalies)} anomalies in {col} (severity: {severity})",
                    confidence=min(z_scores.max() / 4, 1.0),
                    impact_score=len(anomalies) * 2,  # More anomalies = higher impact
                    recommended_actions=actions,
                    data_points={
                        'column': col,
                        'anomaly_count': len(anomalies),
                        'max_z_score': z_scores.max(),
                        'anomaly_values': anomalies.tolist(),
                        'severity': severity
                    }
                ))
        
        return insights
    
    def _generate_predictions(self, data: pd.DataFrame, persona: str, metric_name: str) -> List[MetricInsight]:
        """Generate predictions for metric values"""
        insights = []
        
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            values = data[col].dropna()
            
            if len(values) < 4:
                continue
            
            try:
                # Simple linear prediction for next period
                x = np.arange(len(values))
                coeffs = np.polyfit(x, values, 1)
                predicted_next = coeffs[0] * len(values) + coeffs[1]
                
                current_value = values.iloc[-1] if len(values) > 0 else 0
                prediction_change = (predicted_next - current_value) / current_value * 100 if current_value != 0 else 0
                
                if abs(prediction_change) > 10:  # Significant predicted change
                    confidence = 1 / (1 + abs(prediction_change) / 50)  # Higher change = lower confidence
                    
                    actions = self._generate_prediction_actions(col, persona, prediction_change, predicted_next)
                    
                    insights.append(MetricInsight(
                        metric_name=metric_name,
                        persona=persona,
                        insight_type='prediction',
                        message=f"Predicted {prediction_change:+.1f}% change in {col} next period",
                        confidence=confidence,
                        impact_score=abs(prediction_change) / 5,
                        recommended_actions=actions,
                        data_points={
                            'column': col,
                            'current_value': current_value,
                            'predicted_value': predicted_next,
                            'prediction_change_pct': prediction_change,
                            'prediction_confidence': confidence
                        }
                    ))
            
            except Exception as e:
                logger.warning(f"Prediction failed for {col}: {e}")
                continue
        
        return insights
    
    def _score_optimization_opportunities(self, data: pd.DataFrame, persona: str, metric_name: str) -> List[MetricInsight]:
        """Identify optimization opportunities"""
        insights = []
        
        # Persona-specific optimization patterns
        if persona == 'cfo':
            insights.extend(self._identify_financial_optimizations(data, metric_name))
        elif persona == 'cio':
            insights.extend(self._identify_strategic_optimizations(data, metric_name))
        elif persona == 'cto':
            insights.extend(self._identify_operational_optimizations(data, metric_name))
        elif persona == 'pm':
            insights.extend(self._identify_project_optimizations(data, metric_name))
        
        return insights
    
    def _identify_financial_optimizations(self, data: pd.DataFrame, metric_name: str) -> List[MetricInsight]:
        """CFO-specific optimization opportunities"""
        insights = []
        
        # Look for cost reduction opportunities
        if 'cost' in metric_name.lower() or 'spend' in metric_name.lower() or 'budget' in metric_name.lower():
            
            # Find high-spend categories
            if 'Annual Spend' in data.columns or 'Budget' in data.columns:
                spend_col = 'Annual Spend' if 'Annual Spend' in data.columns else [col for col in data.columns if 'budget' in col.lower()][0] if any('budget' in col.lower() for col in data.columns) else None
                
                if spend_col and pd.api.types.is_numeric_dtype(data[spend_col]):
                    high_spend_threshold = data[spend_col].quantile(0.8)
                    high_spend_items = data[data[spend_col] > high_spend_threshold]
                    
                    potential_savings = high_spend_items[spend_col].sum() * 0.1  # Assume 10% optimization potential
                    
                    insights.append(MetricInsight(
                        metric_name=metric_name,
                        persona='cfo',
                        insight_type='optimization',
                        message=f"High-spend items identified with ${potential_savings:,.0f} optimization potential",
                        confidence=0.75,
                        impact_score=potential_savings / 10000,  # Scale to reasonable range
                        recommended_actions=[
                            "Review high-spend vendors for consolidation opportunities",
                            "Negotiate volume discounts for top spend categories", 
                            "Evaluate alternative solutions for cost optimization",
                            "Implement spend approval thresholds"
                        ],
                        data_points={
                            'high_spend_count': len(high_spend_items),
                            'total_high_spend': high_spend_items[spend_col].sum(),
                            'potential_savings': potential_savings,
                            'optimization_percentage': 10
                        }
                    ))
        
        return insights
    
    def _identify_strategic_optimizations(self, data: pd.DataFrame, metric_name: str) -> List[MetricInsight]:
        """CIO-specific optimization opportunities"""
        insights = []
        
        # Look for strategic alignment opportunities
        if 'digital' in metric_name.lower() or 'transformation' in metric_name.lower():
            insights.append(MetricInsight(
                metric_name=metric_name,
                persona='cio',
                insight_type='optimization',
                message="Digital transformation acceleration opportunity identified",
                confidence=0.7,
                impact_score=7.5,
                recommended_actions=[
                    "Prioritize high-ROI digital initiatives",
                    "Align technology roadmap with business strategy",
                    "Implement change management for digital adoption",
                    "Measure business value realization from digital investments"
                ],
                data_points={
                    'optimization_type': 'strategic_alignment',
                    'expected_roi_multiplier': 3.2
                }
            ))
        
        return insights
    
    def _identify_operational_optimizations(self, data: pd.DataFrame, metric_name: str) -> List[MetricInsight]:
        """CTO-specific optimization opportunities"""
        insights = []
        
        # Look for operational efficiency opportunities
        if 'infrastructure' in metric_name.lower() or 'system' in metric_name.lower():
            insights.append(MetricInsight(
                metric_name=metric_name,
                persona='cto',
                insight_type='optimization',
                message="Infrastructure optimization opportunity detected",
                confidence=0.8,
                impact_score=6.0,
                recommended_actions=[
                    "Implement automated monitoring and alerting",
                    "Optimize resource allocation and utilization",
                    "Consolidate redundant systems and processes",
                    "Deploy predictive maintenance capabilities"
                ],
                data_points={
                    'optimization_type': 'operational_efficiency',
                    'expected_efficiency_gain': 35
                }
            ))
        
        return insights
    
    def _identify_project_optimizations(self, data: pd.DataFrame, metric_name: str) -> List[MetricInsight]:
        """PM-specific optimization opportunities"""
        insights = []
        
        # Look for project delivery optimizations
        if 'project' in metric_name.lower() or 'delivery' in metric_name.lower():
            insights.append(MetricInsight(
                metric_name=metric_name,
                persona='pm',
                insight_type='optimization',
                message="Project delivery optimization opportunity identified",
                confidence=0.75,
                impact_score=5.5,
                recommended_actions=[
                    "Implement agile project management practices",
                    "Enhance stakeholder communication processes",
                    "Optimize resource allocation across projects",
                    "Deploy project analytics and reporting tools"
                ],
                data_points={
                    'optimization_type': 'delivery_efficiency',
                    'expected_time_savings': 20
                }
            ))
        
        return insights
    
    def _generate_trend_actions(self, direction: str, column: str, persona: str, trend_pct: float) -> List[str]:
        """Generate actions based on trend analysis"""
        actions = []
        
        if persona == 'cfo':
            if 'cost' in column.lower() or 'spend' in column.lower():
                if direction == 'increasing':
                    actions = [
                        "Investigate cost increase drivers",
                        "Implement cost control measures",
                        "Review vendor contracts for optimization",
                        "Consider budget reallocation strategies"
                    ]
                else:
                    actions = [
                        "Validate cost reduction sustainability",
                        "Document cost optimization best practices",
                        "Reallocate savings to strategic initiatives",
                        "Monitor for potential service impacts"
                    ]
        elif persona == 'cio':
            if direction == 'increasing':
                actions = [
                    "Assess strategic alignment of growth trend",
                    "Evaluate scalability requirements",
                    "Plan for increased capacity needs",
                    "Monitor business value delivery"
                ]
            else:
                actions = [
                    "Investigate decline causes",
                    "Assess impact on strategic objectives", 
                    "Consider intervention strategies",
                    "Review and adjust strategic roadmap"
                ]
        elif persona == 'cto':
            if direction == 'increasing':
                actions = [
                    "Monitor system capacity and performance",
                    "Plan infrastructure scaling",
                    "Optimize resource utilization",
                    "Implement automated monitoring"
                ]
            else:
                actions = [
                    "Investigate performance issues",
                    "Review system efficiency metrics",
                    "Plan capacity optimization",
                    "Update monitoring thresholds"
                ]
        
        return actions or ["Monitor trend continuation", "Analyze root causes", "Plan appropriate response"]
    
    def _generate_anomaly_actions(self, column: str, persona: str, severity: str, anomaly_values: np.ndarray) -> List[str]:
        """Generate actions for anomaly detection"""
        base_actions = [
            "Investigate root cause of anomalies",
            "Validate data accuracy and completeness",
            "Check for external factors or events"
        ]
        
        if severity == 'high':
            base_actions.extend([
                "Implement immediate monitoring",
                "Escalate to appropriate stakeholders",
                "Create detailed incident report"
            ])
        
        return base_actions
    
    def _generate_prediction_actions(self, column: str, persona: str, change_pct: float, predicted_value: float) -> List[str]:
        """Generate actions based on predictions"""
        actions = []
        
        if abs(change_pct) > 20:  # Significant change predicted
            if change_pct > 0:  # Increase predicted
                actions = [
                    "Prepare for anticipated increase",
                    "Plan resource scaling strategies",
                    "Monitor leading indicators",
                    "Update forecasting models"
                ]
            else:  # Decrease predicted
                actions = [
                    "Investigate potential decline causes",
                    "Develop mitigation strategies",
                    "Review current initiatives effectiveness",
                    "Plan corrective interventions"
                ]
        else:
            actions = [
                "Continue current monitoring",
                "Validate prediction accuracy over time",
                "Refine prediction models"
            ]
        
        return actions
    
    def _score_insights(self, insights: List[MetricInsight], persona: str) -> List[MetricInsight]:
        """Apply persona-specific scoring to insights"""
        
        weights = self.persona_weights.get(persona, self.persona_weights['cfo'])
        
        for insight in insights:
            # Adjust impact score based on persona priorities
            if insight.insight_type == 'optimization':
                if 'cost' in insight.message.lower():
                    insight.impact_score *= (1 + weights.get('cost_focus', 0))
                elif 'strategic' in insight.message.lower():
                    insight.impact_score *= (1 + weights.get('strategic_focus', 0))
                elif 'operational' in insight.message.lower():
                    insight.impact_score *= (1 + weights.get('operational_focus', 0))
            
            # Filter low-confidence insights
            if insight.confidence < self.thresholds['confidence_minimum']:
                insight.impact_score *= 0.5  # Reduce impact for low confidence
        
        return [i for i in insights if i.impact_score > 0.5]  # Filter very low impact
    
    def _add_persona_context(self, insights: List[MetricInsight], persona: str) -> List[MetricInsight]:
        """Add persona-specific context to insights"""
        
        context_mapping = {
            'cfo': "Financial Impact",
            'cio': "Strategic Alignment",
            'cto': "Operational Efficiency",
            'pm': "Project Delivery"
        }
        
        for insight in insights:
            # Add persona context to message
            context = context_mapping.get(persona, "Business")
            insight.message = f"[{context}] {insight.message}"
        
        return insights
    
    def generate_executive_summary(self, all_insights: Dict[str, List[MetricInsight]], persona: str) -> Dict[str, Any]:
        """Generate executive summary of insights across all metrics"""
        
        summary = {
            'total_insights': sum(len(insights) for insights in all_insights.values()),
            'high_impact_count': 0,
            'total_potential_value': 0,
            'top_recommendations': [],
            'risk_alerts': [],
            'optimization_opportunities': []
        }
        
        all_flat_insights = [insight for insights in all_insights.values() for insight in insights]
        
        # Calculate summary statistics
        for insight in all_flat_insights:
            if insight.impact_score > 7:
                summary['high_impact_count'] += 1
            
            # Extract potential value from data points
            potential_value = insight.data_points.get('potential_savings', 0)
            potential_value += insight.data_points.get('expected_benefit', 0)
            summary['total_potential_value'] += potential_value
            
            # Categorize insights
            if insight.insight_type == 'optimization':
                summary['optimization_opportunities'].append({
                    'metric': insight.metric_name,
                    'message': insight.message,
                    'impact': insight.impact_score,
                    'confidence': insight.confidence
                })
            elif insight.insight_type == 'anomaly' and insight.confidence > 0.8:
                summary['risk_alerts'].append({
                    'metric': insight.metric_name,
                    'message': insight.message,
                    'severity': insight.data_points.get('severity', 'medium')
                })
        
        # Top recommendations by impact
        top_insights = sorted(all_flat_insights, key=lambda x: x.impact_score, reverse=True)[:5]
        summary['top_recommendations'] = [
            {
                'message': insight.message,
                'actions': insight.recommended_actions[:2],  # Top 2 actions
                'impact': insight.impact_score,
                'confidence': f"{insight.confidence:.0%}"
            }
            for insight in top_insights
        ]
        
        return summary

# Integration helper functions
def analyze_single_metric(data: pd.DataFrame, persona: str, metric_name: str) -> List[MetricInsight]:
    """Standalone function to analyze a single metric"""
    engine = MetricIntelligenceEngine()
    return engine.analyze_metric(data, persona, metric_name)

def generate_optimization_recommendations(persona: str, all_metric_data: Dict[str, pd.DataFrame]) -> List[OptimizationOpportunity]:
    """Generate optimization recommendations across all metrics for a persona"""
    engine = MetricIntelligenceEngine()
    
    all_insights = {}
    for metric_name, data in all_metric_data.items():
        if data is not None:
            all_insights[metric_name] = engine.analyze_metric(data, persona, metric_name)
    
    # Convert insights to optimization opportunities
    opportunities = []
    for metric_name, insights in all_insights.items():
        for insight in insights:
            if insight.insight_type == 'optimization' and insight.impact_score > 5:
                opportunity = OptimizationOpportunity(
                    title=insight.message.replace(f'[{persona.upper()}] ', ''),
                    description=f"Based on analysis of {metric_name}: {insight.message}",
                    category=insight.data_points.get('optimization_type', 'General'),
                    potential_value=insight.data_points.get('potential_savings', insight.impact_score * 1000),
                    implementation_effort='Medium',  # Default, could be enhanced
                    timeline='3-6 months',  # Default, could be enhanced
                    confidence=insight.confidence,
                    prerequisites=["Data validation", "Stakeholder approval"],
                    success_metrics=["Cost reduction", "Efficiency improvement"]
                )
                opportunities.append(opportunity)
    
    return sorted(opportunities, key=lambda x: x.potential_value, reverse=True)

# Example usage and testing functions
def test_intelligence_engine():
    """Test the intelligence engine with sample data"""
    
    # Create sample data
    sample_data = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=12, freq='M'),
        'Budget': [100000, 95000, 110000, 105000, 98000, 120000, 115000, 108000, 125000, 118000, 130000, 122000],
        'Actual_Spend': [98000, 102000, 108000, 112000, 95000, 118000, 121000, 105000, 128000, 115000, 135000, 125000],
        'Vendor_Count': [15, 15, 16, 16, 14, 17, 17, 16, 18, 17, 19, 18]
    })
    
    engine = MetricIntelligenceEngine()
    
    # Test with different personas
    for persona in ['cfo', 'cio', 'cto']:
        print(f"\n=== Testing {persona.upper()} Persona ===")
        insights = engine.analyze_metric(sample_data, persona, 'budget_analysis')
        
        for insight in insights[:3]:  # Show top 3 insights
            print(f"\nInsight Type: {insight.insight_type}")
            print(f"Message: {insight.message}")
            print(f"Confidence: {insight.confidence:.2f}")
            print(f"Impact Score: {insight.impact_score:.1f}")
            print(f"Recommended Actions: {insight.recommended_actions[:2]}")

if __name__ == "__main__":
    test_intelligence_engine()