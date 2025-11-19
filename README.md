# Loan Default Risk Dashboard
A complete end-to-end Loan Default Risk Analysis System designed to help credit analysts, lenders, and financial risk professionals evaluate borrower behavior, identify default-prone segments, and build a clean analytical pipeline from raw Kaggle data → MySQL → Python → Power BI.
This project transforms the Home Credit Default Risk dataset into actionable insights using:
- Python (ETL, cleaning)
- MySQL (raw + cleaned tables)
- Power BI (interactive dashboard)
- Environment variables for secure credential handling
The workflow is fully automated and easily reproducible.

## Business Problem
Financial institutions face major challenges in identifying applicants who pose a higher risk of defaulting on their loans. Traditional manual analysis is slow, inconsistent, and error-prone.
This project helps decision-makers and analysts:
- Understand application-level financial behavior
- Identify high-risk borrower demographics
- Detect income, employment, and credit patterns linked to default
- Build a robust data pipeline using industry-standard tools
- Visualize insights in an organized Power BI dashboard

## Project Structure (Actual Layout)
Loan_default_risk/
├── data/
│   └── application_train.csv          # RAW Kaggle dataset (NOT uploaded to GitHub)
├── scripts/
│   ├── load_data.py                   # Loads CSV into MySQL (raw table)
│   └── clean_data.py                  # Cleans data and inserts into MySQL (clean table)
├── loan_default_risk_dashboard.pbix   # Power BI dashboard (2 pages)
├── .gitignore                         # Hides .env and CSV
└── requirements.txt                   # Python dependencies

## Dataset Source (Required Manual Download)
The dataset cannot be included in the GitHub repo because it exceeds the 100 MB limit.
Please download manually from Kaggle:

🔗 Home Credit Default Risk Dataset
https://www.kaggle.com/competitions/home-credit-default-risk/data

## Technology Stack
- Python
- SQL
- MySQL Server
- Power BI Desktop
- VS Code
- Kaggle
- pandas
- mysql-connector-python
- python-dotenv

## How It Works (End-to-End Pipeline)
1. Data Ingestion — load_data.py
- Reads .env for MySQL credentials
- Loads application_train.csv into pandas
- Dynamically creates MySQL table
- Bulk inserts all rows into: application_train_raw

Key Features:
- Dynamic schema generation
- Handles 300k+ rows
- Uses batch inserts for speed
- Clean separation of credentials via .env

2. Data Cleaning — clean_data.py
Cleaning steps include:
- Handling special values
- Replaces anomalous DAYS_EMPLOYED = 365243 with NULL
- Numeric conversion

3. Power BI Dashboard
Key Measures (DAX): 
- Total Applications = COUNTROWS(Applications)
- Total Defaults = CALCULATE(COUNTROWS(Applications), Applications[TARGET] = 1)
- Default Rate % = DIVIDE([Total Defaults], [Total Applications])
- Average Credit Amount = AVERAGE(Applications[AMT_CREDIT])

## Getting Started
1. Install dependencies: pip install -r requirements.txt
2. Create a .env file (Not uploaded to GitHub — for security)

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=loan_default_db

3. Download the Kaggle dataset
Place here: data/application_train.csv

4. Load raw data into MySQL
python scripts/load_data.py

5. Clean and transform data
python scripts/clean_data.py

6. Open the Power BI dashboard
Open loan_default_risk_dashboard.pbix

Refresh data source

## Performance Notes
- Raw dataset: 307,511 rows
- Cleaning time: ~10–20 seconds
- Ingestion time: optimized via batching
- Power BI refresh: ~5–10 seconds

## Common Issues
MySQL connection error: 
- Ensure MySQL service is running
- Use correct port (default 3306)
- Confirm .env credentials are correct
Power BI not connecting:
- Install MySQL ODBC Connector 8.0
CSV loading error: 
- Ensure file path is correct
- Ensure no Excel app is locking the file

## Contributing
- Fork repo
- Create new branch
- Submit PR with explanation

## Contact
If you need help customizing this dashboard or extending this project, feel free to reach out via GitHub Issues.
This project is free to use for learning, analysis, and portfolio building.
## Contact

If you need help customizing this dashboard or extending this project, feel free to reach out via GitHub Issues.
