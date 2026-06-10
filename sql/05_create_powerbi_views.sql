/*
Project: CustomerLens BI
File purpose: Create aggregated views for Power BI reporting.
Input table(s): customer_business_segments
Output table/view(s): vw_segment_summary, vw_country_segment_summary
*/

DROP VIEW IF EXISTS vw_country_segment_summary;
DROP VIEW IF EXISTS vw_segment_summary;

CREATE VIEW vw_segment_summary AS
SELECT
    business_segment,
    COUNT(*) AS customers,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS customer_share_pct,
    ROUND(SUM(monetary), 2) AS total_revenue,
    ROUND(
        SUM(monetary) * 100.0 / SUM(SUM(monetary)) OVER (),
        2
    ) AS revenue_share_pct,
    ROUND(AVG(recency), 2) AS avg_recency,
    ROUND(AVG(frequency), 2) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_monetary
FROM customer_business_segments
GROUP BY business_segment
ORDER BY total_revenue DESC;

CREATE VIEW vw_country_segment_summary AS
SELECT
    country,
    business_segment,
    COUNT(*) AS customers,
    ROUND(SUM(monetary), 2) AS total_revenue
FROM customer_business_segments
GROUP BY country, business_segment
ORDER BY total_revenue DESC;
