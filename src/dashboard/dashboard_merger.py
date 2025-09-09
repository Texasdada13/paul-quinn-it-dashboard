#!/usr/bin/env python3
"""
Dashboard Feature Merger
Compares two Streamlit dashboard files and extracts specific features
"""

import re
import ast
from pathlib import Path
from typing import List, Dict, Tuple
import difflib

class DashboardMerger:
    def __init__(self, main_file: str, source_file: str):
        self.main_file = Path(main_file)
        self.source_file = Path(source_file)
        self.main_content = self.main_file.read_text()
        self.source_content = self.source_file.read_text()
    
    def find_differences(self) -> List[str]:
        """Find major differences between the files"""
        main_lines = self.main_content.splitlines()
        source_lines = self.source_content.splitlines()
        
        differ = difflib.unified_diff(
            main_lines, 
            source_lines, 
            fromfile=str(self.main_file),
            tofile=str(self.source_file),
            lineterm=''
        )
        
        differences = []
        for line in differ:
            if line.startswith('+ ') and 'AI' in line:
                differences.append(line[2:])  # Remove '+ ' prefix
        
        return differences
    
    def extract_ai_tabs(self) -> List[str]:
        """Extract AI-related tab content from source file"""
        ai_sections = []
        
        # Look for AI tab content
        ai_patterns = [
            r'(?:".*AI.*Optimization.*".*?:.*?)(?=elif|\Z)',
            r'(?:AI Strategic.*?:.*?)(?=\n\s*(?:elif|else|\Z))',
            r'with\s+tab.*?AI.*?:.*?(?=\n(?:with\s+tab|\Z))'
        ]
        
        for pattern in ai_patterns:
            matches = re.findall(pattern, self.source_content, re.DOTALL | re.IGNORECASE)
            ai_sections.extend(matches)
        
        return ai_sections
    
    def extract_ai_imports(self) -> List[str]:
        """Extract AI-related imports from source file"""
        ai_imports = []
        
        import_patterns = [
            r'from.*ai.*import.*',
            r'import.*ai.*',
            r'from.*optimization.*import.*'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, self.source_content, re.IGNORECASE)
            ai_imports.extend(matches)
        
        return ai_imports
    
    def extract_ai_functions(self) -> List[str]:
        """Extract AI-related functions from source file"""
        ai_functions = []
        
        # Parse AST to find functions
        try:
            tree = ast.parse(self.source_content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if 'ai' in node.name.lower() or 'optimization' in node.name.lower():
                        # Extract function code
                        func_lines = self.source_content.splitlines()
                        start_line = node.lineno - 1
                        
                        # Find end of function
                        end_line = start_line + 1
                        indent_level = len(func_lines[start_line]) - len(func_lines[start_line].lstrip())
                        
                        for i in range(start_line + 1, len(func_lines)):
                            line = func_lines[i]
                            if line.strip() and (len(line) - len(line.lstrip())) <= indent_level:
                                end_line = i
                                break
                        
                        function_code = '\n'.join(func_lines[start_line:end_line])
                        ai_functions.append(function_code)
        
        except SyntaxError:
            print("Warning: Could not parse source file for function extraction")
        
        return ai_functions
    
    def create_ai_component(self, output_file: str = "ai_optimization_component.py"):
        """Create standalone AI component file"""
        ai_imports = self.extract_ai_imports()
        ai_functions = self.extract_ai_functions()
        ai_tabs = self.extract_ai_tabs()
        
        component_template = '''"""
AI Strategic Optimization Component
Extracted from withAI_Updates_fully_integrated_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

{imports}

{functions}

def render_ai_optimization_tab():
    """Main function to render AI Strategic Optimization tab"""
    st.markdown("### 🤖 AI Strategic Optimization")
    
    # Add your extracted AI tab content here
    {tab_content}
    
if __name__ == "__main__":
    render_ai_optimization_tab()
'''
        
        imports_str = '\n'.join(ai_imports)
        functions_str = '\n\n'.join(ai_functions)
        tab_content = '\n    '.join(ai_tabs) if ai_tabs else 'st.info("AI optimization features extracted")'
        
        component_code = component_template.format(
            imports=imports_str,
            functions=functions_str,
            tab_content=tab_content
        )
        
        with open(output_file, 'w') as f:
            f.write(component_code)
        
        print(f"✅ AI component created: {output_file}")
        return output_file
    
    def add_ai_tab_to_main(self, backup: bool = True) -> str:
        """Add AI tab to main dashboard file"""
        if backup:
            backup_file = f"{self.main_file.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
            Path(backup_file).write_text(self.main_content)
            print(f"✅ Backup created: {backup_file}")
        
        updated_content = self.main_content
        
        # 1. Add import for AI component
        ai_import = "from ai_optimization_component import render_ai_optimization_tab\n"
        
        # Find where to add import (after existing imports)
        import_pattern = r'((?:from|import).*\n)*'
        match = re.search(import_pattern, updated_content)
        if match:
            insert_pos = match.end()
            updated_content = updated_content[:insert_pos] + ai_import + updated_content[insert_pos:]
        
        # 2. Add AI tab to tabs list
        tabs_pattern = r'st\.tabs\(\[(.*?)\]\)'
        match = re.search(tabs_pattern, updated_content, re.DOTALL)
        if match:
            existing_tabs = match.group(1)
            new_tabs = existing_tabs + ', "🤖 AI Optimization"'
            updated_content = updated_content.replace(match.group(0), f'st.tabs([{new_tabs}])')
        
        # 3. Add AI tab content
        # Find the last tab handling and add AI tab after it
        last_tab_pattern = r'(with tabs\[\d+\]:.*?)(\n\n# Footer|$)'
        
        ai_tab_content = '''
with tabs[-1]:  # AI Optimization tab
    render_ai_optimization_tab()
'''
        
        # Insert AI tab content before footer or end of file
        footer_pattern = r'(\n# Footer|\nst\.markdown\(.*Footer.*\)|\Z)'
        match = re.search(footer_pattern, updated_content)
        if match:
            insert_pos = match.start()
            updated_content = updated_content[:insert_pos] + ai_tab_content + updated_content[insert_pos:]
        
        # Save updated file
        output_file = f"{self.main_file.stem}_with_AI.py"
        Path(output_file).write_text(updated_content)
        
        print(f"✅ Updated dashboard created: {output_file}")
        return output_file

def main():
    """Main execution function"""
    print("🔄 Dashboard Feature Merger")
    print("=" * 50)
    
    # Initialize merger
    merger = DashboardMerger(
        main_file="fully_integrated_dashboard.py",
        source_file="withAI_Updates_fully_integrated_dashboard.py"
    )
    
    # Find differences
    print("\n📊 Finding differences...")
    differences = merger.find_differences()
    print(f"Found {len(differences)} AI-related differences")
    
    # Extract AI features
    print("\n🔍 Extracting AI features...")
    ai_imports = merger.extract_ai_imports()
    ai_functions = merger.extract_ai_functions()
    ai_tabs = merger.extract_ai_tabs()
    
    print(f"Found {len(ai_imports)} AI imports")
    print(f"Found {len(ai_functions)} AI functions")
    print(f"Found {len(ai_tabs)} AI tab sections")
    
    # Create AI component
    print("\n🔧 Creating AI component...")
    component_file = merger.create_ai_component()
    
    # Integrate into main dashboard
    print("\n🔗 Integrating into main dashboard...")
    integrated_file = merger.add_ai_tab_to_main()
    
    print("\n✅ Integration complete!")
    print(f"📁 Files created:")
    print(f"   - {component_file} (standalone AI component)")
    print(f"   - {integrated_file} (integrated dashboard)")
    print(f"\n🚀 Test with: streamlit run {integrated_file}")

if __name__ == "__main__":
    main()