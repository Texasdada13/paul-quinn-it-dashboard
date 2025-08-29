"""
Paul Quinn College IT Analytics Suite - Enhanced Field Enumeration Script V2
This version organizes output by sheets and tabs for better organization
"""

import os
import pandas as pd
import json
import re
from pathlib import Path
from typing import Dict, List, Set
import ast
import inspect

class DashboardFieldEnumeratorV2:
    def __init__(self, project_root: str = None):
        """Initialize the field enumerator with project structure"""
        if project_root is None:
            # Try to find project root automatically
            current_dir = Path(__file__).parent
            # Look for src directory
            if (current_dir / 'src').exists():
                self.project_root = current_dir
            elif (current_dir.parent / 'src').exists():
                self.project_root = current_dir.parent
            else:
                self.project_root = current_dir
        else:
            self.project_root = Path(project_root)
        
        self.dashboard_dir = self.project_root / 'src' / 'dashboard'
        self.metrics_dir = self.project_root / 'src' / 'metrics'
        
        # Enhanced storage organized by persona/section
        self.all_fields = {
            'csv_columns': {},
            'display_functions': {},
            'metric_names': {},
            'chart_fields': {},
            'ui_labels': {}
        }
        
        # Organization mappings
        self.persona_mapping = {
            'cfo': 'CFO - Financial Steward',
            'cio': 'CIO - Strategic Business Partner', 
            'cto': 'CTO - Technology Operator',
            'pm': 'Project Manager'
        }
        
        # Tab/section mapping based on your dashboard structure
        self.section_mapping = {
            'budget': 'Budget Analysis',
            'contract': 'Contracts & Vendors',
            'grant': 'Grant Compliance',
            'roi': 'ROI & Benchmarking',
            'digital': 'Digital Transformation',
            'strategic': 'Strategic Alignment',
            'risk': 'Risk Management',
            'infrastructure': 'Infrastructure Performance',
            'cloud': 'Cloud Cost Optimization',
            'security': 'Security & Compliance'
        }
    
    def scan_all_fields(self) -> Dict:
        """Main method to scan all fields across the dashboard"""
        print("🔍 Starting comprehensive field enumeration V2...")
        print(f"📁 Project root: {self.project_root}")
        print(f"📊 Dashboard dir: {self.dashboard_dir}")
        print(f"📈 Metrics dir: {self.metrics_dir}")
        
        # Scan different types of fields
        self.scan_csv_files()
        self.scan_python_files()
        self.scan_display_functions()
        self.scan_ui_elements()
        self.scan_chart_configurations()
        
        # Generate summary
        summary = self.generate_field_summary()
        
        # Export results with enhanced organization
        self.export_enhanced_field_mappings()
        
        return summary
    
    def scan_csv_files(self):
        """Scan all CSV files for column names and data values"""
        print("\n📊 Scanning CSV files for column names and sample values...")
        
        csv_files = []
        if self.metrics_dir.exists():
            csv_files = list(self.metrics_dir.rglob('*.csv'))
        
        for csv_file in csv_files:
            try:
                # Read the full CSV to get columns AND sample values
                df = pd.read_csv(csv_file)
                
                relative_path = csv_file.relative_to(self.project_root)
                
                # Determine persona and section from file path
                persona, section = self.categorize_file_path(str(relative_path))
                
                file_info = {
                    'columns': list(df.columns),
                    'sample_values': {},
                    'unique_values': {},
                    'row_count': len(df),
                    'persona': persona,
                    'section': section,
                    'file_path': str(relative_path),
                    'visualization_fields': self.extract_visualization_fields(str(csv_file), df)
                }
                
                # For each column, capture sample and unique values
                for col in df.columns:
                    # Get first few non-null values as samples
                    sample_vals = df[col].dropna().head(5).tolist()
                    file_info['sample_values'][col] = sample_vals
                    
                    # For categorical-looking columns, get unique values (dropdown options)
                    if df[col].dtype == 'object' or df[col].nunique() <= 20:
                        unique_vals = df[col].dropna().unique().tolist()
                        file_info['unique_values'][col] = unique_vals[:50]  # Limit to 50
                
                self.all_fields['csv_columns'][str(relative_path)] = file_info
                print(f"✅ {csv_file.name} ({persona} - {section}): {len(df.columns)} columns, {len(df)} rows")
                
            except Exception as e:
                print(f"❌ Error reading {csv_file.name}: {e}")
    
    def categorize_file_path(self, file_path: str) -> tuple:
        """Determine persona and section from file path"""
        file_path_lower = file_path.lower()
        
        # Determine persona
        persona = "General"
        if 'cfo' in file_path_lower:
            persona = "CFO - Financial Steward"
        elif 'cio' in file_path_lower:
            persona = "CIO - Strategic Business Partner"
        elif 'cto' in file_path_lower:
            persona = "CTO - Technology Operator"
        elif 'pm' in file_path_lower:
            persona = "Project Manager"
        
        # Determine section
        section = "General"
        for key, display_name in self.section_mapping.items():
            if key in file_path_lower:
                section = display_name
                break
        
        # Additional section detection from filename
        filename = Path(file_path).stem.lower()
        if 'budget' in filename:
            section = "Budget Analysis"
        elif 'contract' in filename:
            section = "Contracts & Vendors"
        elif 'grant' in filename:
            section = "Grant Compliance"
        elif 'roi' in filename or 'benchmark' in filename:
            section = "ROI & Benchmarking"
        elif 'digital' in filename or 'transformation' in filename:
            section = "Digital Transformation"
        elif 'strategic' in filename or 'alignment' in filename:
            section = "Strategic Alignment"
        elif 'risk' in filename:
            section = "Risk Management"
        elif 'infrastructure' in filename or 'performance' in filename:
            section = "Infrastructure Performance"
        elif 'cloud' in filename:
            section = "Cloud Cost Optimization"
        elif 'security' in filename:
            section = "Security & Compliance"
        
        return persona, section
    
    def scan_python_files(self):
        """Scan Python files for field references, variable names, and visualization parameters"""
        print("\n🐍 Scanning Python files for field references...")
        
        python_files = []
        if self.dashboard_dir.exists():
            python_files.extend(list(self.dashboard_dir.glob('*.py')))
        if self.metrics_dir.exists():
            python_files.extend(list(self.metrics_dir.rglob('*.py')))
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = py_file.relative_to(self.project_root)
                persona, section = self.categorize_file_path(str(relative_path))
                
                file_info = {
                    'dataframe_columns': self.extract_dataframe_columns(content),
                    'plotly_fields': self.extract_plotly_fields(content),
                    'streamlit_elements': self.extract_streamlit_elements(content),
                    'variable_names': self.extract_variable_names(content),
                    'string_literals': self.extract_display_strings(content),
                    'persona': persona,
                    'section': section,
                    'file_path': str(relative_path)
                }
                
                self.all_fields['display_functions'][str(relative_path)] = file_info
                print(f"✅ {py_file.name} ({persona} - {section}): Extracted field references")
                
            except Exception as e:
                print(f"❌ Error reading {py_file.name}: {e}")
    
    def extract_plotly_fields(self, content: str) -> Dict:
        """Extract field names used in Plotly visualizations"""
        plotly_fields = {
            'x_axis': [],
            'y_axis': [],
            'color_fields': [],
            'hover_fields': [],
            'filter_fields': [],
            'dropdown_options': []
        }
        
        # Patterns to find Plotly chart parameters
        patterns = {
            'x_axis': [r'x=[\'"](.*?)[\'"]', r'x=([a-zA-Z_]\w*)', r'x=df\[[\'"](.*?)[\'"]\]'],
            'y_axis': [r'y=[\'"](.*?)[\'"]', r'y=([a-zA-Z_]\w*)', r'y=df\[[\'"](.*?)[\'"]\]'],
            'color_fields': [r'color=[\'"](.*?)[\'"]', r'color=([a-zA-Z_]\w*)', r'color=df\[[\'"](.*?)[\'"]\]'],
            'hover_fields': [r'hover_name=[\'"](.*?)[\'"]', r'hover_data=\[(.*?)\]'],
            'dropdown_options': [r'options=\[(.*?)\]', r'selectbox\(.*?,\s*\[(.*?)\]']
        }
        
        for field_type, regex_list in patterns.items():
            for pattern in regex_list:
                matches = re.findall(pattern, content, re.IGNORECASE)
                plotly_fields[field_type].extend(matches)
        
        # Clean up the results
        for field_type in plotly_fields:
            plotly_fields[field_type] = list(set(plotly_fields[field_type]))
        
        return plotly_fields
    
    def extract_dataframe_columns(self, content: str) -> List[str]:
        """Extract column names referenced in dataframe operations"""
        column_patterns = [
            r'df\[[\'"](.*?)[\'"]\]',  # df['column_name']
            r'\.([a-zA-Z_]\w*)',       # df.column_name
            r'columns=\[(.*?)\]',      # columns=['col1', 'col2']
            r'groupby\([\'"](.*?)[\'"]', # groupby('column')
            r'sort_values\([\'"](.*?)[\'"]', # sort_values('column')
        ]
        
        columns = []
        for pattern in column_patterns:
            matches = re.findall(pattern, content)
            columns.extend(matches)
        
        return list(set(columns))
    
    def extract_streamlit_elements(self, content: str) -> Dict:
        """Extract Streamlit UI element labels and options"""
        ui_elements = {
            'metric_labels': [],
            'selectbox_options': [],
            'button_labels': [],
            'tab_names': [],
            'column_headers': [],
            'markdown_titles': []
        }
        
        patterns = {
            'metric_labels': [r'st\.metric\([\'"](.*?)[\'"]'],
            'selectbox_options': [r'st\.selectbox\([^,]*,\s*\[(.*?)\]'],
            'button_labels': [r'st\.button\([\'"](.*?)[\'"]'],
            'tab_names': [r'st\.tabs\(\[(.*?)\]'],
            'markdown_titles': [r'st\.markdown\([\'"]#+\s*(.*?)[\'"]']
        }
        
        for element_type, regex_list in patterns.items():
            for pattern in regex_list:
                matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
                if element_type == 'selectbox_options' or element_type == 'tab_names':
                    # Parse list-like strings
                    for match in matches:
                        options = re.findall(r'[\'"](.*?)[\'"]', match)
                        ui_elements[element_type].extend(options)
                else:
                    ui_elements[element_type].extend(matches)
        
        return ui_elements
    
    def extract_variable_names(self, content: str) -> List[str]:
        """Extract variable names that might be field references"""
        # Find variable assignments that look like field names
        variable_patterns = [
            r'(\w+_(?:amount|total|budget|spend|cost|revenue|profit|rate|percent|score|count|value))\s*=',
            r'(\w+_(?:name|title|label|category|type|status|date|time))\s*=',
            r'(\w+_(?:metric|kpi|measurement|indicator))\s*='
        ]
        
        variables = []
        for pattern in variable_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            variables.extend(matches)
        
        return list(set(variables))
    
    def extract_display_strings(self, content: str) -> List[str]:
        """Extract string literals used for display purposes"""
        # Find strings that look like field labels or titles
        display_patterns = [
            r'[\'"]((?:[A-Z][a-z]*\s*)+)[\'"]',  # Title Case strings
            r'[\'"](\w+\s+(?:Budget|Spend|Cost|Revenue|Analysis|Report|Dashboard))[\'"]',
            r'[\'"](\w+\s+vs\s+\w+)[\'"]',  # "X vs Y" patterns
        ]
        
        strings = []
        for pattern in display_patterns:
            matches = re.findall(pattern, content)
            # Filter out very short or very long strings
            filtered = [m for m in matches if 3 <= len(m) <= 50]
            strings.extend(filtered)
        
        return list(set(strings))
    
    def scan_display_functions(self):
        """Scan display functions to understand how fields are used in visualizations"""
        print("\n🎨 Scanning display functions for visualization field usage...")
        
        # Try to import and inspect display functions
        try:
            import sys
            sys.path.append(str(self.project_root))
            from dashboard_metric_loader import DashboardMetricLoader
            
            loader = DashboardMetricLoader()
            
            # Get all methods from the loader
            methods = [method for method in dir(loader) if method.startswith('display_')]
            
            function_fields = {}
            for method_name in methods:
                try:
                    method = getattr(loader, method_name)
                    # Get source code if possible
                    source = inspect.getsource(method)
                    
                    # Categorize the method
                    persona, section = self.categorize_method_name(method_name)
                    
                    # Extract field usage from the source
                    fields = self.extract_fields_from_function_source(source)
                    fields['persona'] = persona
                    fields['section'] = section
                    function_fields[method_name] = fields
                    
                except Exception as e:
                    print(f"⚠️ Could not analyze {method_name}: {e}")
            
            self.all_fields['display_functions']['loader_methods'] = function_fields
            
        except Exception as e:
            print(f"⚠️ Could not import dashboard_metric_loader: {e}")
    
    def categorize_method_name(self, method_name: str) -> tuple:
        """Categorize display methods by persona and section"""
        method_lower = method_name.lower()
        
        # Determine persona
        persona = "General"
        if 'cfo' in method_lower:
            persona = "CFO - Financial Steward"
        elif 'cio' in method_lower:
            persona = "CIO - Strategic Business Partner"
        elif 'cto' in method_lower:
            persona = "CTO - Technology Operator"
        elif 'pm' in method_lower:
            persona = "Project Manager"
        
        # Determine section
        section = "General"
        for key, display_name in self.section_mapping.items():
            if key in method_lower:
                section = display_name
                break
        
        return persona, section
    
    def extract_fields_from_function_source(self, source: str) -> Dict:
        """Extract field names from function source code"""
        fields = {
            'dataframe_columns': [],
            'chart_axes': [],
            'filter_options': [],
            'labels': []
        }
        
        # Look for specific patterns in function source
        patterns = {
            'dataframe_columns': [
                r'df\[[\'"](.*?)[\'"]\]',
                r'data\[[\'"](.*?)[\'"]\]',
                r'\.([a-zA-Z_]\w*(?:_(?:amount|total|budget|count|rate|date|name)))',
            ],
            'chart_axes': [
                r'x=[\'"]?(.*?)[\'"]?[,\)]',
                r'y=[\'"]?(.*?)[\'"]?[,\)]',
                r'color=[\'"]?(.*?)[\'"]?[,\)]'
            ],
            'filter_options': [
                r'unique\(\)\s*\.tolist\(\)',
                r'\.value_counts\(\)',
                r'selectbox.*?\[(.*?)\]'
            ],
            'labels': [
                r'title=[\'"]?(.*?)[\'"]?[,\)]',
                r'label=[\'"]?(.*?)[\'"]?[,\)]'
            ]
        }
        
        for field_type, regex_list in patterns.items():
            for pattern in regex_list:
                matches = re.findall(pattern, source, re.IGNORECASE)
                fields[field_type].extend(matches)
        
        return fields
    
    def extract_visualization_fields(self, csv_file_path: str, df: pd.DataFrame) -> Dict:
        """Extract fields that would be used in dropdowns, filters, and chart axes"""
        viz_fields = {
            'dropdown_candidates': [],  # Categorical columns good for dropdowns
            'numeric_fields': [],       # Numeric columns for charts
            'date_fields': [],         # Date columns for time series
            'categorical_fields': [],   # Categories for grouping/coloring
            'filter_fields': []        # Fields commonly used in filters
        }
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Identify date fields
            if any(date_word in col_lower for date_word in ['date', 'time', 'year', 'month', 'day']):
                viz_fields['date_fields'].append(col)
            
            # Identify numeric fields (good for chart axes)
            elif df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                viz_fields['numeric_fields'].append(col)
                
                # Fields that commonly appear in dropdowns for amount/value selection
                if any(word in col_lower for word in ['amount', 'total', 'budget', 'cost', 'spend', 'revenue']):
                    viz_fields['dropdown_candidates'].append(col)
            
            # Identify categorical fields (good for dropdowns, filters, color coding)
            elif df[col].dtype == 'object':
                unique_count = df[col].nunique()
                
                # Good candidates for dropdowns (few unique values)
                if unique_count <= 20:
                    viz_fields['dropdown_candidates'].append(col)
                    viz_fields['categorical_fields'].append(col)
                
                # Common filter field patterns
                if any(filter_word in col_lower for filter_word in 
                      ['category', 'type', 'status', 'department', 'vendor', 'project']):
                    viz_fields['filter_fields'].append(col)
        
        return viz_fields
    
    def scan_ui_elements(self):
        """Scan for UI element labels and dropdown options"""
        print("\n🖥️ Scanning UI elements...")
        
        # This method looks for hardcoded UI text
        if self.dashboard_dir.exists():
            for py_file in self.dashboard_dir.glob('*.py'):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    relative_path = py_file.relative_to(self.project_root)
                    persona, section = self.categorize_file_path(str(relative_path))
                    
                    # Extract UI text patterns
                    ui_patterns = {
                        'tab_labels': r'st\.tabs\(\[(.*?)\]',
                        'selectbox_labels': r'st\.selectbox\([\'"]([^"\']*)[\'"]',
                        'metric_titles': r'st\.metric\([\'"]([^"\']*)[\'"]',
                        'header_text': r'st\.(?:header|subheader|title)\([\'"]([^"\']*)[\'"]',
                        'markdown_headers': r'#+\s*([^\n]+)'
                    }
                    
                    file_ui = {
                        'persona': persona,
                        'section': section,
                        'file_path': str(relative_path)
                    }
                    for ui_type, pattern in ui_patterns.items():
                        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
                        if ui_type in ['tab_labels']:
                            # Parse tab arrays
                            tab_matches = []
                            for match in matches:
                                tabs = re.findall(r'[\'"]([^"\']+)[\'"]', match)
                                tab_matches.extend(tabs)
                            file_ui[ui_type] = tab_matches
                        else:
                            file_ui[ui_type] = matches
                    
                    self.all_fields['ui_labels'][py_file.name] = file_ui
                    
                except Exception as e:
                    print(f"❌ Error scanning UI in {py_file.name}: {e}")
    
    def scan_chart_configurations(self):
        """Scan for chart-specific field usage patterns"""
        print("\n📈 Scanning chart configurations...")
        
        chart_configs = {}
        
        # Look for Plotly chart configurations in Python files
        python_files = list(self.dashboard_dir.glob('*.py')) if self.dashboard_dir.exists() else []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                relative_path = py_file.relative_to(self.project_root)
                persona, section = self.categorize_file_path(str(relative_path))
                
                # Find chart creation patterns
                chart_patterns = {
                    'bar_charts': r'px\.bar\((.*?)\)',
                    'line_charts': r'px\.line\((.*?)\)',
                    'scatter_plots': r'px\.scatter\((.*?)\)',
                    'pie_charts': r'px\.pie\((.*?)\)',
                    'histogram': r'px\.histogram\((.*?)\)',
                    'box_plots': r'px\.box\((.*?)\)'
                }
                
                file_charts = {
                    'persona': persona,
                    'section': section,
                    'file_path': str(relative_path)
                }
                for chart_type, pattern in chart_patterns.items():
                    matches = re.findall(pattern, content, re.DOTALL)
                    chart_fields = []
                    
                    for match in matches:
                        # Extract field parameters from chart creation
                        field_params = re.findall(r'([xy]|color|size|hover_name|facet_col)=[\'"]?(\w+)[\'"]?', match)
                        chart_fields.extend(field_params)
                    
                    if chart_fields:
                        file_charts[chart_type] = chart_fields
                
                if len([k for k in file_charts.keys() if k not in ['persona', 'section', 'file_path']]) > 0:
                    chart_configs[py_file.name] = file_charts
                    
            except Exception as e:
                print(f"❌ Error scanning charts in {py_file.name}: {e}")
        
        self.all_fields['chart_fields'] = chart_configs
    
    def generate_field_summary(self) -> Dict:
        """Generate a comprehensive summary of all discovered fields"""
        print("\n📋 Generating field summary...")
        
        summary = {
            'total_csv_files': len(self.all_fields['csv_columns']),
            'total_python_files': len(self.all_fields['display_functions']),
            'field_categories': {},
            'renaming_candidates': {},
            'persona_breakdown': {}
        }
        
        # Collect all unique field names by category
        all_column_names = set()
        all_ui_labels = set()
        all_chart_fields = set()
        all_dropdown_options = set()
        
        # Track by persona
        persona_stats = {}
        
        # From CSV files
        for file_info in self.all_fields['csv_columns'].values():
            all_column_names.update(file_info['columns'])
            persona = file_info.get('persona', 'General')
            
            if persona not in persona_stats:
                persona_stats[persona] = {'csv_files': 0, 'total_columns': 0}
            persona_stats[persona]['csv_files'] += 1
            persona_stats[persona]['total_columns'] += len(file_info['columns'])
            
            for col, unique_vals in file_info['unique_values'].items():
                if isinstance(unique_vals, list):
                    all_dropdown_options.update([str(v) for v in unique_vals])
        
        # From Python files
        for file_info in self.all_fields['display_functions'].values():
            if 'dataframe_columns' in file_info:
                all_column_names.update(file_info['dataframe_columns'])
            if 'plotly_fields' in file_info:
                for field_list in file_info['plotly_fields'].values():
                    all_chart_fields.update(field_list)
        
        # From UI elements
        for file_info in self.all_fields['ui_labels'].values():
            for key, label_list in file_info.items():
                if isinstance(label_list, list):
                    all_ui_labels.update(label_list)
        
        summary['field_categories'] = {
            'csv_columns': sorted(list(all_column_names)),
            'ui_labels': sorted(list(all_ui_labels)),
            'chart_fields': sorted(list(all_chart_fields)),
            'dropdown_options': sorted(list(all_dropdown_options))
        }
        
        summary['persona_breakdown'] = persona_stats
        
        # Identify common renaming candidates
        summary['renaming_candidates'] = self.identify_renaming_candidates(
            all_column_names, all_ui_labels, all_chart_fields
        )
        
        return summary
    
    def identify_renaming_candidates(self, columns: Set, labels: Set, chart_fields: Set) -> Dict:
        """Identify fields that are good candidates for renaming"""
        candidates = {
            'technical_names': [],      # Fields with technical/code-like names
            'abbreviations': [],        # Abbreviated field names
            'inconsistent_naming': [],  # Fields with inconsistent naming patterns
            'user_facing_labels': []    # Labels that users see directly
        }
        
        all_fields = columns.union(labels).union(chart_fields)
        
        for field in all_fields:
            field_lower = str(field).lower()
            
            # Technical/code-like names (contains underscores, camelCase, etc.)
            if '_' in field or re.search(r'[a-z][A-Z]', field):
                candidates['technical_names'].append(field)
            
            # Abbreviations (short, all caps, or obvious abbreviations)
            if len(field) <= 4 and field.isupper():
                candidates['abbreviations'].append(field)
            elif any(abbrev in field_lower for abbrev in ['ytd', 'roi', 'cfo', 'cio', 'cto', 'kpi']):
                candidates['abbreviations'].append(field)
            
            # User-facing labels (spaces, proper capitalization)
            if ' ' in field and any(word[0].isupper() for word in field.split()):
                candidates['user_facing_labels'].append(field)
        
        return candidates
    
    def export_enhanced_field_mappings(self):
        """Export field mappings organized by sheets and tabs"""
        output_dir = self.project_root / 'field_enumeration_output_v2'
        output_dir.mkdir(exist_ok=True)
        
        print(f"\n📊 Creating enhanced field mappings organized by sheets and tabs...")
        
        # Export comprehensive field list (JSON)
        with open(output_dir / 'all_fields_comprehensive_v2.json', 'w') as f:
            json.dump(self.all_fields, f, indent=2, default=str)
        
        # Create organized Excel workbook with multiple sheets
        self.create_organized_excel_workbook(output_dir)
        
        # Create persona-specific CSV files
        self.create_persona_csv_files(output_dir)
        
        # Create section-specific CSV files
        self.create_section_csv_files(output_dir)
        
        print(f"\n✅ Enhanced field enumeration complete!")
        print(f"📁 Output saved to: {output_dir}")
        print(f"📄 Files created:")
        print(f"   - all_fields_comprehensive_v2.json (detailed analysis)")
        print(f"   - field_mapping_organized.xlsx (Excel with multiple sheets)")
        print(f"   - persona_*.csv files (one per persona)")
        print(f"   - section_*.csv files (one per dashboard section)")
    
    def create_organized_excel_workbook(self, output_dir):
        """Create Excel workbook with organized sheets and tabs"""
        try:
            # Collect all fields with metadata
            all_field_data = []
            
            # Process CSV files
            for file_path, file_info in self.all_fields['csv_columns'].items():
                persona = file_info.get('persona', 'General')
                section = file_info.get('section', 'General')
                
                for col in file_info['columns']:
                    viz_info = file_info.get('visualization_fields', {})
                    usage_type = self.determine_field_usage_type(col, viz_info)
                    
                    all_field_data.append({
                        'field_name': col,
                        'persona': persona,
                        'section': section,
                        'source_type': 'CSV Column',
                        'source_file': file_path,
                        'usage_type': usage_type,
                        'sample_values': str(file_info['sample_values'].get(col, [])[:3]),
                        'unique_count': len(file_info['unique_values'].get(col, [])),
                        'suggested_new_name': '',
                        'renaming_priority': self.assess_renaming_priority(col),
                        'notes': ''
                    })
                    
                    # Also add dropdown options as separate fields
                    for unique_val in file_info['unique_values'].get(col, [])[:10]:  # Limit to 10
                        all_field_data.append({
                            'field_name': str(unique_val),
                            'persona': persona,
                            'section': section,
                            'source_type': 'Dropdown Option',
                            'source_file': file_path,
                            'usage_type': f'Dropdown value for {col}',
                            'sample_values': '',
                            'unique_count': 1,
                            'suggested_new_name': '',
                            'renaming_priority': 'Low',
                            'notes': f'Dropdown option for column: {col}'
                        })
            
            # Process Python files
            for file_path, file_info in self.all_fields['display_functions'].items():
                persona = file_info.get('persona', 'General')
                section = file_info.get('section', 'General')
                
                # Add UI elements
                for ui_type, ui_items in file_info.get('streamlit_elements', {}).items():
                    if isinstance(ui_items, list):
                        for item in ui_items:
                            all_field_data.append({
                                'field_name': str(item),
                                'persona': persona,
                                'section': section,
                                'source_type': f'UI Element - {ui_type}',
                                'source_file': file_path,
                                'usage_type': ui_type.replace('_', ' ').title(),
                                'sample_values': '',
                                'unique_count': 1,
                                'suggested_new_name': '',
                                'renaming_priority': self.assess_renaming_priority(str(item)),
                                'notes': ''
                            })
            
            # Create DataFrame
            df = pd.DataFrame(all_field_data)
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(output_dir / 'field_mapping_organized.xlsx', engine='openpyxl') as writer:
                # Overview sheet
                df.to_excel(writer, sheet_name='All Fields', index=False)
                
                # Persona-specific sheets
                for persona in df['persona'].unique():
                    persona_df = df[df['persona'] == persona].copy()
                    sheet_name = persona.replace(' - ', '_').replace(' ', '_')[:31]  # Excel sheet name limit
                    persona_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Section-specific sheets
                for section in df['section'].unique():
                    if section != 'General':  # Skip general section to avoid clutter
                        section_df = df[df['section'] == section].copy()
                        sheet_name = section.replace(' ', '_')[:31]  # Excel sheet name limit
                        section_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # High priority renaming sheet
                high_priority_df = df[df['renaming_priority'] == 'High'].copy()
                if not high_priority_df.empty:
                    high_priority_df.to_excel(writer, sheet_name='High_Priority_Renames', index=False)
        
        except Exception as e:
            print(f"⚠️ Could not create Excel file: {e}")
            print("📝 Creating CSV files instead...")
    
    def create_persona_csv_files(self, output_dir):
        """Create separate CSV files for each persona"""
        # Collect fields by persona
        persona_fields = {}
        
        # From CSV files
        for file_path, file_info in self.all_fields['csv_columns'].items():
            persona = file_info.get('persona', 'General')
            if persona not in persona_fields:
                persona_fields[persona] = []
            
            for col in file_info['columns']:
                persona_fields[persona].append({
                    'field_name': col,
                    'section': file_info.get('section', 'General'),
                    'source_type': 'CSV Column',
                    'source_file': file_path,
                    'sample_values': str(file_info['sample_values'].get(col, [])[:3]),
                    'suggested_new_name': '',
                    'notes': ''
                })
        
        # Create CSV for each persona
        for persona, fields in persona_fields.items():
            if fields:  # Only create if there are fields
                df = pd.DataFrame(fields)
                filename = f"persona_{persona.lower().replace(' - ', '_').replace(' ', '_')}.csv"
                df.to_csv(output_dir / filename, index=False)
    
    def create_section_csv_files(self, output_dir):
        """Create separate CSV files for each dashboard section"""
        # Collect fields by section
        section_fields = {}
        
        # From CSV files
        for file_path, file_info in self.all_fields['csv_columns'].items():
            section = file_info.get('section', 'General')
            if section not in section_fields:
                section_fields[section] = []
            
            for col in file_info['columns']:
                section_fields[section].append({
                    'field_name': col,
                    'persona': file_info.get('persona', 'General'),
                    'source_type': 'CSV Column',
                    'source_file': file_path,
                    'sample_values': str(file_info['sample_values'].get(col, [])[:3]),
                    'suggested_new_name': '',
                    'notes': ''
                })
        
        # Create CSV for each section
        for section, fields in section_fields.items():
            if fields and section != 'General':  # Only create if there are fields and not general
                df = pd.DataFrame(fields)
                filename = f"section_{section.lower().replace(' ', '_').replace('&', 'and')}.csv"
                df.to_csv(output_dir / filename, index=False)
    
    def determine_field_usage_type(self, field_name: str, viz_info: Dict) -> str:
        """Determine how a field is likely used in visualizations"""
        usage_types = []
        
        if field_name in viz_info.get('dropdown_candidates', []):
            usage_types.append('Dropdown')
        if field_name in viz_info.get('numeric_fields', []):
            usage_types.append('Chart Axis')
        if field_name in viz_info.get('date_fields', []):
            usage_types.append('Time Series')
        if field_name in viz_info.get('categorical_fields', []):
            usage_types.append('Color/Group')
        if field_name in viz_info.get('filter_fields', []):
            usage_types.append('Filter')
        
        return ', '.join(usage_types) if usage_types else 'Data Field'
    
    def assess_renaming_priority(self, field_name: str) -> str:
        """Assess renaming priority for a field"""
        field_lower = str(field_name).lower()
        
        # High priority: technical names, abbreviations
        if ('_' in field_name or 
            len(field_name) <= 4 and field_name.isupper() or
            any(abbrev in field_lower for abbrev in ['ytd', 'roi', 'cfo', 'cio', 'cto', 'kpi'])):
            return 'High'
        
        # Medium priority: camelCase, inconsistent naming
        if re.search(r'[a-z][A-Z]', field_name):
            return 'Medium'
        
        # Low priority: already user-friendly
        if ' ' in field_name and any(word[0].isupper() for word in field_name.split()):
            return 'Low'
        
        return 'Medium'

def main():
    """Run the enhanced field enumeration process"""
    print("🎓 Paul Quinn College IT Analytics Suite - Enhanced Field Enumerator V2")
    print("=" * 70)
    
    # Initialize enumerator
    enumerator = DashboardFieldEnumeratorV2()
    
    # Run comprehensive scan
    summary = enumerator.scan_all_fields()
    
    # Display summary
    print(f"\n📊 ENHANCED FIELD ENUMERATION SUMMARY:")
    print(f"CSV Files Scanned: {summary['total_csv_files']}")
    print(f"Python Files Scanned: {summary['total_python_files']}")
    
    if 'persona_breakdown' in summary:
        print(f"\n👥 Persona Breakdown:")
        for persona, stats in summary['persona_breakdown'].items():
            print(f"  {persona}: {stats['csv_files']} files, {stats['total_columns']} columns")
    
    if 'field_categories' in summary:
        for category, fields in summary['field_categories'].items():
            print(f"{category.replace('_', ' ').title()}: {len(fields)} fields")
    
    print(f"\n🎯 Renaming candidates identified:")
    if 'renaming_candidates' in summary:
        for category, candidates in summary['renaming_candidates'].items():
            if candidates:
                print(f"  {category.replace('_', ' ').title()}: {len(candidates)} fields")
    
    print(f"\n✅ Enhanced field enumeration complete! Check the organized output files.")

if __name__ == "__main__":
    main()