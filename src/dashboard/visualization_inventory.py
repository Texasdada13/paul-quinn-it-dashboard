"""
ISSA Dashboard Visualization Inventory System
Automatically catalogs all visualizations across the entire dashboard
"""

import ast
import os
import re
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict

@dataclass
class Visualization:
    """Data class for storing visualization information"""
    viz_id: str
    viz_type: str
    library: str
    persona: str
    tab_name: str
    data_source: str
    location: str  # File and line number
    key: Optional[str] = None
    chart_config: Dict = field(default_factory=dict)
    data_columns: List[str] = field(default_factory=list)
    interactive: bool = False
    styling: Dict = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)

class DashboardVisualizationInventory:
    """Complete visualization inventory system for ISSA dashboard"""
    
    def __init__(self, dashboard_file: str = None):
        # Get the directory where this script is located
        self.script_dir = Path(__file__).parent
        
        # If dashboard file specified, use it; otherwise look in current directory
        if dashboard_file:
            self.dashboard_path = Path(dashboard_file)
        else:
            # Look for the dashboard file in the same directory
            self.dashboard_path = self.script_dir / 'fully_integrated_dashboard.py'
        
        self.visualizations = []
        self.viz_patterns = {
            # Streamlit patterns
            'st.metric': r'st\.metric\s*\([^)]+\)',
            'st.progress': r'st\.progress\s*\([^)]+\)',
            'st.dataframe': r'st\.dataframe\s*\([^)]+\)',
            'st.table': r'st\.table\s*\([^)]+\)',
            'st.button': r'st\.button\s*\([^)]+\)',
            'st.selectbox': r'st\.selectbox\s*\([^)]+\)',
            'st.multiselect': r'st\.multiselect\s*\([^)]+\)',
            'st.tabs': r'st\.tabs\s*\([^)]+\)',
            'st.columns': r'st\.columns\s*\([^)]+\)',
            'st.expander': r'st\.expander\s*\([^)]+\)',
            'st.plotly_chart': r'st\.plotly_chart\s*\([^)]+\)',
            
            # Plotly Express patterns
            'px.bar': r'px\.bar\s*\([^)]+\)',
            'px.line': r'px\.line\s*\([^)]+\)',
            'px.scatter': r'px\.scatter\s*\([^)]+\)',
            'px.pie': r'px\.pie\s*\([^)]+\)',
            'px.timeline': r'px\.timeline\s*\([^)]+\)',
            'px.sunburst': r'px\.sunburst\s*\([^)]+\)',
            'px.box': r'px\.box\s*\([^)]+\)',
            
            # Plotly Graph Objects patterns
            'go.Figure': r'go\.Figure\s*\([^)]+\)',
            'go.Indicator': r'go\.Indicator\s*\([^)]+\)',
            'go.Bar': r'go\.Bar\s*\([^)]+\)',
            'go.Scatter': r'go\.Scatter\s*\([^)]+\)',
            'go.Scatterpolar': r'go\.Scatterpolar\s*\([^)]+\)',
            'go.Pie': r'go\.Pie\s*\([^)]+\)',
            
            # Custom HTML/CSS patterns
            'st.markdown': r'st\.markdown\s*\([^)]*unsafe_allow_html=True[^)]*\)',
            'HTML div': r'<div[^>]*class=["\'][^"\']*box[^"\']*["\'][^>]*>',
            
            # DataFrame styling
            'df.style': r'\.style\.',
        }
        
        self.persona_mappings = {
            'CFO': ['budget', 'contract', 'grant', 'vendor', 'roi', 'spend', 'compliance'],
            'CIO': ['digital', 'strategic', 'business', 'risk', 'transformation'],
            'CTO': ['infrastructure', 'cloud', 'security', 'automation', 'operations'],
            'PM': ['project', 'portfolio', 'timeline', 'resource', 'raid'],
            'HBCU': ['institutional', 'mission', 'student', 'benchmark']
        }
    
    def scan_dashboard_files(self) -> List[Path]:
        """Find all Python files in the dashboard directory"""
        python_files = []
        
        print(f"Starting scan from: {self.script_dir}")
        
        # Look for dashboard files in the current directory
        dashboard_files = list(self.script_dir.glob('*.py'))
        
        # Exclude the inventory script itself
        dashboard_files = [f for f in dashboard_files if f.name != 'visualization_inventory.py']
        
        print(f"Found {len(dashboard_files)} dashboard files in {self.script_dir}")
        python_files.extend(dashboard_files)
        
        # Look for metrics directory (go up one level then into metrics)
        metrics_path = self.script_dir.parent / 'metrics'
        if not metrics_path.exists():
            # Try current directory's parent
            metrics_path = self.script_dir.parent.parent / 'metrics'
        
        if metrics_path.exists():
            print(f"Found metrics directory at: {metrics_path}")
            for persona_dir in ['cfo', 'cio', 'cto', 'pm', 'hbcu']:
                persona_path = metrics_path / persona_dir
                if persona_path.exists():
                    persona_files = list(persona_path.glob('*.py'))
                    print(f"  Found {len(persona_files)} files in {persona_dir}/")
                    python_files.extend(persona_files)
        else:
            print(f"Warning: Metrics directory not found at expected location")
        
        return python_files
    
    def detect_persona(self, file_path: Path, content: str) -> str:
        """Detect which persona a visualization belongs to"""
        file_str = str(file_path).lower()
        content_lower = content.lower()
        
        # Check directory structure first
        if 'cfo' in file_str:
            return 'CFO'
        elif 'cio' in file_str:
            return 'CIO'
        elif 'cto' in file_str:
            return 'CTO'
        elif 'pm' in file_str or 'project' in file_str:
            return 'PM'
        elif 'hbcu' in file_str:
            return 'HBCU'
        
        # Then check content keywords
        for persona, keywords in self.persona_mappings.items():
            if any(keyword in content_lower for keyword in keywords):
                return persona
        
        return 'UNKNOWN'
    
    def extract_visualizations(self, file_path: Path) -> List[Visualization]:
        """Extract all visualizations from a Python file"""
        file_visualizations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            persona = self.detect_persona(file_path, content)
            
            # Search for each visualization pattern
            for viz_type, pattern in self.viz_patterns.items():
                matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
                
                for match in matches:
                    # Find line number
                    line_num = content[:match.start()].count('\n') + 1
                    
                    # Extract the matched code
                    viz_code = match.group()
                    
                    # Try to extract key if present
                    key_match = re.search(r'key\s*=\s*["\']([^"\']+)["\']', viz_code)
                    key = key_match.group(1) if key_match else None
                    
                    # Determine library
                    if viz_type.startswith('st.'):
                        library = 'streamlit'
                    elif viz_type.startswith('px.'):
                        library = 'plotly_express'
                    elif viz_type.startswith('go.'):
                        library = 'plotly_graph_objects'
                    else:
                        library = 'custom'
                    
                    # Create visualization object
                    viz = Visualization(
                        viz_id=f"{persona}_{viz_type}_{line_num}",
                        viz_type=viz_type,
                        library=library,
                        persona=persona,
                        tab_name=self.extract_tab_context(content, match.start()),
                        data_source=self.extract_data_source(viz_code),
                        location=f"{file_path.name}:{line_num}",
                        key=key,
                        interactive=viz_type not in ['st.metric', 'st.table', 'HTML div']
                    )
                    
                    file_visualizations.append(viz)
        
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return file_visualizations
    
    def extract_tab_context(self, content: str, position: int) -> str:
        """Find which tab a visualization belongs to"""
        # Look backwards for tab context
        before_content = content[:position]
        tab_matches = list(re.finditer(r'with tab[s]?\[[\d]+\]:|"([^"]+)".*?[\]\)]', before_content))
        
        if tab_matches:
            last_match = tab_matches[-1]
            if last_match.group(1):
                return last_match.group(1)
        
        return 'MAIN'
    
    def extract_data_source(self, viz_code: str) -> str:
        """Extract data source from visualization code"""
        # Look for common data patterns
        data_patterns = [
            r'data\s*=\s*([^\s,\)]+)',
            r'df\s*=\s*([^\s,\)]+)',
            r'\(([^,\s]+),\s*[xy]\s*=',
        ]
        
        for pattern in data_patterns:
            match = re.search(pattern, viz_code)
            if match:
                return match.group(1)
        
        return 'UNKNOWN'
    
    def analyze_metrics_csv(self, metrics_dir: Path) -> Dict:
        """Analyze CSV files for data points"""
        csv_analysis = {}
        
        for csv_file in metrics_dir.glob('**/*.csv'):
            try:
                df = pd.read_csv(csv_file)
                csv_analysis[csv_file.stem] = {
                    'rows': len(df),
                    'columns': list(df.columns),
                    'data_points': len(df) * len(df.columns),
                    'numeric_columns': df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                }
            except Exception as e:
                print(f"Error reading {csv_file}: {e}")
        
        return csv_analysis
    
    def run_complete_inventory(self) -> Dict:
        """Run complete visualization inventory"""
        print("Starting ISSA Dashboard Visualization Inventory...")
        print("="*60)
        
        # Scan all files
        files = self.scan_dashboard_files()
        print(f"\nTotal files to analyze: {len(files)}")
        print("-"*40)
        
        # Extract visualizations
        for file_path in files:
            file_vizs = self.extract_visualizations(file_path)
            self.visualizations.extend(file_vizs)
            if file_vizs:
                print(f"  ✓ {file_path.name}: {len(file_vizs)} visualizations")
        
        # Analyze CSV data
        metrics_dir = self.script_dir.parent / 'metrics'
        if not metrics_dir.exists():
            metrics_dir = self.script_dir.parent.parent / 'metrics'
        
        csv_analysis = self.analyze_metrics_csv(metrics_dir) if metrics_dir.exists() else {}
        
        # Generate summary statistics
        summary = self.generate_summary()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_visualizations': len(self.visualizations),
            'visualizations': [asdict(v) for v in self.visualizations],
            'csv_analysis': csv_analysis,
            'summary': summary
        }
    
    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        summary = {
            'total_count': len(self.visualizations),
            'by_persona': {},
            'by_type': {},
            'by_library': {},
            'interactive_count': sum(1 for v in self.visualizations if v.interactive),
            'with_keys': sum(1 for v in self.visualizations if v.key is not None)
        }
        
        # Count by persona
        for viz in self.visualizations:
            summary['by_persona'][viz.persona] = summary['by_persona'].get(viz.persona, 0) + 1
            summary['by_type'][viz.viz_type] = summary['by_type'].get(viz.viz_type, 0) + 1
            summary['by_library'][viz.library] = summary['by_library'].get(viz.library, 0) + 1
        
        return summary
    
    def export_to_database(self, output_file: str = 'visualization_inventory.db'):
        """Export inventory to SQLite database"""
        import sqlite3
        
        conn = sqlite3.connect(output_file)
        
        # Create visualizations DataFrame
        viz_df = pd.DataFrame([asdict(v) for v in self.visualizations])
        
        # Export to database
        viz_df.to_sql('visualizations', conn, if_exists='replace', index=False)
        
        # Create summary table
        summary_df = pd.DataFrame([self.generate_summary()])
        summary_df.to_sql('summary', conn, if_exists='replace', index=False)
        
        conn.close()
        print(f"Database exported to {output_file}")
    
    def export_to_excel(self, output_file: str = 'visualization_inventory.xlsx'):
        """Export inventory to Excel with multiple sheets"""
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main visualizations sheet
            viz_df = pd.DataFrame([asdict(v) for v in self.visualizations])
            viz_df.to_excel(writer, sheet_name='All_Visualizations', index=False)
            
            # Per-persona sheets
            for persona in viz_df['persona'].unique():
                persona_df = viz_df[viz_df['persona'] == persona]
                persona_df.to_excel(writer, sheet_name=f'{persona}_Vizs', index=False)
            
            # Summary sheet
            summary_df = pd.DataFrame([self.generate_summary()])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"Excel report exported to {output_file}")

# Usage
if __name__ == "__main__":
    # Initialize the inventory system - no need to specify path, it will find files automatically
    inventory = DashboardVisualizationInventory()
    
    # Run complete inventory
    results = inventory.run_complete_inventory()
    
    # Export results
    with open('visualization_inventory.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    inventory.export_to_database()
    inventory.export_to_excel()
    
    # Print summary
    print("\n" + "="*60)
    print("VISUALIZATION INVENTORY COMPLETE")
    print("="*60)
    print(f"Total Visualizations Found: {results['total_visualizations']}")
    print(f"\nBreakdown by Persona:")
    for persona, count in results['summary']['by_persona'].items():
        print(f"  {persona}: {count}")
    print(f"\nTop Visualization Types:")
    for viz_type, count in sorted(results['summary']['by_type'].items(), 
                                  key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {viz_type}: {count}")