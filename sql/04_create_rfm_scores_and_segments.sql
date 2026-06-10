/*
Project: CustomerLens BI
File purpose: Calculate RFM scores and assign business segments.
Input table(s): customer_features
Output table/view(s): customer_rfm, customer_rfm_scores, customer_business_segments
*/

DROP VIEW IF EXISTS vw_country_segment_summary;
DROP VIEW IF EXISTS vw_segment_summary;

DROP TABLE IF EXISTS customer_business_segments;
DROP TABLE IF EXISTS customer_rfm_scores;
DROP TABLE IF EXISTS customer_rfm;

CREATE TABLE customer_rfm AS
SELECT
    customer_id,
    country,
    recency_days AS recency,
    total_orders AS frequency,
    total_revenue AS monetary,
    avg_order_value,
    unique_products,
    total_quantity,
    customer_lifetime_days
FROM customer_features;

CREATE TABLE customer_rfm_scores AS
WITH rfm_scored AS (
    SELECT
        customer_id,
        country,
        recency,
        frequency,
        monetary,
        avg_order_value,
        unique_products,
        total_quantity,
        customer_lifetime_days,
        NTILE(5) OVER (ORDER BY recency DESC) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS frequency_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS monetary_score
    FROM customer_rfm
)
SELECT
    *,
    recency_score + frequency_score + monetary_score AS rfm_total_score,
    CONCAT(recency_score, frequency_score, monetary_score) AS rfm_score
FROM rfm_scored;

CREATE TABLE customer_business_segments AS
SELECT
    *,
    CASE
        WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4
            THEN 'Champions'
        WHEN recency_score >= 3 AND frequency_score >= 4 AND monetary_score >= 3
            THEN 'Loyal Customers'
        WHEN recency_score >= 4 AND frequency_score <= 2
            THEN 'New / Promising Customers'
        WHEN recency_score <= 2 AND frequency_score >= 4 AND monetary_score >= 4
            THEN 'At Risk High Value'
        WHEN recency_score <= 2 AND frequency_score <= 2
            THEN 'Hibernating Customers'
        WHEN monetary_score >= 4 AND frequency_score <= 2
            THEN 'Big Spenders'
        ELSE 'Regular Customers'
    END AS business_segment
FROM customer_rfm_scores;
