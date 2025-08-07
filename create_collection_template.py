"""
Paul Quinn College - IT Effectiveness Data Collection Template Generator
Creates Excel templates for easy data collection
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_data_collection_template():
    """Create an Excel file with multiple sheets for data collection"""
    
    # Create Excel writer
    with pd.ExcelWriter('PQC_Data_Collection_Template.xlsx', engine='xlsxwriter') as writer:
        
        # 1. IT Budget Sheet
        budget_template = pd.DataFrame({
            'Category': ['Hardware', 'Software Licenses', 'Cloud Services', 'Professional Services', 
                        'IT Staff Salaries', 'Telecommunications', 'Maintenance Contracts', 'Other'],
            'FY2023_Budget': [''] * 8,
            'FY2023_Actual': [''] * 8,
            'FY2024_Budget': [''] * 8,
            'FY2024_Actual': [''] * 8,
            'FY2025_Budget': [''] * 8,
            'Notes': [''] * 8
        })
        budget_template.to_excel(writer, sheet_name='IT_Budget', index=False)
        
        # 2. Vendor Information Sheet
        vendor_template = pd.DataFrame({
            'Vendor_Name': ['Example: Microsoft', '', '', '', ''],
            'Category': ['Software', '', '', '', ''],
            'Annual_Contract_Value': ['50000', '', '', '', ''],
            'Contract_Start_Date': ['01/01/2024', '', '', '', ''],
            'Contract_End_Date': ['12/31/2024', '', '', '', ''],
            'Payment_Terms': ['Annual', '', '', '', ''],
            'Auto_Renewal': ['Yes', '', '', '', ''],
            'Business_Owner': ['John Smith', '', '', '', ''],
            'Technical_Owner': ['Jane Doe', '', '', '', ''],
            'Critical_System': ['Yes', '', '', '', ''],
            'Number_of_Users': ['500', '', '', '', '']
        })
        vendor_template.to_excel(writer, sheet_name='Vendors', index=False)
        
        # 3. Project Portfolio Sheet
        project_template = pd.DataFrame({
            'Project_Name': ['Example: Student Portal Upgrade', '', '', '', ''],
            'Project_Type': ['Transform', '', '', '', ''],
            'Department': ['IT', '', '', '', ''],
            'Status': ['In Progress', '', '', '', ''],
            'Health': ['Green', '', '', '', ''],
            'Start_Date': ['01/15/2024', '', '', '', ''],
            'Target_End_Date': ['12/31/2024', '', '', '', ''],
            'Budget': ['75000', '', '', '', ''],
            'Spent_to_Date': ['45000', '', '', '', ''],
            'Percent_Complete': ['60', '', '', '', ''],
            'Business_Value': ['High', '', '', '', ''],
            'Risk_Level': ['Medium', '', '', '', '']
        })
        project_template.to_excel(writer, sheet_name='Projects', index=False)
        
        # 4. Systems Inventory Sheet
        systems_template = pd.DataFrame({
            'System_Name': ['Example: Banner ERP', '', '', '', ''],
            'System_Type': ['Enterprise Application', '', '', '', ''],
            'Vendor': ['Ellucian', '', '', '', ''],
            'Version': ['9.0', '', '', '', ''],
            'Hosted': ['On-Premise', '', '', '', ''],
            'Users': ['1200', '', '', '', ''],
            'Criticality': ['Mission Critical', '', '', '', ''],
            'Last_Major_Upgrade': ['01/01/2022', '', '', '', ''],
            'Annual_Maintenance_Cost': ['120000', '', '', '', ''],
            'Availability_Target': ['99.9%', '', '', '', ''],
            'Actual_Availability': ['99.5%', '', '', '', '']
        })
        systems_template.to_excel(writer, sheet_name='Systems', index=False)
        
        # 5. Instructions Sheet
        instructions = pd.DataFrame({
            'Instructions': [
                'IT EFFECTIVENESS DATA COLLECTION TEMPLATE',
                '',
                'This template is designed to collect the essential data needed for IT effectiveness analysis.',
                '',
                'INSTRUCTIONS:',
                '1. Fill out each tab with your current data',
                '2. Use the example row as a guide for format',
                '3. Leave cells blank if data is not available',
                '4. Add additional rows as needed',
                '',
                'TAB DESCRIPTIONS:',
                '- IT_Budget: Annual IT budget by category for trending',
                '- Vendors: All IT vendors with contract details',
                '- Projects: Active and planned IT projects',
                '- Systems: Inventory of major IT systems',
                '',
                'REQUIRED FIELDS:',
                '- Vendor_Name, Annual_Contract_Value',
                '- Project_Name, Budget, Status',
                '- System_Name, Users, Criticality',
                '',
                'For questions, contact: [your email]'
            ]
        })
        instructions.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Format the workbook
        workbook = writer.book
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#003366',
            'font_color': 'white',
            'border': 1
        })
        
        # Apply formatting to headers
        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.set_row(0, 20, header_format)
            worksheet.set_column('A:K', 20)
    
    print("✅ Data Collection Template Created: PQC_Data_Collection_Template.xlsx")
    print("\nPlease send this to Paul Quinn College for completion.")

# Create the template
create_data_collection_template()
