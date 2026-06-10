/*
Project: CustomerLens BI
File purpose: Build customer-level behavioral and revenue features.
Input table(s): online_retail_clean
Output table/view(s): customer_features
*/

DROP TABLE IF EXISTS customer_features;

CREATE TABLE customer_features AS
SELECT
    customer_id,
    country,
    COUNT(DISTINCT invoice_no) AS total_orders,
    ROUND(SUM(total_price), 2) AS total_revenue,
    ROUND(AVG(total_price), 2) AS avg_line_value,
    ROUND(SUM(total_price) / COUNT(DISTINCT invoice_no), 2) AS avg_order_value,
    SUM(quantity) AS total_quantity,
    COUNT(*) AS total_lines,
    COUNT(DISTINCT stock_code) AS unique_products,
    MIN(invoice_date) AS first_purchase_date,
    MAX(invoice_date) AS last_purchase_date,
    DATE '2011-12-10' - MAX(invoice_date)::DATE AS recency_days,
    MAX(invoice_date)::DATE - MIN(invoice_date)::DATE AS customer_lifetime_days
FROM online_retail_clean
GROUP BY customer_id, country;
