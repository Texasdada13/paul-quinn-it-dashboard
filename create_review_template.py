import pandas as pd
from datetime import datetime
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows

def create_dashboard_review_spreadsheet():
    """Create a comprehensive dashboard review spreadsheet"""
    
    # Define the structure for each persona
    dashboard_structure = {
        'CFO': {
            'title': 'CFO - Financial Steward',
            'tabs': {
                'Budget Analysis': ['Budget vs Actual', 'Variance Analysis', 'Budget Alerts'],
                'Contracts & Vendors': ['Contract Expiration Alerts', 'Vendor Spend Analysis', 'Contract Timeline'],
                'Grant Compliance': ['Compliance Dashboard', 'Risk Assessment', 'Grant Utilization'],
                'ROI & Benchmarking': ['Student Success ROI', 'HBCU Peer Benchmarking', 'IT Spend Breakdown'],
                'All Metrics': ['Summary View', 'Metric Availability', 'Data Quality']
            }
        },
        'CIO': {
            'title': 'CIO - Strategic Business Partner',
            'tabs': {
                'Strategic Portfolio': ['Digital Transformation', 'Strategic Alignment', 'Portfolio Balance'],
                'Business Analysis': ['Business Unit IT Spend', 'App Cost Analysis', 'Resource Allocation'],
                'Risk & Vendor': ['Risk Metrics', 'Vendor Management', 'Compliance Status'],
                'All Metrics': ['Summary View', 'Metric Availability', 'Data Quality']
            }
        },
        'CTO': {
            'title': 'CTO - Technology Operator',
            'tabs': {
                'Infrastructure': ['Performance Metrics', 'System Utilization', 'Capacity Planning'],
                'Cloud & Assets': ['Cloud Cost Optimization', 'Asset Lifecycle', 'License Management'],
                'Security & Tech Debt': ['Security Metrics', 'Technical Debt Analysis', 'Incident Response'],
                'All Metrics': ['Summary View', 'Metric Availability', 'Data Quality']
            }
        }
    }
    
    # Create the review template structure
    review_columns = [
        'Tab Name',
        'Visualization/Component',
        'Current State',
        'Issues Identified',
        'Severity',
        'Proposed Changes',
        'Priority',
        'Effort Estimate',
        'Impact',
        'Dependencies',
        'Notes',
        'Review Date',
        'Reviewer'
    ]
    
    # Create Excel writer
    with pd.ExcelWriter('Dashboard_Review_Template.xlsx', engine='openpyxl') as writer:
        
        # Create overview sheet
        overview_data = []
        for persona, details in dashboard_structure.items():
            for tab, components in details['tabs'].items():
                overview_data.append({
                    'Persona': persona,
                    'Tab': tab,
                    'Components': len(components),
                    'Status': 'Not Reviewed',
                    'Last Review': '',
                    'Issues Count': 0,
                    'Priority Issues': 0
                })
        
        overview_df = pd.DataFrame(overview_data)
        overview_df.to_excel(writer, sheet_name='Overview', index=False)
        
        # Create detailed review sheets for each persona
        for persona, details in dashboard_structure.items():
            sheet_data = []
            
            for tab, components in details['tabs'].items():
                for component in components:
                    sheet_data.append({
                        'Tab Name': tab,
                        'Visualization/Component': component,
                        'Current State': '',
                        'Issues Identified': '',
                        'Severity': '',  # Critical, High, Medium, Low
                        'Proposed Changes': '',
                        'Priority': '',  # P0, P1, P2, P3
                        'Effort Estimate': '',  # Hours or Days
                        'Impact': '',  # High, Medium, Low
                        'Dependencies': '',
                        'Notes': '',
                        'Review Date': datetime.now().strftime('%Y-%m-%d'),
                        'Reviewer': ''
                    })
            
            df = pd.DataFrame(sheet_data)
            sheet_name = f"{persona}_Review"
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Format the sheet
            worksheet = writer.sheets[sheet_name]
            
            # Set column widths
            column_widths = {
                'A': 20,  # Tab Name
                'B': 30,  # Visualization/Component
                'C': 40,  # Current State
                'D': 50,  # Issues Identified
                'E': 15,  # Severity
                'F': 50,  # Proposed Changes
                'G': 10,  # Priority
                'H': 15,  # Effort Estimate
                'I': 10,  # Impact
                'J': 30,  # Dependencies
                'K': 40,  # Notes
                'L': 15,  # Review Date
                'M': 20   # Reviewer
            }
            
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width
            
            # Add header formatting
            header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
            header_font = Font(color="FFFFFF", bold=True)
            
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")
        
        # Create Issues Summary sheet
        issues_template = pd.DataFrame({
            'Issue ID': ['ISS-001', 'ISS-002', 'ISS-003'],
            'Persona': ['', '', ''],
            'Tab': ['', '', ''],
            'Component': ['', '', ''],
            'Issue Description': ['', '', ''],
            'Severity': ['', '', ''],
            'Priority': ['', '', ''],
            'Status': ['Open', 'Open', 'Open'],
            'Assigned To': ['', '', ''],
            'Due Date': ['', '', ''],
            'Resolution': ['', '', '']
        })
        issues_template.to_excel(writer, sheet_name='Issues_Summary', index=False)
        
        # Create Action Items sheet
        actions_template = pd.DataFrame({
            'Action ID': ['ACT-001', 'ACT-002', 'ACT-003'],
            'Related Issue': ['', '', ''],
            'Action Description': ['', '', ''],
            'Owner': ['', '', ''],
            'Due Date': ['', '', ''],
            'Status': ['Not Started', 'Not Started', 'Not Started'],
            'Progress Notes': ['', '', ''],
            'Blockers': ['', '', '']
        })
        actions_template.to_excel(writer, sheet_name='Action_Items', index=False)
    
    print("Dashboard Review Template created: Dashboard_Review_Template.xlsx")
    
    # Create a companion markdown file for review guidelines
    guidelines = """# Dashboard Review Guidelines

## Review Process

### 1. Systematic Review Approach
- Review each persona's dashboard separately
- Go through each tab in order
- Document all observations, even minor ones
- Take screenshots of issues for reference

### 2. For Each Component, Document:

#### Current State
- What exists now?
- Is it functioning correctly?
- What data is being displayed?
- How is it visualized?

#### Issues Identified
- Data quality issues
- Visualization problems
- Performance issues
- User experience problems
- Missing functionality

#### Severity Levels
- **Critical**: Broken functionality, wrong data, security issues
- **High**: Major UX issues, significant data delays, important missing features
- **Medium**: Minor UX issues, nice-to-have features, optimization opportunities
- **Low**: Cosmetic issues, minor enhancements

#### Priority Levels
- **P0**: Must fix immediately (blocking users)
- **P1**: Fix in current sprint
- **P2**: Fix in next sprint
- **P3**: Backlog/nice to have

### 3. Proposed Changes
Be specific about:
- What needs to change
- How it should work instead
- Any mockups or examples
- Technical requirements

### 4. Effort Estimation
- **Small**: < 4 hours
- **Medium**: 4-16 hours (0.5-2 days)
- **Large**: 16-40 hours (2-5 days)
- **XL**: > 40 hours (needs breakdown)

### 5. Impact Assessment
- **High**: Affects core functionality or many users
- **Medium**: Improves experience for specific use cases
- **Low**: Nice to have, minimal user impact

## Review Checklist

### Data Quality
- [ ] Data is current and updated at expected frequency
- [ ] No missing or null values where unexpected
- [ ] Calculations are accurate
- [ ] Data formats are consistent

### Visualization
- [ ] Charts are appropriate for the data type
- [ ] Colors are meaningful and accessible
- [ ] Labels and titles are clear
- [ ] Legends are present where needed
- [ ] Scales make sense

### User Experience
- [ ] Loading time is acceptable
- [ ] Interactions are intuitive
- [ ] Error states are handled gracefully
- [ ] Mobile responsiveness (if required)

### Technical
- [ ] No console errors
- [ ] Performance is acceptable
- [ ] Security best practices followed
- [ ] Code is maintainable

## Example Issues

### Example 1: Data Issue
- **Component**: Budget vs Actual Chart
- **Issue**: Actual spend showing as negative values
- **Severity**: Critical
- **Proposed Change**: Fix data transformation logic to ensure positive values
- **Priority**: P0

### Example 2: UX Issue
- **Component**: Contract Expiration Timeline
- **Issue**: Timeline is difficult to read with overlapping labels
- **Severity**: Medium
- **Proposed Change**: Implement zoom/pan functionality or alternate view for dense data
- **Priority**: P2

### Example 3: Enhancement
- **Component**: Grant Compliance Dashboard
- **Issue**: No export functionality for compliance reports
- **Severity**: Low
- **Proposed Change**: Add PDF/Excel export button
- **Priority**: P3
"""
    
    with open('Dashboard_Review_Guidelines.md', 'w') as f:
        f.write(guidelines)
    
    print("Review Guidelines created: Dashboard_Review_Guidelines.md")

# Run the function to create the files
if __name__ == "__main__":
    create_dashboard_review_spreadsheet()