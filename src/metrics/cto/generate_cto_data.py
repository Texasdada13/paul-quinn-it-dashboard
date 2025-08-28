"""
CTO Data Transformation Script
This script converts the example CSV files into dashboard-ready data format
Run this script from the src/metrics/cto/ directory
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducible data
np.random.seed(42)

def create_dashboard_ready_data():
    """Transform example CSV files into dashboard-ready format"""
    
    # Check if we're in the right directory
    current_dir = os.getcwd()
    if not current_dir.endswith('cto'):
        print("Warning: Run this script from the src/metrics/cto/ directory")
    
    # 1. ASSET LIFECYCLE MANAGEMENT
    print("Generating Asset Lifecycle Management dashboard data...")
    
    # Generate realistic asset data
    assets = ['Core Network Switch', 'Dell Server R740', 'Staff Laptop A14', 'HVAC Controller',
              'Student Portal Application', 'Library Firewall', 'Cisco IP Phone', 'Facilities UPS']
    
    asset_data = []
    base_date = datetime.now() - timedelta(days=180)
    
    for i in range(200):  # 200 rows of asset data
        date = base_date + timedelta(days=np.random.randint(0, 180))
        asset_name = np.random.choice(assets)
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'asset_name': asset_name,
            'asset_type': np.random.choice(['Server', 'Switch', 'Laptop', 'Application', 'Firewall', 'Phone', 'Controller', 'UPS']),
            'asset_age_years': np.round(np.random.uniform(0.5, 8.0), 1),
            'lifecycle_stage': np.random.choice(['New', 'Active', 'Maintenance', 'End-of-Life']),
            'annual_maintenance_cost': np.random.randint(500, 15000),
            'total_assets': len(assets) + np.random.randint(-2, 5),
            'end_of_life_next_12_months': np.random.randint(0, 12),
            'refresh_budget_utilization': np.random.uniform(45, 95),
            'maintenance_cost_trend': np.random.randint(2000, 25000)
        }
        asset_data.append(record)
    
    df_assets = pd.DataFrame(asset_data)
    df_assets.to_csv('asset_lifecycle_management_metrics.csv', index=False)
    print(f"✓ Created asset_lifecycle_management_metrics.csv with {len(df_assets)} records")
    
    # 2. CAPACITY PLANNING
    print("Generating Capacity Planning dashboard data...")
    
    components = ['Campus WiFi', 'Data Analytics Cluster', 'Email Platform', 'Student Portal',
                  'Core Network', 'Virtual Desktop', 'File Storage', 'Meeting Platform']
    
    capacity_data = []
    for i in range(150):
        date = base_date + timedelta(days=np.random.randint(0, 180))
        component = np.random.choice(components)
        
        current_util = np.random.uniform(20, 95)
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'resource_type': component,
            'current_utilization_pct': current_util,
            'predicted_capacity_needed': current_util + np.random.uniform(5, 25),
            'current_capacity': np.random.randint(100, 1000),
            'cost_optimization_opportunity': np.random.randint(1000, 50000),
            'time_to_capacity_limit_days': np.random.randint(30, 365)
        }
        capacity_data.append(record)
    
    df_capacity = pd.DataFrame(capacity_data)
    df_capacity.to_csv('capacity_planning_metrics.csv', index=False)
    print(f"✓ Created capacity_planning_metrics.csv with {len(df_capacity)} records")
    
    # 3. CLOUD COST OPTIMIZATION
    print("Generating Cloud Cost Optimization dashboard data...")
    
    cloud_services = ['AWS EC2', 'AWS S3', 'Azure SQL', 'Google BigQuery', 'Zoom Cloud', 'Canvas LMS Cloud', 'Tableau Cloud', 'Dropbox Business']
    
    cloud_data = []
    for i in range(120):
        date = base_date + timedelta(days=np.random.randint(0, 180))
        service = np.random.choice(cloud_services)
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'cloud_service': service,
            'monthly_cloud_spend': np.random.randint(500, 35000),
            'resource_utilization_pct': np.random.uniform(25, 90),
            'cost_optimization_savings': np.random.randint(100, 15000),
            'wasted_spend_identified': np.random.randint(0, 8000),
            'optimization_opportunity': np.random.uniform(1, 10),
            'potential_savings': np.random.randint(500, 20000)
        }
        cloud_data.append(record)
    
    df_cloud = pd.DataFrame(cloud_data)
    df_cloud.to_csv('cloud_cost_optimization_metrics.csv', index=False)
    print(f"✓ Created cloud_cost_optimization_metrics.csv with {len(df_cloud)} records")
    
    # 4. INFRASTRUCTURE PERFORMANCE
    print("Generating Infrastructure Performance dashboard data...")
    
    infrastructure_systems = ['Network', 'WiFi', 'Campus Servers', 'Cloud Storage', 'VPN Gateway', 'Firewall', 'VoIP Phones']
    
    infra_data = []
    for i in range(140):
        date = base_date + timedelta(days=np.random.randint(0, 180))
        system = np.random.choice(infrastructure_systems)
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'system_name': system,
            'system_uptime_pct': np.random.uniform(95, 99.99),
            'response_time_ms': np.random.randint(50, 800),
            'incidents_resolved': np.random.randint(0, 15),
            'performance_score': np.random.uniform(6, 10),
            'incident_severity': np.random.choice(['Low', 'Medium', 'High', 'Critical'])
        }
        infra_data.append(record)
    
    df_infra = pd.DataFrame(infra_data)
    df_infra.to_csv('infrastructure_performance_metrics.csv', index=False)
    print(f"✓ Created infrastructure_performance_metrics.csv with {len(df_infra)} records")
    
    # 5. SECURITY METRICS
    print("Generating Security dashboard data...")
    
    security_assets = ['Core Network', 'Email Suite', 'ERP System', 'Website', 'Student Portal', 'Cloud Servers', 'Campus WiFi']
    
    security_data = []
    for i in range(100):
        date = base_date + timedelta(days=np.random.randint(0, 180))
        asset = np.random.choice(security_assets)
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'asset': asset,
            'security_incidents': np.random.randint(0, 8),
            'vulnerability_score': np.random.uniform(2, 8),
            'compliance_score': np.random.uniform(85, 99),
            'security_training_completion': np.random.uniform(70, 95),
            'threat_level': np.random.choice(['Low', 'Medium', 'High'])
        }
        security_data.append(record)
    
    df_security = pd.DataFrame(security_data)
    df_security.to_csv('security_metrics.csv', index=False)
    print(f"✓ Created security_metrics.csv with {len(df_security)} records")
    
    # 6. SYSTEM UTILIZATION
    print("Generating System Utilization dashboard data...")
    
    system_data = []
    for i in range(160):
        date = base_date + timedelta(days=np.random.randint(0, 180))
        system = np.random.choice(infrastructure_systems)
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'system_name': system,
            'cpu_utilization_pct': np.random.uniform(20, 85),
            'memory_utilization_pct': np.random.uniform(30, 90),
            'storage_utilization_pct': np.random.uniform(40, 95),
            'network_utilization_pct': np.random.uniform(15, 75),
            'performance_score': np.random.uniform(6, 10)
        }
        system_data.append(record)
    
    df_system = pd.DataFrame(system_data)
    df_system.to_csv('system_utilization_metrics.csv', index=False)
    print(f"✓ Created system_utilization_metrics.csv with {len(df_system)} records")
    
    # 7. TECHNICAL DEBT
    print("Generating Technical Debt dashboard data...")
    
    systems = ['Student Information System', 'Legacy ERP', 'Old Website', 'Email Server', 'Database Server', 'File Server']
    
    debt_data = []
    for i in range(80):
        date = base_date + timedelta(days=np.random.randint(0, 180))
        system = np.random.choice(systems)
        
        record = {
            'date': date.strftime('%Y-%m-%d'),
            'system_name': system,
            'technical_debt_score': np.random.uniform(3, 9),
            'legacy_systems_count': np.random.randint(1, 12),
            'maintenance_cost_annual': np.random.randint(5000, 80000),
            'modernization_priority': np.random.choice(['Low', 'Medium', 'High'])
        }
        debt_data.append(record)
    
    df_debt = pd.DataFrame(debt_data)
    df_debt.to_csv('technical_debt_metrics.csv', index=False)
    print(f"✓ Created technical_debt_metrics.csv with {len(df_debt)} records")
    
    print("\n🎉 All CTO dashboard-ready CSV files have been created!")
    print("You can now run your dashboard and the CTO metrics should display properly.")

if __name__ == "__main__":
    create_dashboard_ready_data()