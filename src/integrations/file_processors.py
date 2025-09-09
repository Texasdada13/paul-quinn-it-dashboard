"""
File Processors for Contract Data
Handles CSV, Excel, and other file formats for data ingestion
"""

import pandas as pd
import os
import numpy as np
from pathlib import Path
from typing import Union, Dict, List, Optional, Tuple
import logging
from datetime import datetime
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContractFileProcessor:
    """Process contract data from various file formats"""
    
    # Standard column mappings for ISSA format
    STANDARD_COLUMNS = {
        'vendor_name': 'Vendor',
        'vendor': 'Vendor',
        'supplier': 'Vendor',
        'company': 'Vendor',
        'system_product': 'System/Product',
        'product': 'System/Product',
        'service': 'System/Product',
        'description': 'System/Product',
        'start_date': 'Contract Start Date',
        'begin_date': 'Contract Start Date',
        'effective_date': 'Contract Start Date',
        'end_date': 'Contract End Date',
        'expiry_date': 'Contract End Date',
        'expiration_date': 'Contract End Date',
        'annual_spend': 'Annual Spend',
        'annual_cost': 'Annual Spend',
        'yearly_cost': 'Annual Spend',
        'cost': 'Annual Spend',
        'amount': 'Annual Spend',
        'value': 'Annual Spend',
        'renewal_option': 'Renewal Option',
        'auto_renewal': 'Renewal Option',
        'renewal': 'Renewal Option'
    }
    
    # Common date formats to try
    DATE_FORMATS = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y/%m/%d',
        '%m-%d-%Y',
        '%d-%m-%Y',
        '%B %d, %Y',
        '%b %d, %Y',
        '%d %B %Y',
        '%d %b %Y'
    ]
    
    def __init__(self, upload_directory: str = "data/uploads"):
        self.upload_dir = Path(upload_directory)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processing_log = []
        
    def process_file(self, file_path: Union[str, Path], 
                    mapping_config: Dict = None, 
                    sheet_name: str = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Process uploaded contract file with flexible column mapping
        
        Args:
            file_path: Path to the file to process
            mapping_config: Dictionary mapping source columns to standard columns
            sheet_name: For Excel files, specify sheet name
            
        Returns:
            Tuple of (processed_dataframe, processing_summary)
        """
        
        file_path = Path(file_path)
        processing_summary = {
            'file_name': file_path.name,
            'file_size': file_path.stat().st_size if file_path.exists() else 0,
            'rows_input': 0,
            'rows_output': 0,
            'columns_mapped': 0,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Read file based on extension
            df = self._read_file(file_path, sheet_name)
            processing_summary['rows_input'] = len(df)
            
            # Auto-detect column mappings if not provided
            if mapping_config is None:
                mapping_config = self._auto_detect_columns(df)
            
            processing_summary['columns_mapped'] = len(mapping_config)
            
            # Apply column mapping
            df_mapped = self._apply_column_mapping(df, mapping_config)
            
            # Standardize data types and clean data
            df_standardized = self._standardize_contract_data(df_mapped, processing_summary)
            
            # Validate data quality
            df_validated = self._validate_data_quality(df_standardized, processing_summary)
            
            processing_summary['rows_output'] = len(df_validated)
            
            logger.info(f"Successfully processed {file_path.name}: {processing_summary['rows_input']} → {processing_summary['rows_output']} rows")
            
            return df_validated, processing_summary
            
        except Exception as e:
            error_msg = f"Error processing file {file_path.name}: {str(e)}"
            logger.error(error_msg)
            processing_summary['errors'].append(error_msg)
            return pd.DataFrame(), processing_summary
    
    def _read_file(self, file_path: Path, sheet_name: str = None) -> pd.DataFrame:
        """Read file based on extension"""
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = file_path.suffix.lower()
        
        if extension == '.csv':
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    return pd.read_csv(file_path, encoding=encoding)
                except UnicodeDecodeError:
                    continue
            raise ValueError("Could not read CSV file with any encoding")
            
        elif extension in ['.xlsx', '.xls']:
            if sheet_name:
                return pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                # Read first sheet by default
                return pd.read_excel(file_path)
                
        elif extension == '.json':
            return pd.read_json(file_path)
            
        elif extension in ['.txt', '.tsv']:
            return pd.read_csv(file_path, sep='\t')
            
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _auto_detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """Auto-detect column mappings based on column names"""
        
        mapping = {}
        df_columns_lower = [col.lower().strip() for col in df.columns]
        
        for idx, col in enumerate(df_columns_lower):
            # Clean column name for matching
            clean_col = re.sub(r'[^\w\s]', '', col).strip()
            clean_col = re.sub(r'\s+', '_', clean_col)
            
            # Check for exact matches first
            if clean_col in self.STANDARD_COLUMNS:
                mapping[df.columns[idx]] = self.STANDARD_COLUMNS[clean_col]
                continue
            
            # Check for partial matches
            for pattern, standard_col in self.STANDARD_COLUMNS.items():
                if pattern in clean_col or clean_col in pattern:
                    mapping[df.columns[idx]] = standard_col
                    break
            
            # Special cases for common variations
            if any(keyword in clean_col for keyword in ['vendor', 'supplier', 'company']) and 'Vendor' not in mapping.values():
                mapping[df.columns[idx]] = 'Vendor'
            elif any(keyword in clean_col for keyword in ['product', 'service', 'system', 'description']) and 'System/Product' not in mapping.values():
                mapping[df.columns[idx]] = 'System/Product'
            elif any(keyword in clean_col for keyword in ['start', 'begin', 'effective']) and 'date' in clean_col:
                mapping[df.columns[idx]] = 'Contract Start Date'
            elif any(keyword in clean_col for keyword in ['end', 'expir', 'terminat']) and 'date' in clean_col:
                mapping[df.columns[idx]] = 'Contract End Date'
            elif any(keyword in clean_col for keyword in ['cost', 'spend', 'amount', 'value', 'price']) and any(keyword in clean_col for keyword in ['annual', 'yearly', 'total']):
                mapping[df.columns[idx]] = 'Annual Spend'
        
        logger.info(f"Auto-detected {len(mapping)} column mappings")
        return mapping
    
    def _apply_column_mapping(self, df: pd.DataFrame, mapping_config: Dict) -> pd.DataFrame:
        """Apply column mapping to standardize column names"""
        
        # Create a copy to avoid modifying original
        df_mapped = df.copy()
        
        # Rename columns based on mapping
        df_mapped = df_mapped.rename(columns=mapping_config)
        
        # Ensure all required standard columns exist
        required_columns = [
            'Vendor', 'System/Product', 'Contract Start Date', 
            'Contract End Date', 'Annual Spend', 'Renewal Option'
        ]
        
        for col in required_columns:
            if col not in df_mapped.columns:
                df_mapped[col] = ''
        
        return df_mapped
    
    def _standardize_contract_data(self, df: pd.DataFrame, summary: Dict) -> pd.DataFrame:
        """Standardize contract data to ISSA format"""
        
        df_std = df.copy()
        
        # Clean text fields
        text_columns = ['Vendor', 'System/Product', 'Renewal Option']
        for col in text_columns:
            if col in df_std.columns:
                df_std[col] = df_std[col].astype(str).str.strip()
                df_std[col] = df_std[col].replace('nan', '')
        
        # Standardize date columns
        date_columns = ['Contract Start Date', 'Contract End Date']
        for col in date_columns:
            if col in df_std.columns:
                df_std[col] = self._standardize_dates(df_std[col], summary)
        
        # Standardize monetary columns
        if 'Annual Spend' in df_std.columns:
            df_std['Annual Spend'] = self._standardize_currency(df_std['Annual Spend'], summary)
        
        # Add derived fields
        df_std = self._add_derived_fields(df_std)
        
        # Add metadata
        df_std['Source_System'] = 'File_Upload'
        df_std['Import_Date'] = datetime.now().isoformat()
        df_std['File_Name'] = summary.get('file_name', 'Unknown')
        
        return df_std
    
    def _standardize_dates(self, date_series: pd.Series, summary: Dict) -> pd.Series:
        """Standardize date formats"""
        
        standardized_dates = pd.Series(index=date_series.index, dtype='datetime64[ns]')
        
        for idx, date_val in date_series.items():
            if pd.isna(date_val) or str(date_val).strip() == '':
                continue
                
            date_str = str(date_val).strip()
            
            # Try each date format
            for fmt in self.DATE_FORMATS:
                try:
                    standardized_dates[idx] = pd.to_datetime(date_str, format=fmt)
                    break
                except:
                    continue
            
            # If no format worked, try pandas auto-parsing
            if pd.isna(standardized_dates[idx]):
                try:
                    standardized_dates[idx] = pd.to_datetime(date_str)
                except:
                    summary['warnings'].append(f"Could not parse date: {date_str}")
        
        return standardized_dates
    
    def _standardize_currency(self, currency_series: pd.Series, summary: Dict) -> pd.Series:
        """Standardize currency values"""
        
        standardized_currency = pd.Series(index=currency_series.index, dtype='float64')
        
        for idx, val in currency_series.items():
            if pd.isna(val):
                standardized_currency[idx] = 0.0
                continue
            
            # Convert to string and clean
            val_str = str(val).strip()
            
            # Remove currency symbols and common formatting
            cleaned_val = re.sub(r'[$,€£¥]', '', val_str)
            cleaned_val = re.sub(r'[^\d.-]', '', cleaned_val)
            
            try:
                standardized_currency[idx] = float(cleaned_val)
            except:
                summary['warnings'].append(f"Could not parse currency value: {val_str}")
                standardized_currency[idx] = 0.0
        
        return standardized_currency
    
    def _add_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add calculated/derived fields"""
        
        # Calculate days until expiry
        if 'Contract End Date' in df.columns:
            today = pd.Timestamp.now()
            df['Days Until Expiry'] = (df['Contract End Date'] - today).dt.days
            
            # Add alert status based on days until expiry
            df['Alert Status'] = df['Days Until Expiry'].apply(
                lambda x: 'Critical' if pd.notna(x) and x < 30 
                         else 'Warning' if pd.notna(x) and x < 90 
                         else 'OK' if pd.notna(x) 
                         else 'Unknown'
            )
        
        # Calculate contract duration
        if 'Contract Start Date' in df.columns and 'Contract End Date' in df.columns:
            df['Contract Duration (Days)'] = (df['Contract End Date'] - df['Contract Start Date']).dt.days
        
        # Standardize renewal options
        if 'Renewal Option' in df.columns:
            renewal_mapping = {
                'yes': 'Yes',
                'no': 'No',
                'true': 'Yes',
                'false': 'No',
                '1': 'Yes',
                '0': 'No',
                'auto': 'Auto-Renew',
                'manual': 'Manual',
                'optional': 'Optional'
            }
            
            df['Renewal Option'] = df['Renewal Option'].str.lower().map(renewal_mapping).fillna('Unknown')
        
        return df
    
    def _validate_data_quality(self, df: pd.DataFrame, summary: Dict) -> pd.DataFrame:
        """Validate data quality and flag issues"""
        
        validation_issues = []
        
        # Check for required fields
        required_fields = ['Vendor', 'Contract End Date']
        for field in required_fields:
            if field in df.columns:
                null_count = df[field].isna().sum()
                if null_count > 0:
                    validation_issues.append(f"{field}: {null_count} missing values")
        
        # Check for reasonable date ranges
        if 'Contract End Date' in df.columns:
            future_dates = df['Contract End Date'] > (pd.Timestamp.now() + pd.Timedelta(days=3650))  # 10 years
            if future_dates.any():
                validation_issues.append(f"Contract End Date: {future_dates.sum()} dates more than 10 years in future")
        
        # Check for reasonable spending amounts
        if 'Annual Spend' in df.columns:
            high_spend = df['Annual Spend'] > 10000000  # $10M
            if high_spend.any():
                validation_issues.append(f"Annual Spend: {high_spend.sum()} contracts over $10M")
        
        # Remove rows with critical missing data
        before_count = len(df)
        df_clean = df.dropna(subset=['Vendor'])  # Must have vendor
        after_count = len(df_clean)
        
        if before_count != after_count:
            validation_issues.append(f"Removed {before_count - after_count} rows with missing vendor information")
        
        summary['warnings'].extend(validation_issues)
        
        return df_clean
    
    def get_column_suggestions(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Get suggestions for column mapping"""
        
        suggestions = {}
        
        # Standard columns we're looking for
        target_columns = [
            'Vendor', 'System/Product', 'Contract Start Date', 
            'Contract End Date', 'Annual Spend', 'Renewal Option'
        ]
        
        for target_col in target_columns:
            suggestions[target_col] = []
            
            # Score each source column for similarity
            for source_col in df.columns:
                score = self._calculate_column_similarity(source_col, target_col)
                if score > 0.3:  # Threshold for suggestion
                    suggestions[target_col].append((source_col, score))
            
            # Sort by score and take top 3
            suggestions[target_col].sort(key=lambda x: x[1], reverse=True)
            suggestions[target_col] = [col for col, score in suggestions[target_col][:3]]
        
        return suggestions
    
    def _calculate_column_similarity(self, source_col: str, target_col: str) -> float:
        """Calculate similarity score between source and target column names"""
        
        source_lower = source_col.lower()
        target_lower = target_col.lower()
        
        # Exact match
        if source_lower == target_lower:
            return 1.0
        
        # Keyword matching
        target_keywords = {
            'vendor': ['vendor', 'supplier', 'company', 'provider'],
            'system/product': ['product', 'service', 'system', 'description', 'item'],
            'contract start date': ['start', 'begin', 'effective', 'commence'],
            'contract end date': ['end', 'expir', 'terminat', 'finish'],
            'annual spend': ['cost', 'spend', 'amount', 'value', 'price', 'annual'],
            'renewal option': ['renewal', 'auto', 'extend', 'option']
        }
        
        keywords = target_keywords.get(target_lower, [])
        
        score = 0.0
        for keyword in keywords:
            if keyword in source_lower:
                score += 0.5
        
        # Date field detection
        if 'date' in target_lower and 'date' in source_lower:
            score += 0.3
        
        return min(score, 1.0)
    
    def export_processing_report(self, processing_summaries: List[Dict], output_path: str = None) -> str:
        """Export processing report to file"""
        
        if output_path is None:
            output_path = self.upload_dir / f"processing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_files_processed': len(processing_summaries),
            'summaries': processing_summaries
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Processing report exported to {output_path}")
        return str(output_path)

# Batch processing utilities
class BatchFileProcessor:
    """Process multiple files in batch"""
    
    def __init__(self, upload_directory: str = "data/uploads"):
        self.processor = ContractFileProcessor(upload_directory)
        
    def process_directory(self, directory_path: str, file_pattern: str = "*") -> Tuple[pd.DataFrame, List[Dict]]:
        """Process all files in a directory"""
        
        directory = Path(directory_path)
        files = list(directory.glob(file_pattern))
        
        all_data = []
        all_summaries = []
        
        for file_path in files:
            try:
                df, summary = self.processor.process_file(file_path)
                if not df.empty:
                    all_data.append(df)
                all_summaries.append(summary)
                
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                all_summaries.append({
                    'file_name': file_path.name,
                    'error': str(e)
                })
        
        # Consolidate all data
        if all_data:
            consolidated_df = pd.concat(all_data, ignore_index=True)
        else:
            consolidated_df = pd.DataFrame()
        
        return consolidated_df, all_summaries

# Example usage
if __name__ == "__main__":
    # Example usage
    processor = ContractFileProcessor("data/uploads")
    
    # Example processing (uncomment to test with actual file)
    # df, summary = processor.process_file("data/uploads/contracts.csv")
    # print(f"Processed {len(df)} contracts")
    # print(f"Summary: {summary}")
    
    print("File processor module loaded successfully")