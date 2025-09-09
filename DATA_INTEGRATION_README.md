# ISSA Data Integration System

This document describes the data integration capabilities added to the ISSA dashboard system.

## Overview

The ISSA Data Integration System allows the dashboard to:
- Connect to enterprise systems like SAP and Paycom
- Process uploaded CSV/Excel files
- Automatically update dashboard metrics
- Handle data security and encryption
- Run automated data pipelines

## Components

### 1. Data Connectors (`src/integrations/data_connectors.py`)
- **SAPContractConnector**: Connects to SAP S/4HANA systems
- **PaycomHRConnector**: Connects to Paycom HR systems
- **DataSourceManager**: Manages multiple data sources

### 2. File Processors (`src/integrations/file_processors.py`)
- **ContractFileProcessor**: Processes individual files
- **BatchFileProcessor**: Processes multiple files at once
- Supports CSV, Excel, and other formats
- Auto-detects column mappings

### 3. Security Handler (`src/security/data_encryption.py`)
- **SecureDataHandler**: Encrypts sensitive data
- Creates masked versions for display
- Maintains audit logs

### 4. Data Pipeline (`src/pipelines/data_pipeline.py`)
- **ContractDataPipeline**: Automated data processing
- Scheduled runs and manual triggers
- Data quality validation
- Report generation

## Setup Instructions

### 1. Install Dependencies
```bash
pip install cryptography requests schedule