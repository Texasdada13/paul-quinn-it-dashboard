"""
Paul Quinn College IT Analytics Suite - Field Enumeration Script
This script scans through all dashboard components to extract field names for renaming exercises
"""

import os
import pandas as pd
import json
import re
from pathlib import Path
from typing import Dict, List, Set
import ast
import inspect

class DashboardFieldEnumerator:
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
        
        # Storage for all discovered fields
        self.all_fields = {
            'csv_columns': {},
            'display_functions': {},
            'metric_names': {},
            'chart_fields': {},
            'ui_labels': {}
        }
    
    def scan_all_fields(self) -> Dict:
        """Main method to scan all fields across the dashboard"""
        print("🔍 Starting comprehensive field enumeration...")
        print(f"📁 Project root: {self.project_root}")
        print(f"📊 Dashboard dir: {self.dashboard_dir}")
        print(f"📈 Metrics dir: {self.metrics_dir}")
        
        # Scan different types of fields
        self.scan_csv_files()
        self.scan_python_files()
        self.scan_display_functions()
        self.scan_ui_elements()
        
        # Generate summary
        summary = self.generate_field_summary()
        
        # Export results
        self.export_field_mappings()
        
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
                file_info = {
                    'columns': list(df.columns),
                    'sample_values': {},
                    'unique_values': {},
                    'row_count': len(df)
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
                print(f"✅ {csv_file.name}: {len(df.columns)} columns, {len(df)} rows")
                
            except Exception as e:
                print(f"❌ Error reading {csv_file.name}: {e}")
    
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
                file_info = {
                    'dataframe_columns': self.extract_dataframe_columns(content),
                    'plotly_fields': self.extract_plotly_fields(content),
                    'streamlit_elements': self.extract_streamlit_elements(content),
                    'variable_names': self.extract_variable_names(content),
                    'string_literals': self.extract_display_strings(content)
                }
                
                self.all_fields['display_functions'][str(relative_path)] = file_info
                print(f"✅ {py_file.name}: Extracted field references")
                
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
            sys.path.append(str(self.dashboard_dir))
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
                    
                    # Extract field usage from the source
                    fields = self.extract_fields_from_function_source(source)
                    function_fields[method_name] = fields
                    
                except Exception as e:
                    print(f"⚠️ Could not analyze {method_name}: {e}")
            
            self.all_fields['display_functions']['loader_methods'] = function_fields
            
        except Exception as e:
            print(f"⚠️ Could not import dashboard_metric_loader: {e}")
    
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
    
    def scan_ui_elements(self):
        """Scan for UI element labels and dropdown options"""
        print("\n🖥️ Scanning UI elements...")
        
        # This method looks for hardcoded UI text
        if self.dashboard_dir.exists():
            for py_file in self.dashboard_dir.glob('*.py'):
                try:
                    with open(py_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract UI text patterns
                    ui_patterns = {
                        'tab_labels': r'st\.tabs\(\[(.*?)\]',
                        'selectbox_labels': r'st\.selectbox\([\'"]([^"\']*)[\'"]',
                        'metric_titles': r'st\.metric\([\'"]([^"\']*)[\'"]',
                        'header_text': r'st\.(?:header|subheader|title)\([\'"]([^"\']*)[\'"]',
                        'markdown_headers': r'#+\s*([^\n]+)'
                    }
                    
                    file_ui = {}
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
                
                # Find chart creation patterns
                chart_patterns = {
                    'bar_charts': r'px\.bar\((.*?)\)',
                    'line_charts': r'px\.line\((.*?)\)',
                    'scatter_plots': r'px\.scatter\((.*?)\)',
                    'pie_charts': r'px\.pie\((.*?)\)',
                    'histogram': r'px\.histogram\((.*?)\)',
                    'box_plots': r'px\.box\((.*?)\)'
                }
                
                file_charts = {}
                for chart_type, pattern in chart_patterns.items():
                    matches = re.findall(pattern, content, re.DOTALL)
                    chart_fields = []
                    
                    for match in matches:
                        # Extract field parameters from chart creation
                        field_params = re.findall(r'([xy]|color|size|hover_name|facet_col)=[\'"]?(\w+)[\'"]?', match)
                        chart_fields.extend(field_params)
                    
                    if chart_fields:
                        file_charts[chart_type] = chart_fields
                
                if file_charts:
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
            'renaming_candidates': {}
        }
        
        # Collect all unique field names by category
        all_column_names = set()
        all_ui_labels = set()
        all_chart_fields = set()
        all_dropdown_options = set()
        
        # From CSV files
        for file_info in self.all_fields['csv_columns'].values():
            all_column_names.update(file_info['columns'])
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
            for label_list in file_info.values():
                if isinstance(label_list, list):
                    all_ui_labels.update(label_list)
        
        summary['field_categories'] = {
            'csv_columns': sorted(list(all_column_names)),
            'ui_labels': sorted(list(all_ui_labels)),
            'chart_fields': sorted(list(all_chart_fields)),
            'dropdown_options': sorted(list(all_dropdown_options))
        }
        
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
    
    def export_field_mappings(self):
        """Export field mappings to files for renaming reference"""
        output_dir = self.project_root / 'field_enumeration_output'
        output_dir.mkdir(exist_ok=True)
        
        # Export comprehensive field list
        with open(output_dir / 'all_fields_comprehensive.json', 'w') as f:
            json.dump(self.all_fields, f, indent=2, default=str)
        
        # Export renaming template CSV
        all_unique_fields = set()
        
        # Collect all unique field names
        for file_info in self.all_fields['csv_columns'].values():
            all_unique_fields.update(file_info['columns'])
        
        for file_info in self.all_fields['display_functions'].values():
            if 'dataframe_columns' in file_info:
                all_unique_fields.update(file_info['dataframe_columns'])
        
        for file_info in self.all_fields['ui_labels'].values():
            for label_list in file_info.values():
                if isinstance(label_list, list):
                    all_unique_fields.update(label_list)
        
        # Create renaming template
        renaming_df = pd.DataFrame({
            'original_field_name': sorted(list(all_unique_fields)),
            'suggested_new_name': [''] * len(all_unique_fields),
            'field_type': [''] * len(all_unique_fields),
            'found_in_files': [''] * len(all_unique_fields),
            'usage_context': [''] * len(all_unique_fields),
            'notes': [''] * len(all_unique_fields)
        })
        
        renaming_df.to_csv(output_dir / 'field_renaming_template.csv', index=False)
        
        print(f"\n✅ Field enumeration complete!")
        print(f"📁 Output saved to: {output_dir}")
        print(f"📄 Files created:")
        print(f"   - all_fields_comprehensive.json (detailed analysis)")
        print(f"   - field_renaming_template.csv (renaming worksheet)")

def main():
    """Run the field enumeration process"""
    print("🎓 Paul Quinn College IT Analytics Suite - Field Enumerator")
    print("=" * 60)
    
    # Initialize enumerator
    enumerator = DashboardFieldEnumerator()
    
    # Run comprehensive scan
    summary = enumerator.scan_all_fields()
    
    # Display summary
    print(f"\n📊 FIELD ENUMERATION SUMMARY:")
    print(f"CSV Files Scanned: {summary['total_csv_files']}")
    print(f"Python Files Scanned: {summary['total_python_files']}")
    
    if 'field_categories' in summary:
        for category, fields in summary['field_categories'].items():
            print(f"{category.replace('_', ' ').title()}: {len(fields)} fields")
    
    print(f"\n🎯 Renaming candidates identified:")
    if 'renaming_candidates' in summary:
        for category, candidates in summary['renaming_candidates'].items():
            if candidates:
                print(f"  {category.replace('_', ' ').title()}: {len(candidates)} fields")
    
    print(f"\n✅ Field enumeration complete! Check the output files for detailed analysis.")

if __name__ == "__main__":
    main()