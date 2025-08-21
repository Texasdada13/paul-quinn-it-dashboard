# Creating comprehensive Run/Grow/Transform framework with extensive calculations
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("CIO RUN/GROW/TRANSFORM PORTFOLIO FRAMEWORK - COMPREHENSIVE BREAKDOWN")
print("=" * 80)
print()

# 1. Core Framework Definitions with Industry Standards
rgt_framework = {
    'Category': ['RUN', 'GROW', 'TRANSFORM'],
    'Definition': [
        'Keep the lights on - maintain current business operations',
        'Enhance existing capabilities - drive organic growth', 
        'Enable new business models - breakthrough innovation'
    ],
    'Industry_Benchmark_Low': [60, 15, 5],
    'Industry_Benchmark_High': [85, 35, 25],
    'Optimal_Range_HBCU': [65, 25, 15],  # Optimized for higher education
    'Risk_Level': ['Low', 'Medium', 'High'],
    'ROI_Timeline': ['Immediate', '6-18 months', '2-5 years'],
    'Business_Impact': ['Operational Continuity', 'Competitive Advantage', 'Market Disruption']
}

df_rgt_framework = pd.DataFrame(rgt_framework)
print("1. RUN/GROW/TRANSFORM FRAMEWORK DEFINITIONS")
print("-" * 50)
print(df_rgt_framework.to_string(index=False))

print("\n\n2. DETAILED CATEGORIZATION CRITERIA")
print("-" * 50)

# 2. Detailed categorization with scoring matrix
categorization_criteria = {
    'RUN_Criteria': [
        'Infrastructure maintenance and operations',
        'Security, compliance, and regulatory requirements', 
        'Application maintenance and support',
        'Business continuity and disaster recovery',
        'Help desk and user support services',
        'License renewals for existing systems',
        'Routine upgrades and patches',
        'Data backup and storage management'
    ],
    'GROW_Criteria': [
        'Process optimization and automation',
        'Capacity expansion of existing systems',
        'Integration of acquired systems',
        'Performance improvements and optimization',
        'User experience enhancements',
        'Workflow modernization projects',
        'Efficiency-driven technology upgrades',
        'Cost reduction through consolidation'
    ],
    'TRANSFORM_Criteria': [
        'New business model enablement',
        'Digital product/service creation',
        'Emerging technology adoption (AI, ML, IoT)',
        'New market entry capabilities',
        'Student/customer experience transformation',
        'Data monetization initiatives',
        'Platform modernization (cloud-native)',
        'Innovation labs and R&D projects'
    ]
}

for category, criteria in categorization_criteria.items():
    print(f"\n{category.replace('_', ' ')}:")
    for i, criterion in enumerate(criteria, 1):
        print(f"  {i}. {criterion}")

# 3. Comprehensive Metrics and KPIs
print("\n\n3. KEY METRICS & KPIs FOR RGT PORTFOLIO ANALYSIS")
print("-" * 60)

rgt_metrics = {
    'Metric_Category': [
        'Portfolio Balance', 'Portfolio Balance', 'Portfolio Balance',
        'Financial Analysis', 'Financial Analysis', 'Financial Analysis', 'Financial Analysis',
        'Strategic Alignment', 'Strategic Alignment', 'Strategic Alignment',
        'Risk Assessment', 'Risk Assessment', 'Risk Assessment',
        'Performance Tracking', 'Performance Tracking', 'Performance Tracking',
        'Value Realization', 'Value Realization', 'Value Realization'
    ],
    'Specific_Metric': [
        'RGT Spend Distribution %',
        'RGT Portfolio Drift',
        'RGT Balance Score',
        'Cost per Category ($/FTE)',
        'ROI by Category',
        'Budget Variance by Category',
        'Total Cost of Ownership (TCO)',
        'Strategic Initiative Alignment %',
        'Business Capability Coverage',
        'Innovation Index',
        'Portfolio Risk Score',
        'Technology Debt by Category',
        'Compliance Gap Analysis',
        'Project Success Rate by Category',
        'Time to Value by Category',
        'Delivery Velocity by Category',
        'Benefits Realization %',
        'Business Impact Score',
        'Stakeholder Satisfaction'
    ],
    'Calculation_Formula': [
        '(Category Spend / Total IT Spend) * 100',
        '|Current % - Target %| for each category',
        'Weighted score based on optimal balance targets',
        'Category Total Spend / Full-Time Equivalents',
        '(Financial Benefits - Investment) / Investment * 100',
        '(Actual Spend - Budget) / Budget * 100',
        'Initial Cost + Operating Cost + End-of-Life Cost',
        '(Aligned Projects / Total Projects) * 100',
        '(Supported Capabilities / Total Capabilities) * 100',
        'New Tech Adoption Rate + R&D Investment %',
        'Risk Score = Σ(Impact × Probability × Category Weight)',
        'Technical Debt Cost / Category Total Cost',
        '(Met Requirements / Total Requirements) * 100',
        '(Successful Projects / Total Projects) * 100',
        'Average time from project start to benefit realization',
        'Story points or features delivered per sprint/cycle',
        '(Realized Benefits / Planned Benefits) * 100',
        'Weighted impact on strategic objectives (1-10 scale)',
        'Average satisfaction score from business stakeholders'
    ],
    'Target_Benchmark': [
        'Run: 65%, Grow: 25%, Transform: 15% (HBCU optimized)',
        '<5% deviation from target allocation',
        '>8.0/10.0 portfolio balance score',
        'Benchmark against peer institutions',
        'Run: 5-15%, Grow: 15-25%, Transform: >20%',
        '±10% variance acceptable, <5% optimal',
        'Minimize while maintaining quality/performance',
        '>80% of projects aligned with strategy',
        '>90% of critical capabilities supported',
        '>15% of total IT spend on innovation',
        '<7.0/10.0 overall portfolio risk',
        '<20% of category spend on tech debt',
        '>95% compliance across all categories',
        'Run: >95%, Grow: >85%, Transform: >60%',
        'Run: <6 months, Grow: <12 months, Transform: <24 months',
        'Continuous improvement trajectory',
        '>90% of planned benefits realized within 2 years',
        '>7.5/10.0 average business impact',
        '>4.0/5.0 stakeholder satisfaction'
    ],
    'Alert_Thresholds': [
        'Run >80% or <50%, Transform <5% or >30%',
        '>10% deviation from target',
        '<6.0/10.0 balance score',
        '>150% of peer average cost per FTE',
        'Run <5%, Grow <10%, Transform <15% ROI',
        '>15% budget variance',
        'TCO growth >20% year-over-year',
        '<70% strategic alignment',
        '<80% capability coverage',
        '<10% innovation spending',
        '>8.0/10.0 risk score',
        '>30% tech debt ratio',
        '<90% compliance score',
        'Success rate declining >10% year-over-year',
        'Time to value increasing >25%',
        'Velocity declining >15% quarter-over-quarter',
        '<75% benefits realization',
        '<6.0/10.0 business impact',
        '<3.5/5.0 satisfaction'
    ]
}

df_rgt_metrics = pd.DataFrame(rgt_metrics)

# Display metrics by category
for category in df_rgt_metrics['Metric_Category'].unique():
    category_data = df_rgt_metrics[df_rgt_metrics['Metric_Category'] == category]
    print(f"\n{category.upper()} METRICS:")
    print("-" * 30)
    
    for idx, row in category_data.iterrows():
        print(f"📊 {row['Specific_Metric']}")
        print(f"   Formula: {row['Calculation_Formula']}")
        print(f"   Target: {row['Target_Benchmark']}")
        print(f"   Alert: {row['Alert_Thresholds']}")
        print()

# Save comprehensive framework to CSV
df_rgt_metrics.to_csv('rgt_comprehensive_framework.csv', index=False)
print("✅ Comprehensive RGT framework saved to 'rgt_comprehensive_framework.csv'")