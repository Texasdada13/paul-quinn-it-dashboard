"""
Automated Data Pipeline for ISSA Contract Data
Handles scheduled data updates and processing
"""

import schedule
import time
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json
import sys
import os
from typing import Dict, List, Optional, Tuple
import traceback

# Add parent directories to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent
sys.path.append(str(src_dir))

from integrations.data_connectors import DataSourceManager, SAPContractConnector, PaycomHRConnector
from integrations.file_processors import ContractFileProcessor, BatchFileProcessor
from security.data_encryption import SecureDataHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ContractDataPipeline:
    """Automated pipeline for contract data updates"""
    
    def __init__(self, config_file: str = "pipeline_config.json"):
        """
        Initialize the data pipeline
        
        Args:
            config_file: Path to pipeline configuration file
        """
        self.config = self._load_config(config_file)
        self.data_manager = DataSourceManager()
        self.file_processor = ContractFileProcessor()
        self.security_handler = SecureDataHandler()
        self.last_update = None
        self.pipeline_stats = {
            'total_runs': 0,
            'successful_runs': 0,
            'failed_runs': 0,
            'last_run_time': None,
            'last_error': None,
            'records_processed': 0
        }
        
        # Setup data directories
        self._setup_directories()
        
        # Initialize connectors based on config
        self._initialize_connectors()
    
    def _load_config(self, config_file: str) -> Dict:
        """Load pipeline configuration"""
        
        default_config = {
            "data_sources": {
                "sap": {
                    "enabled": False,
                    "base_url": "",
                    "client_id": "",
                    "client_secret": ""
                },
                "paycom": {
                    "enabled": False,
                    "api_key": "",
                    "company_id": ""
                },
                "file_upload": {
                    "enabled": True,
                    "watch_directory": "data/uploads",
                    "processed_directory": "data/processed"
                }
            },
            "pipeline_settings": {
                "schedule_frequency": "daily",
                "schedule_time": "06:00",
                "data_retention_days": 30,
                "enable_encryption": True,
                "backup_enabled": True,
                "quality_checks": True
            },
            "output_settings": {
                "cfo_metrics_path": "src/metrics/cfo/cfo_contract_expiration_alerts_examples.csv",
                "backup_directory": "data/backups",
                "reports_directory": "data/reports"
            }
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                # Merge with defaults
                default_config.update(user_config)
            else:
                # Create default config file
                with open(config_file, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info(f"Created default configuration file: {config_file}")
                
        except Exception as e:
            logger.error(f"Error loading config: {e}. Using defaults.")
        
        return default_config
    
    def _setup_directories(self):
        """Create necessary directories"""
        
        directories = [
            "data/uploads",
            "data/processed", 
            "data/backups",
            "data/reports",
            "src/metrics/cfo",
            "src/metrics/cio",
            "src/metrics/cto"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def _initialize_connectors(self):
        """Initialize data connectors based on configuration"""
        
        try:
            # SAP Connector
            if self.config["data_sources"]["sap"]["enabled"]:
                sap_config = self.config["data_sources"]["sap"]
                sap_connector = SAPContractConnector(
                    base_url=sap_config["base_url"],
                    client_id=sap_config["client_id"],
                    client_secret=sap_config["client_secret"]
                )
                self.data_manager.register_connector("SAP", sap_connector)
                logger.info("SAP connector initialized")
            
            # Paycom Connector
            if self.config["data_sources"]["paycom"]["enabled"]:
                paycom_config = self.config["data_sources"]["paycom"]
                paycom_connector = PaycomHRConnector(
                    api_key=paycom_config["api_key"],
                    company_id=paycom_config["company_id"]
                )
                self.data_manager.register_connector("Paycom", paycom_connector)
                logger.info("Paycom connector initialized")
                
        except Exception as e:
            logger.error(f"Error initializing connectors: {e}")
    
    def run_pipeline(self, manual_trigger: bool = False) -> Dict[str, any]:
        """
        Execute full data pipeline
        
        Args:
            manual_trigger: Whether this is a manual or scheduled run
            
        Returns:
            Pipeline execution summary
        """
        
        start_time = datetime.now()
        pipeline_result = {
            'success': False,
            'start_time': start_time.isoformat(),
            'end_time': None,
            'duration_seconds': 0,
            'records_processed': 0,
            'sources_processed': 0,
            'errors': [],
            'warnings': [],
            'data_quality_score': 0,
            'manual_trigger': manual_trigger
        }
        
        try:
            logger.info("=" * 50)
            logger.info("Starting contract data pipeline...")
            logger.info(f"Trigger: {'Manual' if manual_trigger else 'Scheduled'}")
            
            # Step 1: Backup existing data
            if self.config["pipeline_settings"]["backup_enabled"]:
                self._backup_existing_data()
            
            # Step 2: Process file uploads
            file_data = self._process_file_uploads(pipeline_result)
            
            # Step 3: Fetch from API sources
            api_data = self._fetch_api_data(pipeline_result)
            
            # Step 4: Consolidate all data
            consolidated_data = self._consolidate_data(file_data, api_data, pipeline_result)
            
            # Step 5: Data quality validation
            if self.config["pipeline_settings"]["quality_checks"]:
                validated_data = self._validate_data_quality(consolidated_data, pipeline_result)
            else:
                validated_data = consolidated_data
            
            # Step 6: Apply security if enabled
            if self.config["pipeline_settings"]["enable_encryption"]:
                secured_data = self._apply_security(validated_data, pipeline_result)
            else:
                secured_data = validated_data
            
            # Step 7: Save processed data
            self._save_processed_data(secured_data, pipeline_result)
            
            # Step 8: Update metrics files
            self._update_metrics_files(secured_data, pipeline_result)
            
            # Step 9: Generate reports
            self._generate_reports(secured_data, pipeline_result)
            
            # Step 10: Cleanup old data
            self._cleanup_old_data()
            
            # Update pipeline stats
            self.pipeline_stats['successful_runs'] += 1
            self.pipeline_stats['records_processed'] += pipeline_result['records_processed']
            self.last_update = start_time
            
            pipeline_result['success'] = True
            logger.info("Pipeline completed successfully!")
            
        except Exception as e:
            error_msg = f"Pipeline failed: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            
            pipeline_result['errors'].append(error_msg)
            self.pipeline_stats['failed_runs'] += 1
            self.pipeline_stats['last_error'] = error_msg
        
        finally:
            # Update timing and stats
            end_time = datetime.now()
            pipeline_result['end_time'] = end_time.isoformat()
            pipeline_result['duration_seconds'] = (end_time - start_time).total_seconds()
            
            self.pipeline_stats['total_runs'] += 1
            self.pipeline_stats['last_run_time'] = end_time.isoformat()
            
            # Save pipeline stats
            self._save_pipeline_stats()
            
            logger.info(f"Pipeline completed in {pipeline_result['duration_seconds']:.2f} seconds")
            logger.info("=" * 50)
        
        return pipeline_result
    
    def _backup_existing_data(self):
        """Backup existing data files"""
        
        try:
            backup_dir = Path(self.config["output_settings"]["backup_directory"])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Files to backup
            files_to_backup = [
                self.config["output_settings"]["cfo_metrics_path"],
                "data/processed/latest_contracts.csv"
            ]
            
            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    file_name = Path(file_path).name
                    backup_name = f"{timestamp}_{file_name}"
                    backup_path = backup_dir / backup_name
                    
                    # Copy file to backup
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    
            logger.info(f"Data backed up to {backup_dir}")
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
    
    def _process_file_uploads(self, pipeline_result: Dict) -> pd.DataFrame:
        """Process uploaded files"""
        
        try:
            upload_dir = Path(self.config["data_sources"]["file_upload"]["watch_directory"])
            
            if not upload_dir.exists():
                return pd.DataFrame()
            
            # Get all processable files
            file_patterns = ["*.csv", "*.xlsx", "*.xls"]
            all_files = []
            
            for pattern in file_patterns:
                all_files.extend(upload_dir.glob(pattern))
            
            if not all_files:
                logger.info("No files found for processing")
                return pd.DataFrame()
            
            # Process files in batch
            batch_processor = BatchFileProcessor(str(upload_dir))
            consolidated_data, summaries = batch_processor.process_directory(str(upload_dir))
            
            # Move processed files
            processed_dir = Path(self.config["data_sources"]["file_upload"]["processed_directory"])
            for file_path in all_files:
                try:
                    new_path = processed_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_path.name}"
                    file_path.rename(new_path)
                except Exception as e:
                    logger.warning(f"Could not move file {file_path}: {e}")
            
            pipeline_result['sources_processed'] += len(all_files)
            pipeline_result['records_processed'] += len(consolidated_data)
            
            logger.info(f"Processed {len(all_files)} files, {len(consolidated_data)} records")
            return consolidated_data
            
        except Exception as e:
            error_msg = f"File processing failed: {e}"
            pipeline_result['errors'].append(error_msg)
            logger.error(error_msg)
            return pd.DataFrame()
    
    def _fetch_api_data(self, pipeline_result: Dict) -> pd.DataFrame:
        """Fetch data from API sources"""
        
        try:
            if not self.data_manager.connectors:
                logger.info("No API connectors configured")
                return pd.DataFrame()
            
            api_data = self.data_manager.get_consolidated_contract_data()
            
            if not api_data.empty:
                pipeline_result['sources_processed'] += len(self.data_manager.connectors)
                pipeline_result['records_processed'] += len(api_data)
                logger.info(f"Fetched {len(api_data)} records from API sources")
            
            return api_data
            
        except Exception as e:
            error_msg = f"API data fetch failed: {e}"
            pipeline_result['errors'].append(error_msg)
            logger.error(error_msg)
            return pd.DataFrame()
    
    def _consolidate_data(self, file_data: pd.DataFrame, api_data: pd.DataFrame, 
                         pipeline_result: Dict) -> pd.DataFrame:
        """Consolidate data from all sources"""
        
        try:
            all_data = []
            
            if not file_data.empty:
                all_data.append(file_data)
            
            if not api_data.empty:
                all_data.append(api_data)
            
            if not all_data:
                logger.warning("No data to consolidate")
                return pd.DataFrame()
            
            # Combine all data
            consolidated = pd.concat(all_data, ignore_index=True, sort=False)
            
            # Remove duplicates
            before_dedup = len(consolidated)
            consolidated = self._deduplicate_contracts(consolidated)
            after_dedup = len(consolidated)
            
            if before_dedup != after_dedup:
                pipeline_result['warnings'].append(f"Removed {before_dedup - after_dedup} duplicate records")
            
            logger.info(f"Consolidated {len(consolidated)} unique records")
            return consolidated
            
        except Exception as e:
            error_msg = f"Data consolidation failed: {e}"
            pipeline_result['errors'].append(error_msg)
            logger.error(error_msg)
            return pd.DataFrame()
    
    def _deduplicate_contracts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate contracts"""
        
        if df.empty:
            return df
        
        # Create composite key for deduplication
        df['_dedup_key'] = (
            df.get('Vendor', '').astype(str).str.upper().str.strip() + '|' +
            df.get('System/Product', '').astype(str).str.upper().str.strip() + '|' +
            df.get('Contract End Date', '').astype(str)
        )
        
        # Keep most recent record for each key
        df['_timestamp'] = pd.to_datetime(df.get('Import_Date', datetime.now()))
        df_sorted = df.sort_values('_timestamp', ascending=False)
        df_deduped = df_sorted.drop_duplicates('_dedup_key', keep='first')
        
        # Clean up temporary columns
        df_deduped = df_deduped.drop(['_dedup_key', '_timestamp'], axis=1)
        
        return df_deduped.reset_index(drop=True)
    
    def _validate_data_quality(self, df: pd.DataFrame, pipeline_result: Dict) -> pd.DataFrame:
        """Validate data quality and calculate score"""
        
        if df.empty:
            pipeline_result['data_quality_score'] = 0
            return df
        
        quality_checks = {
            'vendor_completeness': self._check_completeness(df, 'Vendor'),
            'date_validity': self._check_date_validity(df),
            'amount_validity': self._check_amount_validity(df),
            'future_dates': self._check_future_dates(df),
            'duplicate_check': self._check_remaining_duplicates(df)
        }
        
        # Calculate overall quality score
        quality_score = sum(quality_checks.values()) / len(quality_checks) * 100
        pipeline_result['data_quality_score'] = round(quality_score, 2)
        
        # Log quality issues
        for check, passed in quality_checks.items():
            if not passed:
                pipeline_result['warnings'].append(f"Data quality issue: {check}")
        
        logger.info(f"Data quality score: {quality_score:.1f}%")
        
        # Remove invalid records
        validated_df = self._clean_invalid_records(df, pipeline_result)
        
        return validated_df
    
    def _check_completeness(self, df: pd.DataFrame, column: str) -> bool:
        """Check if column has acceptable completeness"""
        if column not in df.columns:
            return False
        
        completeness = (df[column].notna() & (df[column] != '')).sum() / len(df)
        return completeness >= 0.8  # 80% completeness threshold
    
    def _check_date_validity(self, df: pd.DataFrame) -> bool:
        """Check if dates are valid"""
        date_columns = ['Contract Start Date', 'Contract End Date']
        
        for col in date_columns:
            if col in df.columns:
                try:
                    pd.to_datetime(df[col], errors='coerce')
                except:
                    return False
        return True
    
    def _check_amount_validity(self, df: pd.DataFrame) -> bool:
        """Check if amounts are reasonable"""
        if 'Annual Spend' not in df.columns:
            return True
        
        try:
            amounts = pd.to_numeric(df['Annual Spend'], errors='coerce')
            # Check for reasonable range (0 to $50M)
            valid_amounts = amounts.between(0, 50000000, inclusive='both')
            return valid_amounts.sum() / len(amounts) >= 0.9
        except:
            return False
    
    def _check_future_dates(self, df: pd.DataFrame) -> bool:
        """Check for unreasonably future dates"""
        if 'Contract End Date' not in df.columns:
            return True
        
        try:
            end_dates = pd.to_datetime(df['Contract End Date'], errors='coerce')
            future_limit = datetime.now() + timedelta(days=3650)  # 10 years
            reasonable_dates = end_dates <= future_limit
            return reasonable_dates.sum() / len(end_dates) >= 0.95
        except:
            return False
    
    def _check_remaining_duplicates(self, df: pd.DataFrame) -> bool:
        """Check for remaining duplicates"""
        if df.empty:
            return True
        
        # Simple duplicate check on vendor + product
        if 'Vendor' in df.columns and 'System/Product' in df.columns:
            composite_key = df['Vendor'].astype(str) + '|' + df['System/Product'].astype(str)
            duplicates = composite_key.duplicated().sum()
            return duplicates / len(df) < 0.05  # Less than 5% duplicates
        
        return True
    
    def _clean_invalid_records(self, df: pd.DataFrame, pipeline_result: Dict) -> pd.DataFrame:
        """Remove invalid records"""
        
        if df.empty:
            return df
        
        original_count = len(df)
        
        # Remove records with missing vendor
        df_clean = df[df['Vendor'].notna() & (df['Vendor'] != '')]
        
        # Remove records with invalid amounts
        if 'Annual Spend' in df.columns:
            df_clean = df_clean[
                pd.to_numeric(df_clean['Annual Spend'], errors='coerce').between(0, 50000000)
            ]
        
        cleaned_count = len(df_clean)
        removed_count = original_count - cleaned_count
        
        if removed_count > 0:
            pipeline_result['warnings'].append(f"Removed {removed_count} invalid records")
            logger.warning(f"Removed {removed_count} invalid records")
        
        return df_clean
    
    def _apply_security(self, df: pd.DataFrame, pipeline_result: Dict) -> pd.DataFrame:
        """Apply security measures to sensitive data"""
        
        try:
            if df.empty:
                return df
            
            # Encrypt sensitive columns
            secured_df = self.security_handler.encrypt_dataframe(
                df, 
                sensitivity_level='medium'
            )
            
            logger.info("Security measures applied to sensitive data")
            return secured_df
            
        except Exception as e:
            error_msg = f"Security application failed: {e}"
            pipeline_result['errors'].append(error_msg)
            logger.error(error_msg)
            return df  # Return original if security fails
    
    def _save_processed_data(self, df: pd.DataFrame, pipeline_result: Dict):
        """Save processed data to files"""
        
        try:
            if df.empty:
                logger.warning("No data to save")
                return
            
            # Save main processed file
            output_path = "data/processed/latest_contracts.csv"
            df.to_csv(output_path, index=False)
            
            # Save timestamped version
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            timestamped_path = f"data/processed/contracts_{timestamp}.csv"
            df.to_csv(timestamped_path, index=False)
            
            logger.info(f"Processed data saved to {output_path}")
            
        except Exception as e:
            error_msg = f"Failed to save processed data: {e}"
            pipeline_result['errors'].append(error_msg)
            logger.error(error_msg)
    
    def _update_metrics_files(self, df: pd.DataFrame, pipeline_result: Dict):
        """Update metrics files for dashboard"""
        
        try:
            if df.empty:
                return
            
            # Update CFO contract metrics
            cfo_path = self.config["output_settings"]["cfo_metrics_path"]
            
            # Ensure directory exists
            Path(cfo_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Decrypt data for metrics if encrypted
            if hasattr(df, 'attrs') and df.attrs.get('encrypted_columns'):
                metrics_df = self.security_handler.decrypt_dataframe(df)
            else:
                metrics_df = df.copy()
            
            # Save to CFO metrics
            metrics_df.to_csv(cfo_path, index=False)
            
            # Update other persona metrics as needed
            # ... (can add CIO, CTO specific processing here)
            
            logger.info("Metrics files updated")
            
        except Exception as e:
            error_msg = f"Failed to update metrics files: {e}"
            pipeline_result['errors'].append(error_msg)
            logger.error(error_msg)
    
    def _generate_reports(self, df: pd.DataFrame, pipeline_result: Dict):
        """Generate summary reports"""
        
        try:
            if df.empty:
                return
            
            reports_dir = Path(self.config["output_settings"]["reports_directory"])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Generate summary report
            summary_report = self._create_summary_report(df, pipeline_result)
            
            report_path = reports_dir / f"pipeline_report_{timestamp}.json"
            with open(report_path, 'w') as f:
                json.dump(summary_report, f, indent=2)
            
            logger.info(f"Pipeline report saved to {report_path}")
            
        except Exception as e:
            logger.error(f"Failed to generate reports: {e}")
    
    def _create_summary_report(self, df: pd.DataFrame, pipeline_result: Dict) -> Dict:
        """Create summary report"""
        
        report = {
            'pipeline_execution': pipeline_result,
            'data_summary': {
                'total_contracts': len(df),
                'unique_vendors': df['Vendor'].nunique() if 'Vendor' in df.columns else 0,
                'contracts_expiring_30_days': 0,
                'contracts_expiring_90_days': 0,
                'total_annual_spend': 0
            },
            'pipeline_stats': self.pipeline_stats.copy()
        }
        
        # Calculate expiring contracts
        if 'Days Until Expiry' in df.columns:
            report['data_summary']['contracts_expiring_30_days'] = (df['Days Until Expiry'] <= 30).sum()
            report['data_summary']['contracts_expiring_90_days'] = (df['Days Until Expiry'] <= 90).sum()
        
        # Calculate total spend
        if 'Annual Spend' in df.columns:
            report['data_summary']['total_annual_spend'] = df['Annual Spend'].sum()
        
        return report
    
    def _cleanup_old_data(self):
        """Cleanup old data files based on retention policy"""
        
        try:
            retention_days = self.config["pipeline_settings"]["data_retention_days"]
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            # Cleanup directories
            cleanup_dirs = [
                "data/processed",
                "data/backups", 
                "data/reports"
            ]
            
            for directory in cleanup_dirs:
                dir_path = Path(directory)
                if dir_path.exists():
                    for file_path in dir_path.glob("*"):
                        if file_path.is_file():
                            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                            if file_time < cutoff_date:
                                file_path.unlink()
                                logger.debug(f"Deleted old file: {file_path}")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def _save_pipeline_stats(self):
        """Save pipeline statistics"""
        
        try:
            stats_path = "data/pipeline_stats.json"
            with open(stats_path, 'w') as f:
                json.dump(self.pipeline_stats, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save pipeline stats: {e}")
    
    def schedule_pipeline(self):
        """Setup scheduled pipeline execution"""
        
        frequency = self.config["pipeline_settings"]["schedule_frequency"]
        schedule_time = self.config["pipeline_settings"]["schedule_time"]
        
        if frequency == "daily":
            schedule.every().day.at(schedule_time).do(self.run_pipeline)
            logger.info(f"Pipeline scheduled daily at {schedule_time}")
            
        elif frequency == "hourly":
            schedule.every().hour.do(self.run_pipeline)
            logger.info("Pipeline scheduled hourly")
            
        elif frequency == "weekly":
            schedule.every().week.at(schedule_time).do(self.run_pipeline)
            logger.info(f"Pipeline scheduled weekly at {schedule_time}")
    
    def get_pipeline_status(self) -> Dict:
        """Get current pipeline status"""
        
        status = {
            'pipeline_stats': self.pipeline_stats,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'configured_sources': len(self.data_manager.connectors),
            'data_source_status': self.data_manager.get_data_source_status(),
            'next_scheduled_run': None  # Could add schedule info here
        }
        
        return status

def start_pipeline_daemon(config_file: str = "pipeline_config.json"):
    """Start the pipeline daemon for scheduled execution"""
    
    pipeline = ContractDataPipeline(config_file)
    pipeline.schedule_pipeline()
    
    logger.info("Pipeline daemon started. Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Pipeline daemon stopped")

def run_manual_pipeline(config_file: str = "pipeline_config.json") -> Dict:
    """Run pipeline manually and return results"""
    
    pipeline = ContractDataPipeline(config_file)
    return pipeline.run_pipeline(manual_trigger=True)

# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ISSA Data Pipeline")
    parser.add_argument("--mode", choices=["daemon", "manual"], default="manual",
                       help="Run mode: daemon for scheduled execution, manual for one-time run")
    parser.add_argument("--config", default="pipeline_config.json",
                       help="Configuration file path")
    
    args = parser.parse_args()
    
    if args.mode == "daemon":
        start_pipeline_daemon(args.config)
    else:
        result = run_manual_pipeline(args.config)
        print(f"Pipeline completed. Success: {result['success']}")
        if result['errors']:
            print(f"Errors: {result['errors']}")