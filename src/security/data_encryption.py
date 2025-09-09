"""
Data Encryption and Security Handler
Handles sensitive data encryption for ISSA dashboard
"""

import os
import pandas as pd
import numpy as np
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import json
import logging
from typing import List, Dict, Optional, Union
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureDataHandler:
    """Handle sensitive data with encryption and security"""
    
    # Define sensitive columns that should be encrypted
    SENSITIVE_COLUMNS = {
        'financial': ['Annual Spend', 'Contract Value', 'Cost', 'Budget', 'Amount'],
        'vendor': ['Vendor', 'Supplier', 'Company'],
        'personal': ['Email', 'Phone', 'SSN', 'Employee ID'],
        'contract': ['Contract Number', 'Agreement ID']
    }
    
    def __init__(self, encryption_key: Optional[str] = None, salt: Optional[bytes] = None):
        """
        Initialize secure data handler
        
        Args:
            encryption_key: Base64 encoded encryption key or password
            salt: Salt for key derivation (if using password)
        """
        self.salt = salt or os.urandom(16)
        self.key = self._get_or_create_key(encryption_key)
        self.cipher = Fernet(self.key)
        self.audit_log = []
        
    def _get_or_create_key(self, encryption_key: Optional[str] = None) -> bytes:
        """Get encryption key from environment or create new one"""
        
        if encryption_key:
            try:
                # Try to decode as base64 first (assuming it's a Fernet key)
                return base64.urlsafe_b64decode(encryption_key.encode())
            except:
                # If not base64, treat as password and derive key
                return self._derive_key_from_password(encryption_key)
        
        # Check environment variable
        env_key = os.getenv('ISSA_ENCRYPTION_KEY')
        if env_key:
            try:
                return base64.urlsafe_b64decode(env_key.encode())
            except:
                return self._derive_key_from_password(env_key)
        
        # Generate new key
        key = Fernet.generate_key()
        logger.warning(f"Generated new encryption key. Store securely: {key.decode()}")
        logger.warning("Set ISSA_ENCRYPTION_KEY environment variable to persist this key")
        return key
    
    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive encryption key from password using PBKDF2"""
        
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password_bytes))
    
    def encrypt_dataframe(self, df: pd.DataFrame, 
                         columns_to_encrypt: Optional[List[str]] = None,
                         sensitivity_level: str = 'auto') -> pd.DataFrame:
        """
        Encrypt sensitive columns in dataframe
        
        Args:
            df: DataFrame to encrypt
            columns_to_encrypt: Specific columns to encrypt (optional)
            sensitivity_level: 'high', 'medium', 'low', or 'auto'
            
        Returns:
            DataFrame with encrypted columns
        """
        
        if df.empty:
            return df
        
        encrypted_df = df.copy()
        
        # Determine columns to encrypt
        if columns_to_encrypt is None:
            columns_to_encrypt = self._identify_sensitive_columns(df, sensitivity_level)
        
        # Encrypt specified columns
        for col in columns_to_encrypt:
            if col in encrypted_df.columns:
                encrypted_df[col] = self._encrypt_column(encrypted_df[col], col)
                self._log_operation('encrypt', col, len(encrypted_df))
        
        # Add encryption metadata
        encrypted_df.attrs['encrypted_columns'] = columns_to_encrypt
        encrypted_df.attrs['encryption_timestamp'] = datetime.now().isoformat()
        
        return encrypted_df
    
    def decrypt_dataframe(self, df: pd.DataFrame, 
                         columns_to_decrypt: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Decrypt encrypted columns in dataframe
        
        Args:
            df: DataFrame with encrypted columns
            columns_to_decrypt: Specific columns to decrypt (optional)
            
        Returns:
            DataFrame with decrypted columns
        """
        
        if df.empty:
            return df
        
        decrypted_df = df.copy()
        
        # Determine columns to decrypt
        if columns_to_decrypt is None:
            columns_to_decrypt = df.attrs.get('encrypted_columns', [])
        
        # Decrypt specified columns
        for col in columns_to_decrypt:
            if col in decrypted_df.columns:
                decrypted_df[col] = self._decrypt_column(decrypted_df[col], col)
                self._log_operation('decrypt', col, len(decrypted_df))
        
        return decrypted_df
    
    def _identify_sensitive_columns(self, df: pd.DataFrame, sensitivity_level: str) -> List[str]:
        """Identify sensitive columns based on name patterns and content"""
        
        sensitive_cols = []
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Check against sensitive column patterns
            for category, patterns in self.SENSITIVE_COLUMNS.items():
                for pattern in patterns:
                    if pattern.lower() in col_lower:
                        if sensitivity_level == 'high' or (
                            sensitivity_level == 'auto' and 
                            self._assess_column_sensitivity(df[col], category) > 0.7
                        ):
                            sensitive_cols.append(col)
                            break
        
        return sensitive_cols
    
    def _assess_column_sensitivity(self, series: pd.Series, category: str) -> float:
        """Assess sensitivity score of a column (0-1)"""
        
        # Basic sensitivity assessment
        if category == 'financial':
            # Check if values look like monetary amounts
            try:
                numeric_series = pd.to_numeric(series, errors='coerce')
                if numeric_series.max() > 1000:  # Likely monetary values
                    return 0.9
            except:
                pass
        
        elif category == 'vendor':
            # Check if values look like company names
            unique_ratio = len(series.unique()) / len(series)
            if unique_ratio > 0.1:  # Good variety of unique values
                return 0.8
        
        return 0.5  # Default medium sensitivity
    
    def _encrypt_column(self, series: pd.Series, column_name: str) -> pd.Series:
        """Encrypt a single column"""
        
        encrypted_series = series.copy()
        
        for idx, value in series.items():
            if pd.notna(value) and str(value).strip():
                try:
                    # Convert to string and encrypt
                    value_str = str(value)
                    encrypted_bytes = self.cipher.encrypt(value_str.encode('utf-8'))
                    encrypted_series[idx] = base64.b64encode(encrypted_bytes).decode('utf-8')
                except Exception as e:
                    logger.error(f"Failed to encrypt value in {column_name}: {e}")
                    encrypted_series[idx] = value  # Keep original if encryption fails
        
        return encrypted_series
    
    def _decrypt_column(self, series: pd.Series, column_name: str) -> pd.Series:
        """Decrypt a single column"""
        
        decrypted_series = series.copy()
        
        for idx, value in series.items():
            if pd.notna(value) and str(value).strip():
                try:
                    # Decode and decrypt
                    encrypted_bytes = base64.b64decode(str(value).encode('utf-8'))
                    decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
                    decrypted_series[idx] = decrypted_bytes.decode('utf-8')
                except Exception as e:
                    logger.error(f"Failed to decrypt value in {column_name}: {e}")
                    decrypted_series[idx] = value  # Keep original if decryption fails
        
        return decrypted_series
    
    def _log_operation(self, operation: str, column: str, row_count: int):
        """Log encryption/decryption operations for audit"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'column': column,
            'row_count': row_count,
            'user': os.getenv('USER', 'system')
        }
        
        self.audit_log.append(log_entry)
        logger.info(f"Security operation: {operation} on {column} ({row_count} rows)")
    
    def create_masked_version(self, df: pd.DataFrame, 
                            mask_columns: Optional[List[str]] = None,
                            mask_type: str = 'partial') -> pd.DataFrame:
        """
        Create masked version of data for display/demo purposes
        
        Args:
            df: DataFrame to mask
            mask_columns: Columns to mask (optional)
            mask_type: 'partial', 'full', or 'hash'
            
        Returns:
            DataFrame with masked sensitive data
        """
        
        if df.empty:
            return df
        
        masked_df = df.copy()
        
        if mask_columns is None:
            mask_columns = self._identify_sensitive_columns(df, 'auto')
        
        for col in mask_columns:
            if col in masked_df.columns:
                masked_df[col] = self._apply_masking(masked_df[col], mask_type)
        
        return masked_df
    
    def _apply_masking(self, series: pd.Series, mask_type: str) -> pd.Series:
        """Apply masking to a series"""
        
        masked_series = series.copy()
        
        for idx, value in series.items():
            if pd.notna(value) and str(value).strip():
                value_str = str(value)
                
                if mask_type == 'partial':
                    # Show first 2 and last 2 characters
                    if len(value_str) > 6:
                        masked_series[idx] = value_str[:2] + '*' * (len(value_str) - 4) + value_str[-2:]
                    else:
                        masked_series[idx] = '*' * len(value_str)
                        
                elif mask_type == 'full':
                    masked_series[idx] = '*' * len(value_str)
                    
                elif mask_type == 'hash':
                    # Create deterministic hash for consistent masking
                    hash_obj = hashlib.md5(value_str.encode())
                    masked_series[idx] = hash_obj.hexdigest()[:8]
        
        return masked_series
    
    def validate_data_integrity(self, original_df: pd.DataFrame, 
                               processed_df: pd.DataFrame) -> Dict[str, bool]:
        """Validate data integrity after encryption/decryption"""
        
        validation_results = {
            'row_count_match': len(original_df) == len(processed_df),
            'column_count_match': len(original_df.columns) == len(processed_df.columns),
            'non_encrypted_columns_match': True,
            'overall_integrity': True
        }
        
        # Check non-encrypted columns for exact match
        encrypted_cols = processed_df.attrs.get('encrypted_columns', [])
        non_encrypted_cols = [col for col in original_df.columns if col not in encrypted_cols]
        
        for col in non_encrypted_cols:
            if col in processed_df.columns:
                if not original_df[col].equals(processed_df[col]):
                    validation_results['non_encrypted_columns_match'] = False
                    break
        
        # Overall integrity check
        validation_results['overall_integrity'] = all([
            validation_results['row_count_match'],
            validation_results['column_count_match'],
            validation_results['non_encrypted_columns_match']
        ])
        
        return validation_results
    
    def export_audit_log(self, output_path: str = None) -> str:
        """Export audit log to file"""
        
        if output_path is None:
            output_path = f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        audit_data = {
            'generated_at': datetime.now().isoformat(),
            'total_operations': len(self.audit_log),
            'operations': self.audit_log
        }
        
        with open(output_path, 'w') as f:
            json.dump(audit_data, f, indent=2)
        
        logger.info(f"Audit log exported to {output_path}")
        return output_path
    
    def get_encryption_summary(self) -> Dict[str, any]:
        """Get summary of encryption operations"""
        
        summary = {
            'key_type': 'Fernet (AES 128)',
            'operations_performed': len(self.audit_log),
            'last_operation': self.audit_log[-1] if self.audit_log else None,
            'sensitive_column_types': list(self.SENSITIVE_COLUMNS.keys())
        }
        
        return summary

# Utility functions for integration
def setup_encryption_for_dashboard(encryption_key: str = None) -> SecureDataHandler:
    """Setup encryption handler for dashboard use"""
    
    handler = SecureDataHandler(encryption_key)
    logger.info("Encryption handler initialized for dashboard")
    return handler

def secure_contract_data(df: pd.DataFrame, 
                        security_level: str = 'medium') -> pd.DataFrame:
    """Quick function to secure contract data"""
    
    handler = SecureDataHandler()
    
    if security_level == 'high':
        cols_to_encrypt = ['Vendor', 'Annual Spend', 'Contract Number']
    elif security_level == 'medium':
        cols_to_encrypt = ['Annual Spend']
    else:
        cols_to_encrypt = []
    
    return handler.encrypt_dataframe(df, cols_to_encrypt)

# Example usage
if __name__ == "__main__":
    # Example usage
    handler = SecureDataHandler()
    
    # Example DataFrame
    sample_data = pd.DataFrame({
        'Vendor': ['Company A', 'Company B', 'Company C'],
        'Annual Spend': [100000, 250000, 75000],
        'Contract Number': ['CT-001', 'CT-002', 'CT-003'],
        'Description': ['Software License', 'Cloud Services', 'Support Contract']
    })
    
    print("Original data:")
    print(sample_data)
    
    # Encrypt sensitive data
    encrypted_data = handler.encrypt_dataframe(sample_data)
    print("\nEncrypted data:")
    print(encrypted_data)
    
    # Decrypt data
    decrypted_data = handler.decrypt_dataframe(encrypted_data)
    print("\nDecrypted data:")
    print(decrypted_data)
    
    # Create masked version
    masked_data = handler.create_masked_version(sample_data)
    print("\nMasked data:")
    print(masked_data)
    
    print("\nSecurity handler module loaded successfully")