{{ config(materialized='view') }}

-- Average annual value for each indicator
SELECT
    series_id,
    indicator_name,
    DATE_TRUNC('year', observation_date) AS year,
    ROUND(AVG(value), 2) AS avg_value
FROM {{ ref('fred_clean') }}
GROUP BY series_id, indicator_name, DATE_TRUNC('year', observation_date)
ORDER BY series_id, year