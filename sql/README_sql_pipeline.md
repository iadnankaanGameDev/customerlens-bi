# CustomerLens BI SQL Pipeline

This folder contains the PostgreSQL SQL pipeline for the CustomerLens BI customer segmentation project. The pipeline turns raw UCI Online Retail transaction data into clean transactions, customer-level features, RFM scores, business segments, and Power BI-ready reporting views.

## Pipeline Flow

Raw import data moves through the following stages:

```text
Raw -> Clean -> Customer Features -> RFM Scores -> Business Segments -> Power BI Views
```

## Script Overview

### 01_create_raw_table.sql

- Creates `online_retail_raw`.
- Stores all imported columns as `TEXT`.
- Reduces type conversion issues during CSV or Excel import.

### 02_create_clean_table.sql

- Creates `online_retail_clean` from `online_retail_raw`.
- Converts transaction fields into PostgreSQL types.
- Removes cancelled invoices, invalid quantities, invalid prices, and missing customer IDs.
- Adds `total_price` for revenue calculations.

### 03_create_customer_features.sql

- Creates `customer_features`.
- Aggregates transaction data at customer and country level.
- Calculates order, revenue, product diversity, purchase date, recency, and lifetime metrics.
- Uses `DATE '2011-12-10'` as the recency reference date.

### 04_create_rfm_scores_and_segments.sql

- Creates `customer_rfm`.
- Creates `customer_rfm_scores` using `NTILE(5)` RFM scoring.
- Scores lower recency as better, and higher frequency and monetary value as better.
- Creates `customer_business_segments` with portfolio-friendly business labels.

### 05_create_powerbi_views.sql

- Creates `vw_segment_summary`.
- Creates `vw_country_segment_summary`.
- Provides aggregated customer and revenue metrics for Power BI dashboards.

## Usage Order

Run script `01_create_raw_table.sql` first, then import the Online Retail dataset into `online_retail_raw`. After the import is complete, run the remaining scripts in numeric order:

```text
01_create_raw_table.sql
Import Online Retail data into online_retail_raw
02_create_clean_table.sql
03_create_customer_features.sql
04_create_rfm_scores_and_segments.sql
05_create_powerbi_views.sql
```

If the raw table is dropped and recreated, import the dataset again before running `02_create_clean_table.sql`.
