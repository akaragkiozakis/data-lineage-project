# 📊 Data Lineage Project with FRED Economic Data

A complete data engineering pipeline that fetches economic data from the Federal Reserve Economic Data (FRED) API, loads it into Snowflake, and transforms it using dbt for analytics and reporting.

## 🎯 Project Overview

This project demonstrates a modern data stack with:
- **API Data Ingestion** from FRED (Federal Reserve Economic Data)
- **Data Warehousing** with Snowflake
- **Data Transformation** using dbt (data build tool)
- **Data Lineage Tracking** with DataHub integration

## 🏗️ Architecture

```
FRED API → Python Scripts → Snowflake → dbt → Analytics Views
    ↓           ↓              ↓         ↓         ↓
Raw JSON → data/raw/ → RAW.FRED_DATA → SILVER → Business Intelligence
```

## 📈 Economic Indicators Tracked

- **GDPC1** - Real GDP (Billions $)
- **UNRATE** - Unemployment Rate (%)
- **CPIAUCSL** - Consumer Price Index (1982-1984=100)
- **INDPRO** - Industrial Production (2017=100)
- **PCE** - Personal Consumption Expenditures (Billions)
- **FEDFUNDS** - Federal Funds Rate (%)

## 🛠️ Tech Stack

- **Python 3.10+** - Data ingestion and processing
- **Snowflake** - Cloud data warehouse
- **dbt** - Data transformation and modeling
- **FRED API** - Economic data source
- **DataHub** - Data discovery and lineage (optional)

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python dependencies
pip install snowflake-connector-python dbt-snowflake python-dotenv requests
```

### Environment Setup
Create a `.env` file:
```env
FRED_API_KEY=your_fred_api_key_here
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username  
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=RAW
```

### 1. Data Ingestion
```bash
# Fetch latest economic data from FRED API
python api_ingestion/fetch_data.py
```

### 2. Load to Snowflake
```bash
# Upload JSON data to Snowflake RAW layer
python snowflake_load/load_to_snowflake.py
```

### 3. dbt Transformations
```bash
cd lineage_dbt
dbt debug  # Test connection
dbt run     # Run all transformations
```

## 📊 Data Models

### Silver Layer (Cleaned Data)
- **`fred_clean`** - Cleaned and standardized FRED data with proper data types

### Gold Layer (Analytics)
- **`yearly_averages`** - Average annual values for each economic indicator
- **`yoy_changes`** - Year-over-year percentage changes analysis
- **`real_interest_rates`** - Real interest rates calculation (Fed Funds - Inflation)

## 📁 Project Structure

```
├── api_ingestion/          # FRED API data fetching
│   ├── __init__.py
│   └── fetch_data.py
├── configs/                # Configuration files
│   ├── __init__.py
│   └── fred_series.py      # FRED series definitions
├── data/
│   └── raw/                # Downloaded JSON files
├── lineage_dbt/            # dbt project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       └── example/
│           ├── silver/     # Cleaned data models
│           └── gold/       # Analytics models
├── snowflake_load/         # Snowflake loading scripts
│   └── load_to_snowflake.py
├── logs/                   # Application logs
└── README.md
```

## 🔄 Data Lineage

```mermaid
graph LR
    A[FRED API] --> B[JSON Files]
    B --> C[RAW.FRED_DATA]
    C --> D[SILVER.FRED_CLEAN]
    D --> E[GOLD.YEARLY_AVERAGES]
    D --> F[GOLD.YOY_CHANGES]  
    D --> G[GOLD.REAL_INTEREST_RATES]
```

## 📋 Data Quality & Testing

```bash
# Run dbt tests
dbt test

# Check data freshness
dbt source freshness
```

## 🏃‍♂️ Running the Full Pipeline

```bash
# 1. Fetch latest data
python api_ingestion/fetch_data.py

# 2. Load to Snowflake  
python snowflake_load/load_to_snowflake.py

# 3. Transform with dbt
cd lineage_dbt && dbt run

# 4. Generate documentation
dbt docs generate && dbt docs serve
```

## 📊 Sample Queries

### Economic Trends Analysis
```sql
-- Top 3 years with highest GDP growth
SELECT year, yoy_change_pct 
FROM SILVER.YOY_CHANGES 
WHERE series_id = 'GDPC1' 
ORDER BY yoy_change_pct DESC 
LIMIT 3;
```

### Real Interest Rate Analysis
```sql
-- Years with negative real interest rates
SELECT year, real_interest_rate
FROM SILVER.REAL_INTEREST_RATES 
WHERE real_interest_rate < 0
ORDER BY year;
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Federal Reserve Bank of St. Louis** for providing the FRED API
- **Snowflake** for the cloud data warehouse platform
- **dbt Labs** for the transformation framework

## 📞 Contact

For questions or suggestions, please open an issue in this repository.

---

**Built with ❤️ for modern data engineering**