"""
Data Connectors for Enterprise Systems
Handles API connections to SAP, Paycom, and other systems
"""

import requests
import pandas as pd
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SAPContractConnector:
    """SAP S/4HANA Contract Data Connector"""
    
    def __init__(self, base_url: str, client_id: str, client_secret: str, username: str = None, password: str = None):
        self.base_url = base_url.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.auth_token = None
        self.session = requests.Session()
        
    def _authenticate(self) -> bool:
        """Authenticate with SAP system"""
        try:
            # Try OAuth2 authentication first
            if self.client_id and self.client_secret:
                auth_url = f"{self.base_url}/sap/bc/sec/oauth2/token"
                
                auth_data = {
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                }
                
                response = requests.post(auth_url, data=auth_data)
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.auth_token = token_data.get('access_token')
                    logger.info("SAP OAuth2 authentication successful")
                    return True
                    
            # Fallback to basic authentication
            elif self.username and self.password:
                credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
                self.session.headers.update({'Authorization': f'Basic {credentials}'})
                logger.info("SAP Basic authentication configured")
                return True
                
            else:
                logger.error("No valid authentication credentials provided")
                return False
                
        except Exception as e:
            logger.error(f"SAP authentication failed: {e}")
            return False
    
    def fetch_contract_data(self) -> pd.DataFrame:
        """Fetch contract data from SAP"""
        if not self._authenticate():
            raise Exception("SAP authentication failed")
        
        try:
            # SAP OData endpoint for contracts
            endpoint = f"{self.base_url}/sap/opu/odata/sap/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract"
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            if self.auth_token:
                headers['Authorization'] = f'Bearer {self.auth_token}'
            
            # Add query parameters for contract data
            params = {
                '$select': 'PurchaseContract,Supplier,PurchaseContractType,CompanyCode,CreationDate,ValidityStartDate,ValidityEndDate,NetPriceAmount,Currency',
                '$expand': 'to_PurchaseContractItem',
                '$filter': f"ValidityEndDate ge datetime'{datetime.now().strftime('%Y-%m-%d')}T00:00:00'"
            }
            
            response = self.session.get(endpoint, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return self._transform_sap_data(data)
            else:
                logger.error(f"SAP API error: {response.status_code} - {response.text}")
                raise Exception(f"SAP API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching SAP data: {e}")
            raise
    
    def _transform_sap_data(self, raw_data: Dict) -> pd.DataFrame:
        """Transform SAP data to ISSA standard format"""
        contracts = []
        
        try:
            results = raw_data.get('d', {}).get('results', [])
            
            for item in results:
                # Extract contract details
                contract = {
                    'Vendor': item.get('Supplier', ''),
                    'System/Product': item.get('PurchaseContractType', ''),
                    'Contract Start Date': self._parse_sap_date(item.get('ValidityStartDate')),
                    'Contract End Date': self._parse_sap_date(item.get('ValidityEndDate')),
                    'Annual Spend': float(item.get('NetPriceAmount', 0)),
                    'Currency': item.get('Currency', 'USD'),
                    'Contract Number': item.get('PurchaseContract', ''),
                    'Company Code': item.get('CompanyCode', ''),
                    'Renewal Option': 'Unknown',  # May need custom field
                    'Contract Type': item.get('PurchaseContractType', ''),
                    'Department': item.get('CompanyCode', ''),
                    'Source_System': 'SAP',
                    'Last_Updated': datetime.now().isoformat()
                }
                
                # Calculate additional fields
                if contract['Contract End Date']:
                    end_date = pd.to_datetime(contract['Contract End Date'])
                    contract['Days Until Expiry'] = (end_date - datetime.now()).days
                else:
                    contract['Days Until Expiry'] = None
                
                contracts.append(contract)
            
            df = pd.DataFrame(contracts)
            logger.info(f"Transformed {len(df)} SAP contracts")
            return df
            
        except Exception as e:
            logger.error(f"Error transforming SAP data: {e}")
            return pd.DataFrame()
    
    def _parse_sap_date(self, sap_date_string: str) -> str:
        """Parse SAP date format to standard datetime"""
        if not sap_date_string:
            return None
            
        try:
            # SAP OData dates come as "/Date(1234567890000)/"
            if '/Date(' in sap_date_string:
                timestamp = int(sap_date_string.split('(')[1].split(')')[0]) / 1000
                return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            else:
                # Try parsing as ISO date
                return pd.to_datetime(sap_date_string).strftime('%Y-%m-%d')
        except:
            return sap_date_string

class PaycomHRConnector:
    """Paycom HR/Contract Data Connector"""
    
    def __init__(self, api_key: str, company_id: str, base_url: str = "https://api.paycom.com/v4"):
        self.api_key = api_key
        self.company_id = company_id
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """Test Paycom API connection"""
        try:
            endpoint = f"{self.base_url}/companies/{self.company_id}"
            response = self.session.get(endpoint)
            
            if response.status_code == 200:
                logger.info("Paycom connection test successful")
                return True
            else:
                logger.error(f"Paycom connection test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Paycom connection test error: {e}")
            return False
    
    def fetch_vendor_contracts(self) -> pd.DataFrame:
        """Fetch vendor/contractor data from Paycom"""
        try:
            # Fetch vendors/contractors
            vendors_endpoint = f"{self.base_url}/companies/{self.company_id}/vendors"
            response = self.session.get(vendors_endpoint)
            
            if response.status_code == 200:
                data = response.json()
                return self._transform_paycom_data(data)
            else:
                logger.error(f"Paycom API error: {response.status_code} - {response.text}")
                raise Exception(f"Paycom API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error fetching Paycom data: {e}")
            raise
    
    def _transform_paycom_data(self, raw_data: Dict) -> pd.DataFrame:
        """Transform Paycom data to ISSA standard format"""
        contracts = []
        
        try:
            vendors = raw_data.get('vendors', [])
            
            for vendor in vendors:
                contract = {
                    'Vendor': vendor.get('name', ''),
                    'System/Product': vendor.get('service_type', ''),
                    'Contract Start Date': vendor.get('start_date', ''),
                    'Contract End Date': vendor.get('end_date', ''),
                    'Annual Spend': float(vendor.get('annual_payment', 0)),
                    'Currency': 'USD',
                    'Vendor ID': vendor.get('vendor_id', ''),
                    'Status': vendor.get('status', ''),
                    'Renewal Option': vendor.get('auto_renewal', 'No'),
                    'Contract Type': 'Service Agreement',
                    'Department': vendor.get('department', ''),
                    'Source_System': 'Paycom',
                    'Last_Updated': datetime.now().isoformat()
                }
                
                # Calculate days until expiry
                if contract['Contract End Date']:
                    try:
                        end_date = pd.to_datetime(contract['Contract End Date'])
                        contract['Days Until Expiry'] = (end_date - datetime.now()).days
                    except:
                        contract['Days Until Expiry'] = None
                else:
                    contract['Days Until Expiry'] = None
                
                contracts.append(contract)
            
            df = pd.DataFrame(contracts)
            logger.info(f"Transformed {len(df)} Paycom contracts")
            return df
            
        except Exception as e:
            logger.error(f"Error transforming Paycom data: {e}")
            return pd.DataFrame()

class GenericAPIConnector:
    """Generic API connector for other systems"""
    
    def __init__(self, base_url: str, auth_type: str = 'bearer', **auth_params):
        self.base_url = base_url.rstrip('/')
        self.auth_type = auth_type.lower()
        self.auth_params = auth_params
        self.session = requests.Session()
        self._setup_authentication()
    
    def _setup_authentication(self):
        """Setup authentication based on auth_type"""
        if self.auth_type == 'bearer':
            token = self.auth_params.get('token')
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            
        elif self.auth_type == 'basic':
            username = self.auth_params.get('username')
            password = self.auth_params.get('password')
            credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
            self.session.headers.update({'Authorization': f'Basic {credentials}'})
            
        elif self.auth_type == 'api_key':
            api_key = self.auth_params.get('api_key')
            header_name = self.auth_params.get('header_name', 'X-API-Key')
            self.session.headers.update({header_name: api_key})
    
    def fetch_data(self, endpoint: str, params: Dict = None) -> Dict:
        """Generic data fetch method"""
        try:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            logger.error(f"Error fetching from {endpoint}: {e}")
            raise

class DataSourceManager:
    """Manage multiple data sources for ISSA metrics"""
    
    def __init__(self):
        self.connectors = {}
        self.last_fetch_times = {}
        
    def register_connector(self, name: str, connector):
        """Register a data connector"""
        self.connectors[name] = connector
        logger.info(f"Registered connector: {name}")
    
    def get_consolidated_contract_data(self) -> pd.DataFrame:
        """Get contract data from all sources and consolidate"""
        all_data = []
        
        for name, connector in self.connectors.items():
            try:
                logger.info(f"Fetching data from {name}...")
                
                if hasattr(connector, 'fetch_contract_data'):
                    data = connector.fetch_contract_data()
                elif hasattr(connector, 'fetch_vendor_contracts'):
                    data = connector.fetch_vendor_contracts()
                else:
                    logger.warning(f"Connector {name} doesn't have expected fetch method")
                    continue
                
                if data is not None and not data.empty:
                    data['Data_Source'] = name
                    data['Fetch_Time'] = datetime.now().isoformat()
                    all_data.append(data)
                    self.last_fetch_times[name] = datetime.now()
                    logger.info(f"Fetched {len(data)} records from {name}")
                else:
                    logger.warning(f"No data returned from {name}")
                    
            except Exception as e:
                logger.error(f"Failed to fetch from {name}: {e}")
                continue
        
        if all_data:
            consolidated = pd.concat(all_data, ignore_index=True, sort=False)
            deduplicated = self._deduplicate_contracts(consolidated)
            logger.info(f"Consolidated {len(deduplicated)} unique contracts from {len(all_data)} sources")
            return deduplicated
        else:
            logger.warning("No data retrieved from any source")
            return pd.DataFrame()
    
    def _deduplicate_contracts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate contracts across data sources"""
        if df.empty:
            return df
            
        # Create unique identifier
        df['Vendor_Clean'] = df['Vendor'].str.upper().str.strip()
        df['Product_Clean'] = df['System/Product'].str.upper().str.strip()
        df['Contract_Key'] = df['Vendor_Clean'] + '|' + df['Product_Clean']
        
        # Define source priority (higher number = higher priority)
        priority_map = {
            'SAP': 3,
            'Paycom': 2,
            'File_Upload': 1,
            'Generic': 1
        }
        
        df['Source_Priority'] = df['Data_Source'].map(priority_map).fillna(0)
        
        # Sort by priority and keep first occurrence of each contract
        df_sorted = df.sort_values(['Contract_Key', 'Source_Priority'], ascending=[True, False])
        deduplicated = df_sorted.drop_duplicates('Contract_Key', keep='first')
        
        # Clean up temporary columns
        columns_to_drop = ['Vendor_Clean', 'Product_Clean', 'Contract_Key', 'Source_Priority']
        deduplicated = deduplicated.drop(columns=[col for col in columns_to_drop if col in deduplicated.columns])
        
        return deduplicated.reset_index(drop=True)
    
    def get_data_source_status(self) -> Dict[str, Dict]:
        """Get status of all data sources"""
        status = {}
        
        for name, connector in self.connectors.items():
            try:
                # Test connection if method exists
                if hasattr(connector, 'test_connection'):
                    is_connected = connector.test_connection()
                else:
                    is_connected = True  # Assume connected if no test method
                
                status[name] = {
                    'connected': is_connected,
                    'last_fetch': self.last_fetch_times.get(name),
                    'connector_type': type(connector).__name__
                }
                
            except Exception as e:
                status[name] = {
                    'connected': False,
                    'error': str(e),
                    'connector_type': type(connector).__name__
                }
        
        return status

# Example usage and testing
if __name__ == "__main__":
    # Example of how to use the connectors
    
    # Initialize data source manager
    manager = DataSourceManager()
    
    # Example SAP connector (replace with real credentials)
    # sap_connector = SAPContractConnector(
    #     base_url="https://your-sap-system.com",
    #     client_id="your_client_id",
    #     client_secret="your_client_secret"
    # )
    # manager.register_connector("SAP", sap_connector)
    
    # Example Paycom connector (replace with real credentials)
    # paycom_connector = PaycomHRConnector(
    #     api_key="your_api_key",
    #     company_id="your_company_id"
    # )
    # manager.register_connector("Paycom", paycom_connector)
    
    # Get consolidated data
    # contract_data = manager.get_consolidated_contract_data()
    # print(f"Retrieved {len(contract_data)} contracts")
    
    print("Data connectors module loaded successfully")