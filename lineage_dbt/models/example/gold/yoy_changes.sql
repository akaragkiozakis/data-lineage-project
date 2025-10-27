{{ config(materialized='view') }}

-- Year-over-year percentage changes for each indicator
WITH base AS (
    SELECT
        series_id,
        indicator_name,
        DATE_TRUNC('year', observation_date) AS year,
        AVG(value) AS avg_value
    FROM {{ ref('fred_clean') }}
    GROUP BY series_id, indicator_name, DATE_TRUNC('year', observation_date)
)

SELECT
    series_id,
    indicator_name,
    year,
    ROUND(avg_value, 2) AS avg_value,
    ROUND(
        100 * (avg_value - LAG(avg_value) OVER (PARTITION BY series_id ORDER BY year))
            / LAG(avg_value) OVER (PARTITION BY series_id ORDER BY year),
        2
    ) AS yoy_change_pct
FROM base
ORDER BY series_id, year