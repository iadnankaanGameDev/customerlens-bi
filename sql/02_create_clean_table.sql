/*
Project: CustomerLens BI
File purpose: Create a typed and cleaned transaction table from raw imports.
Input table(s): online_retail_raw
Output table/view(s): online_retail_clean
*/

DROP TABLE IF EXISTS online_retail_clean;

CREATE TABLE online_retail_clean AS
SELECT
    invoice_no,
    stock_code,
    description,
    quantity::INTEGER AS quantity,
    invoice_date::TIMESTAMP AS invoice_date,
    unit_price::NUMERIC(10, 2) AS unit_price,
    customer_id::NUMERIC::INTEGER AS customer_id,
    country,
    quantity::INTEGER * unit_price::NUMERIC(10, 2) AS total_price
FROM online_retail_raw
WHERE invoice_no NOT LIKE 'C%'
  AND quantity IS NOT NULL
  AND unit_price IS NOT NULL
  AND customer_id IS NOT NULL
  AND NULLIF(TRIM(customer_id), '') IS NOT NULL
  AND quantity::INTEGER > 0
  AND unit_price::NUMERIC(10, 2) > 0;
