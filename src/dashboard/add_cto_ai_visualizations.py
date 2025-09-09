#!/usr/bin/env python3
"""
Add AI visualization calls to CTO section to get the advanced charts
"""

from pathlib import Path
import re

def add_cto_ai_visualizations():
    """Add the AI optimization visualizations to CTO section"""
    
    dashboard_file = Path("fully_integrated_dashboard_with_AI.py")
    
    if not dashboard_file.exists():
        print("❌ Dashboard file not found")
        return False
    
    content = dashboard_file.read_text(encoding='utf-8')
    
    # Find the CTO AI tab section and replace it with full functionality
    cto_ai_replacement = '''                elif tab_name == "🤖 AI Operational Optimization":
                    if AI_FEATURES_AVAILABLE:
                        st.markdown("### AI-Powered Operational Optimization")
                        
                        # Initialize AI optimization dashboard
                        optimization_dashboard = OptimizationDashboard()
                        
                        # Create comprehensive CTO dataset for AI analysis
                        cto_dataset = {
                            'infrastructure_data': pd.DataFrame({
                                'Component': ['Student Information System', 'LMS Platform', 'WiFi Infrastructure', 
                                            'Email Services', 'Cloud Storage'],
                                'Uptime (%)': [99.2, 98.8, 99.5, 99.9, 99.7],
                                'Performance Score': [85, 92, 78, 95, 88],
                                'Maintenance Cost': [25000, 15000, 12000, 8000, 10000],
                                'Age (Years)': [3, 2, 5, 1, 2]
                            }),
                            'cloud_data': pd.DataFrame({
                                'Service': ['AWS EC2', 'Azure Storage', 'Office 365', 'Google Workspace', 'Backup Services'],
                                'Monthly Cost': [4500, 2200, 3800, 1200, 1500],
                                'Utilization (%)': [78, 65, 92, 85, 70],
                                'Optimization Potential': [22, 35, 8, 15, 30]
                            }),
                            'security_data': pd.DataFrame({
                                'Security Layer': ['Firewall', 'Antivirus', 'Email Security', 'Identity Management', 'Data Encryption'],
                                'Effectiveness (%)': [95, 88, 92, 85, 98],
                                'Risk Level': ['Low', 'Medium', 'Low', 'Medium', 'Low'],
                                'Last Updated': ['2024-01-15', '2024-01-10', '2024-01-20', '2024-01-05', '2024-01-18']
                            })
                        }
                        
                        # Render AI optimization dashboard for CTO
                        optimization_dashboard.render_optimization_dashboard('cto', cto_dataset)
                        
                        # Add AI-specific visualizations
                        st.markdown("---")
                        st.markdown("#### AI-Generated Implementation Roadmap")
                        
                        # Create the AI-Optimized Implementation Roadmap
                        roadmap_data = pd.DataFrame({
                            'Task': ['Automated Infrastructure Monitoring', 'Expand AI-Powered Student Analytics', 
                                   'AI-Powered IT Service Desk', 'Enhanced Cybersecurity Framework', 
                                   'Cloud Infrastructure Right-Sizing'],
                            'Start_Date': ['2025-09-01', '2025-10-15', '2025-12-01', '2026-01-15', '2026-03-01'],
                            'End_Date': ['2025-12-01', '2026-06-01', '2026-04-01', '2026-08-01', '2026-05-01'],
                            'Score': [85, 92, 78, 88, 75],
                            'Priority': ['High', 'Critical', 'High', 'Critical', 'Medium']
                        })
                        
                        # Convert dates
                        roadmap_data['Start_Date'] = pd.to_datetime(roadmap_data['Start_Date'])
                        roadmap_data['End_Date'] = pd.to_datetime(roadmap_data['End_Date'])
                        roadmap_data['Duration'] = (roadmap_data['End_Date'] - roadmap_data['Start_Date']).dt.days
                        
                        # Create Gantt-style timeline
                        fig = px.timeline(roadmap_data, 
                                        x_start='Start_Date', x_end='End_Date', y='Task',
                                        color='Score', 
                                        color_continuous_scale='Viridis',
                                        title='AI-Optimized Implementation Roadmap',
                                        height=400)
                        fig.update_layout(xaxis_title="Timeline", yaxis_title="Implementation Tasks")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Infrastructure optimization insights
                        st.markdown("#### Infrastructure Optimization Analysis")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Asset lifecycle analysis
                            asset_data = pd.DataFrame({
                                'Asset_Category': ['Student Information Systems', 'LMS Platforms', 'Email Systems', 
                                                 'Database Servers', 'File Servers', 'Legacy ERP'],
                                'Health_Score': [85, 92, 95, 78, 82, 45],
                                'Age_Years': [3, 2, 1, 4, 3, 8],
                                'Replacement_Priority': [3, 1, 1, 4, 3, 5]
                            })
                            
                            fig = px.scatter(asset_data, x='Age_Years', y='Health_Score', 
                                           size='Replacement_Priority', color='Asset_Category',
                                           title='Asset Health vs Age Analysis',
                                           labels={'Age_Years': 'Age (Years)', 'Health_Score': 'Health Score'})
                            fig.update_layout(height=350)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Technical debt visualization
                            debt_data = pd.DataFrame({
                                'System': ['Student Information System', 'LMS Platform', 'Email System', 
                                         'Database Server', 'File Server', 'Legacy ERP'],
                                'Debt_Score': [3, 2, 1, 4, 3, 8],
                                'Maintenance_Hours': [120, 80, 40, 200, 100, 400]
                            })
                            
                            fig = px.bar(debt_data, x='System', y='Debt_Score',
                                       color='Maintenance_Hours',
                                       color_continuous_scale='Reds',
                                       title='Technical Debt by System',
                                       labels={'Debt_Score': 'Technical Debt Score'})
                            fig.update_xaxes(tickangle=45)
                            fig.update_layout(height=350)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Capacity planning metrics
                        st.markdown("#### Capacity Planning & Utilization")
                        
                        # Create capacity utilization chart
                        capacity_data = pd.DataFrame({
                            'Resource': ['CPU Usage', 'Memory Usage', 'Storage Usage', 'Network Bandwidth', 
                                       'Database Connections', 'Active Users'],
                            'Current_Usage': [68, 72, 85, 45, 60, 1200],
                            'Capacity': [100, 100, 100, 100, 100, 2000],
                            'Projected_Growth': [5, 8, 12, 15, 10, 200]
                        })
                        
                        capacity_data['Usage_Percentage'] = (capacity_data['Current_Usage'] / capacity_data['Capacity'] * 100)
                        capacity_data['Projected_Percentage'] = ((capacity_data['Current_Usage'] + capacity_data['Projected_Growth']) / capacity_data['Capacity'] * 100)
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Bar(
                            name='Current Usage',
                            x=capacity_data['Resource'],
                            y=capacity_data['Usage_Percentage'],
                            marker_color='lightblue'
                        ))
                        
                        fig.add_trace(go.Bar(
                            name='Projected Usage',
                            x=capacity_data['Resource'],
                            y=capacity_data['Projected_Percentage'],
                            marker_color='orange'
                        ))
                        
                        fig.add_hline(y=80, line_dash="dash", line_color="red", 
                                    annotation_text="Capacity Warning Threshold")
                        
                        fig.update_layout(
                            title='Resource Utilization: Current vs Projected',
                            xaxis_title='Resource Type',
                            yaxis_title='Utilization Percentage',
                            barmode='group',
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # System performance trends
                        st.markdown("#### System Performance Trends")
                        
                        # Generate performance trend data
                        dates = pd.date_range('2024-01-01', periods=30, freq='D')
                        performance_trends = pd.DataFrame({
                            'Date': dates,
                            'Student_Portal': np.random.normal(95, 3, 30),
                            'LMS_Platform': np.random.normal(92, 4, 30),
                            'Email_System': np.random.normal(98, 2, 30),
                            'Database': np.random.normal(88, 5, 30),
                            'Network': np.random.normal(94, 3, 30)
                        })
                        
                        fig = px.line(performance_trends, x='Date', 
                                    y=['Student_Portal', 'LMS_Platform', 'Email_System', 'Database', 'Network'],
                                    title='30-Day Performance Trend Analysis',
                                    labels={'value': 'Performance Score', 'variable': 'System'})
                        fig.update_layout(height=350)
                        st.plotly_chart(fig, use_container_width=True)
                        
                    else:
                        st.warning("AI operational optimization features not available")
                        st.info("Install AI modules to access advanced operational analytics")'''
    
    # Find and replace the CTO AI tab section
    pattern = r'elif tab_name == "🤖 AI Operational Optimization":.*?else:'
    
    if re.search(pattern, content, re.DOTALL):
        # Replace the existing CTO AI section
        content = re.sub(pattern, cto_ai_replacement + '\n                else:', content, flags=re.DOTALL)
        print("✅ Updated existing CTO AI section")
    else:
        print("❌ Could not find CTO AI section to update")
        return False
    
    # Save the updated file
    dashboard_file.write_text(content, encoding='utf-8')
    print(f"✅ Enhanced CTO AI visualizations added to {dashboard_file}")
    return True

def main():
    """Main execution"""
    print("🚀 Adding CTO AI Visualizations")
    print("=" * 40)
    
    if add_cto_ai_visualizations():
        print("\n✅ CTO AI visualizations successfully added!")
        print("\n🔄 Next steps:")
        print("1. Restart your dashboard:")
        print("   streamlit run fully_integrated_dashboard_with_AI.py --server.port 8505")
        print("2. Go to CTO persona > AI Operational Optimization tab")
        print("3. You should now see:")
        print("   - AI-Optimized Implementation Roadmap")
        print("   - Asset Health vs Age Analysis")
        print("   - Technical Debt Visualization")
        print("   - Capacity Planning & Utilization")
        print("   - System Performance Trends")
    else:
        print("\n❌ Failed to add CTO AI visualizations")
        print("Check that the dashboard file exists and has the expected structure")

if __name__ == "__main__":
    main()