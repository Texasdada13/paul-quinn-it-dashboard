# Paul Quinn College IT Spend Analysis

## Project Overview
This project builds an IT spend analysis tool for Paul Quinn College to help CFO, CIO, and CTO make data-driven decisions.

## Quick Start
1. Install Python 3.9 or higher
2. Open terminal in project folder
3. Run: `pip install -r 01_Setup/requirements.txt`
4. Run: `python 03_Code/create_test_data.py` to generate sample data
5. Run ETL scripts in `03_Code/etl/` folder

## Folder Structure
- **01_Setup**: Configuration files and setup instructions
- **02_Data**: Raw and processed data files
  - `raw/`: Original Excel files from Paul Quinn
  - `processed/`: Cleaned CSV files ready for Power BI
  - `samples/`: Test data for development
- **03_Code**: Python scripts and notebooks
  - `config/`: Database and system configurations
  - `etl/`: Extract, Transform, Load scripts
  - `analysis/`: Data analysis scripts
  - `reports/`: Report generation scripts
- **04_Documentation**: Project documentation
  - `meeting_notes/`: Notes from client meetings
  - `data_mappings/`: Source to target mappings
- **05_PowerBI**: Power BI reports and dashboards
  - `dashboards/`: .pbix files
  - `datasets/`: Shared datasets

## Key Files
- `simple_vendor_etl.py`: Process vendor data
- `simple_project_etl.py`: Process project data
- `create_test_data.py`: Generate sample data for testing

## Contact
- Project Lead: [Your Name]
- Client: Paul Quinn College
